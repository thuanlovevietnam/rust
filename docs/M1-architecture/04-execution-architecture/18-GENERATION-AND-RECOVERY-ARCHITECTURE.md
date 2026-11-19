# PFS-M1-DOC-018 — Foundation Generator and Recovery Architecture

| Thuộc tính | Giá trị |
|---|---|
| Document ID | PFS-M1-DOC-018 |
| Document Title | Foundation Generator and Journal-Based Staged Commit & Recovery Architecture Specification |
| Project | Project Foundation System (PFS) |
| Milestone | M1 — Documentation & Architecture Foundation |
| Version | 1.1.0 |
| Status | Proposed — Ready for Owner Review |
| Authority | Principal Systems Architect |
| Classification | Internal |
| Reference Architecture | Journal-Based Staged Commit & Recovery, Content-Addressed Storage, Crash Consistency |
| Related Diagrams | DIA-012-generator-sequence.mmd, DIA-016-failure-recovery-flow.mmd |
| Related Decisions | ADR-008, ADR-017 |
| Invariant Reference | INV-08, INV-09 |
| Audit Remediation | Resolved finding FND-M1-05 (Journal-Based Recovery replacing 2PC claim) and FND-M1-06 (M2 Minimal vs M4 Full Generator) |

---

## 1. Generator as a Core Product Capability

Trong **Project Foundation System (PFS)**, **Generator (Bộ Sinh Nền tảng)** không đơn thuần là một đoạn mã nối chuỗi văn bản (template string concatenation) hay một lệnh ghi đè tệp tin thô sơ. Generator là một **Năng lực Sản phẩm Cốt lõi (Core Product Capability)** của PFS, chịu trách nhiệm chuyển hóa toàn bộ các mô hình trừu tượng (Requirements, Architecture Designs, Governance Models, Capability Configurations) thành một **Project Foundation Package** hoàn chỉnh, có cấu trúc, có thể kiểm chứng và sẵn sàng cho việc triển khai thực tế.

Generator vận hành dựa trên nguyên lý an toàn tối cao: **Zero Silent Overwrite & Journal-Based Crash Consistency**. Hệ thống tuyệt đối không bao giờ âm thầm ghi đè lên các tệp tin hiện hữu của người dùng mà không có sự đồng ý tường minh.

### 1.1. Phân định Mức độ Nguyên tử trên Hệ thống Tệp tin (Filesystem Atomicity Reality)

Để bảo đảm tính trung thực kỹ thuật và khả thi trên môi trường đa nền tảng (Windows NTFS/ReFS, Linux ext4/xfs/btrfs, macOS APFS), PFS phân định rạch ròi các cấp độ nguyên tử:
1. **Single-File Atomicity (Nguyên tử cấp tệp):** Có thể bảo đảm nguyên tử ở cấp một tệp tin đơn lẻ thông qua thao tác ghi vào tệp tạm cùng volume rồi hoán đổi nguyên tử (`rename()` trên POSIX, `MoveFileExW` với cờ `MOVEFILE_REPLACE_EXISTING` trên Windows).
2. **Directory-Tree Atomicity (Nguyên tử cấp thư mục):** Một số filesystem Linux hỗ trợ `renameat2` với `RENAME_EXCHANGE`, nhưng cơ chế này KHÔNG tồn tại hoặc không đồng nhất trên Windows hoặc giữa các ổ đĩa mount khác nhau.
3. **Workspace Generation Transaction (Giao dịch toàn bộ không gian làm việc):** Các filesystem thông thường KHÔNG hỗ trợ giao dịch phân tán hai pha (Two-Phase Commit - 2PC) trên toàn bộ cây thư mục. Do đó, PFS KHÔNG tuyên bố bảo đảm 2PC phần cứng trên filesystem, mà triển khai mô hình **Journal-Based Staged Commit & Recovery** có tính chất nhất quán khi gặp sự cố (Crash Consistency), ghi nhật ký bền vững (Durable Write-Ahead Journal) và hỗ trợ hoàn tác bồi hoàn (Compensating Rollback).

---

## 2. The 13 Canonical Stages of Generation and Recovery Pipeline

Hệ thống tuân thủ nghiêm ngặt quy trình sinh và áp dụng 13 giai đoạn:

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│                 PFS 13-Stage Journal-Based Staged Commit & Recovery Pipeline                    │
├─────────────────────────────────────────────────────────────────────────────────────────────────┤
│  1. Inspect Target Workspace: Scan existing files, hashes, permissions, and directory tree      │
│                                │                                                                │
│  2. Build Generation Plan: Resolve DAG dependencies, identify target paths and operation types  │
│                                │                                                                │
│  3. Resolve Ownership & Conflict: Compare with .pfs-manifest.json; halt on user modification    │
│                                │                                                                │
│  4. Prepare Staging Area: Initialize isolated scratch space in .pfs/staging/<session_ulid>/     │
│                                │                                                                │
│  5. Generate Staged Artifacts: Render templates, evaluate variables, write clean files to stage │
│                                │                                                                │
│  6. Validate Staged Artifacts: Run schema, format, syntax, and CAS Merkle validation in stage   │
│                                │                                                                │
│  7. Verify Target Pre-State: Confirm target files have not been modified during staging time    │
│                                │                                                                │
│  8. Write Durable Journal: Flush Write-Ahead Journal (.pfs/journal/<ulid>.json) with sync_all()│
│                                │                                                                │
│  9. Apply Platform Changes: Execute step-by-step file swaps using OS-specific atomic primitives │
│                                │                                                                │
│ 10. Record Completed Operations: Progressively update journal after each file transition        │
│                                │                                                                │
│ 11. Recover / Compensate on Failure: If interrupted, execute compensating inverse operations    │
│                                │                                                                │
│ 12. Verify Final State: Recalculate workspace Merkle hash against expected final manifest       │
│                                │                                                                │
│ 13. Finalize Journal: Update .pfs-manifest.json, seal audit ledger entry, archive journal record│
└─────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### Chi tiết 13 giai đoạn thực thi:
1. **Stage 1 — Inspect Target Workspace:** Quét toàn bộ không gian làm việc mục tiêu, kiểm tra dung lượng ổ đĩa khả dụng, quyền ghi tệp và phát hiện các reparse points/symlinks để ngăn chặn tấn công link traversal.
2. **Stage 2 — Build Generation Plan:** Phân giải đồ thị phụ thuộc giữa các artifacts, xác định danh sách các tệp tin cần tạo mới (`Create`), cập nhật (`Update`), xóa bỏ (`Delete`) hoặc giữ nguyên (`Skip`).
3. **Stage 3 — Resolve Ownership & Conflict:** Đọc bảng kê khai `.pfs-manifest.json`. So sánh mã băm SHA-256 hiện tại của từng tệp với mã băm lúc PFS sinh ra trước đó. Nếu phát hiện tệp đã bị người dùng sửa đổi thủ công -> lập tức kích hoạt trạng thái xung đột và dừng quy trình tự động.
4. **Stage 4 — Prepare Staging Area:** Tạo thư mục tạm thời biệt lập tại `.pfs/staging/<ulid>/` trên cùng ổ đĩa logic (cùng filesystem volume) để bảo đảm thao tác chuyển tệp sau này không phải copy dữ liệu xuyên volume.
5. **Stage 5 — Generate Staged Artifacts:** Render toàn bộ cây thư mục và tệp tin mới vào thư mục tạm; tính toán mã băm SHA-256 cho từng tệp.
6. **Stage 6 — Validate Staged Artifacts:** Chạy bộ kiểm định tĩnh (Linters, JSON Schemas, Markdown checkers) trên thư mục staging; nếu phát hiện 1 lỗi Critical/High -> hủy bỏ staging ngay lập tức.
7. **Stage 7 — Verify Target Pre-State:** Đối soát lại một lần nữa mã băm của các tệp trên workspace mục tiêu để bảo đảm không có tiến trình nào khác (con người hoặc công cụ ngoài) vừa can thiệp vào tệp trong lúc staging đang chạy.
8. **Stage 8 — Write Durable Journal:** Ghi lại toàn bộ kế hoạch giao dịch vào tệp Write-Ahead Journal (`.pfs/journal/<ulid>.json`). Bắt buộc gọi `File::sync_all()` (fsync trên Linux, FlushFileBuffers trên Windows) để bảo đảm dữ liệu nhật ký đã nằm an toàn trên đĩa vật lý trước khi sửa workspace.
9. **Stage 9 — Apply Platform Changes:** Thực hiện hoán đổi từng tệp tin theo thứ tự xác định:
   - Trên Linux: Sử dụng `rename()` nguyên tử cho từng tệp.
   - Trên Windows: Sử dụng `MoveFileExW(..., MOVEFILE_REPLACE_EXISTING | MOVEFILE_WRITE_THROUGH)`.
   - Đối với tệp cập nhật: Ghi tệp gốc vào bản sao lưu tạm `.pfs/backup/<ulid>/` trước khi hoán đổi.
10. **Stage 10 — Record Completed Operations:** Sau mỗi thao tác tệp hoàn tất, ghi nhận trạng thái bước vào journal để phục vụ việc bồi hoàn nếu gặp sự cố sập nguồn giữa chừng.
11. **Stage 11 — Recover or Compensate on Failure:** Nếu xảy ra lỗi (hết đĩa, mất quyền, mất điện hoặc tiến trình bị hủy đột ngột), Recovery Engine đọc Journal và khôi phục các tệp tin đã sao lưu từ `.pfs/backup/` về vị trí cũ, đưa workspace về trạng thái sạch sẽ ban đầu.
12. **Stage 12 — Verify Final State:** Tính toán lại mã băm Merkle Root của toàn bộ workspace và so sánh với giá trị kỳ vọng trong Generation Plan.
13. **Stage 13 — Finalize Journal:** Ghi đè mã băm mới vào `.pfs-manifest.json`, niêm phong chữ ký số vào Sổ cái Kiểm toán, dọn dẹp thư mục staging và chuyển journal sang trạng thái `COMMITTED`.

---

## 3. Platform Limitations & Cross-Platform Hardening

Generator được thiết kế có tính tương thích cao giữa Windows và Linux:

| Yếu tố kỹ thuật | Xử lý trên Linux / macOS | Xử lý trên Windows (NTFS / ReFS) |
|---|---|---|
| **Atomic File Replacement** | `rename(old, new)` là nguyên tử POSIX nếu cùng filesystem. | `MoveFileExW` với `MOVEFILE_REPLACE_EXISTING`. Xử lý trường hợp tệp đang bị khóa bởi trình quét virus bằng cơ chế retry có jitter (tối đa 5 lần, 50ms). |
| **Path Traversal & Symlinks** | Sử dụng `std::fs::canonicalize()`; cấm symlinks trỏ ra ngoài workspace root. | Kiểm tra Reparse Points, Volume Junctions và Short Names (8.3 filenames `PROGRA~1`) để tránh qua mặt bộ lọc đường dẫn. |
| **Case Sensitivity** | Phân biệt hoa thường (`README.md` khác `readme.md`). | Mặc định không phân biệt hoa thường; cấm sinh hai tệp chỉ khác nhau về viết hoa viết thường trong cùng thư mục. |
| **File Permissions** | Lưu trữ quyền POSIX mode (0644, 0755) trong manifest. | Ghi nhận thuộc tính Read-Only, không giả định quyền POSIX. |
| **Line Endings (EOL)** | Chuẩn hóa EOL là `\n` (LF) trong Content-Addressed Storage. | Tự động chuyển đổi sang `\r\n` (CRLF) khi áp dụng nếu cấu hình dự án yêu cầu, nhưng mã băm CAS luôn tính trên `\n`. |

---

## 4. Phân Định Phạm Vi Triển Khai: Minimal Generator (M2) vs Full Generator (M4)

Để giải quyết triệt để xung đột lộ trình (FND-M1-06), trách nhiệm của Crate `pfs-generator` được phân kỳ rõ ràng:

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│              Generator Roadmap Separation: M2 Minimal Foundation vs M4 Full Engine              │
├─────────────────────────────────────────────────────────────────────────────────────────────────┤
│  Milestone M2: Minimal Generator Foundation (Phục vụ First Vertical Slice)                      │
│  ├── Phạm vi: Sinh tập artifact tối thiểu xác định (README.md, specs/, .pfs-manifest.json)     │
│  ├── Staging: Thư mục tạm .pfs/staging/ đơn giản                                                │
│  ├── Conflict Detection: So sánh SHA-256 cơ bản, dừng khi phát hiện tệp đã tồn tại             │
│  ├── Apply Engine: Ghi tệp an toàn cấp tệp đơn lẻ (Single-file safe apply)                      │
│  ├── Failure Handling: Xóa sạch staging khi có lỗi; không có multi-file journal rollback phức tạp│
│  └── Verification: Unit test và Integration test cho kịch bản Vertical Slice                    │
├─────────────────────────────────────────────────────────────────────────────────────────────────┤
│  Milestone M4: Full Generator Automation Engine (Sản phẩm hoàn chỉnh)                           │
│  ├── Phạm vi: Toàn bộ 13 giai đoạn Journal-Based Staged Commit & Recovery đầy đủ               │
│  ├── Template Engine: Hỗ trợ template engine đầy đủ, biến phái sinh, điều kiện lồng nhau       │
│  ├── Generation Plan: Đồ thị phụ thuộc đa tầng (Multi-artifact DAG Planning)                   │
│  ├── Ownership & Conflict: Quản trị quyền sở hữu nâng cao, 3-way merge, interactive diff wizard │
│  ├── Journal Engine: Write-Ahead Journal bền vững, khôi phục sau sự cố mất điện (Crash Recovery)│
│  └── Cross-Platform: Tối ưu hóa sâu cho Windows NTFS file locking và Linux cross-volume mounts  │
└─────────────────────────────────────────────────────────────────────────────────────────────────┘
```

> [!NOTE]
> **Cam kết Ranh giới:** Trong Milestone M2, nhóm phát triển KHÔNG cần triển khai toàn bộ động cơ Generator M4 phức tạp; chỉ cần hoàn thành **Minimal Generator Foundation** theo đúng đặc tả của First Vertical Slice.
