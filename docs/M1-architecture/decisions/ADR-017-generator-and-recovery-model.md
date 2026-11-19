# ADR-017 — Generator and Recovery Model: Journal-Based Staged Commit & Recovery

| Thuộc tính | Giá trị |
|---|---|
| ADR ID | ADR-017 |
| Title | Generator and Recovery Model: Journal-Based Staged Commit and Crash Recovery |
| Status | Proposed — Ready for Owner Review |
| Decision Authority | Principal Systems Architect |
| Date | 2026-11-17 |
| Target Milestone | M1 — Documentation & Architecture Foundation |
| Related Modules | `MOD-22-GEN`, `MOD-20-ART`, `pfs-generator` |
| Related Requirements | M1-EXE-004, M1-DOM-004, M0-MTH-006, M0-ART-004 |
| Related Diagrams | DIA-012-generator-sequence.mmd, DIA-016-failure-recovery-flow.mmd |
| Invariant Reference | INV-08, INV-09 |
| Audit Remediation | Resolved finding FND-M1-05 (Journal-Based Commit replacing 2PC filesystem claim) and FND-M1-08 (Concrete Revisit Conditions) |

---

## 1. Context & Problem Statement

Bộ sinh mã và tài liệu (Generator) là nơi hệ thống tương tác trực tiếp với hệ thống tệp tin (Filesystem) của người dùng. Trong thực tế, các rủi ro nghiêm trọng thường xuyên xảy ra:
- Máy tính bị sập nguồn hoặc hết dung lượng ổ đĩa khi đang ghi tệp, khiến một nửa số tệp tin bị hỏng (Corrupted Partial Write).
- Generator âm thầm ghi đè lên các tệp tin chứa mã nguồn tùy biến của người dùng mà không có cảnh báo trước, làm mất mát dữ liệu không thể phục hồi.
- Không thể tái lập lại chính xác gói Foundation đã sinh do template hoặc biến môi trường bị thay đổi.
- Các filesystem thông thường (NTFS trên Windows, ext4/xfs trên Linux) không cung cấp giao dịch phân tán hai pha (Two-Phase Commit - 2PC) trên toàn bộ cây thư mục; các tuyên bố 2PC trên filesystem là không chính xác về mặt kỹ thuật.

Cần một kiến trúc sinh tệp tin xác định, hỗ trợ kiểm tra trước (Dry-run Preview), phát hiện xung đột dựa trên mã băm, có nhật ký giao dịch ghi trước (Write-Ahead Journal) và khả năng phục hồi nhất quán sau sự cố (Crash Consistency).

---

## 2. Decision Drivers

- **Zero Silent Overwrite:** Tuyệt đối không âm thầm ghi đè tệp tin của người dùng.
- **Journal-Based Crash Consistency:** Sử dụng Write-Ahead Journal bền vững trên đĩa để bảo đảm nếu tiến trình bị dừng đột ngột (crash/mất điện), hệ thống có thể hoàn tác hoặc khôi phục về trạng thái sạch sẽ.
- **Per-File Atomic Replacement:** Áp dụng thao tác đổi tên nguyên tử ở cấp độ từng tệp tin đơn lẻ (`rename()` trên POSIX, `MoveFileExW` với `MOVEFILE_REPLACE_EXISTING` trên Windows).
- **Tính lặp lại xác định (Idempotency):** Chạy lại lệnh sinh với cùng cấu hình đầu vào sẽ không tạo ra sự khác biệt hay lỗi trùng lặp.
- **Phân kỳ lộ trình rõ ràng:** Tách biệt Minimal Generator Foundation (trong M2 phục vụ First Vertical Slice) và Full Generator Engine (trong M4).

---

## 3. Options Considered

- **Option A: Direct In-Place File Writing:**
  - Ghi đè trực tiếp từng tệp tin vào thư mục làm việc của dự án.
  - *Nhược điểm:* Cực kỳ nguy hiểm; nếu tiến trình bị ngắt giữa chừng, không gian làm việc sẽ rơi vào trạng thái dở dang và mất dữ liệu.
- **Option B: Distributed Two-Phase Commit (2PC) over Filesystem:**
  - Giả định hệ điều hành hỗ trợ giao dịch 2PC nguyên tử trên toàn bộ workspace.
  - *Nhược điểm:* Không khả thi trên các hệ điều hành thông dụng; `renameat2` chỉ hoạt động trên Linux nội bộ một mount point và không thể thay thế toàn bộ cây thư mục đang có tệp tin con trên Windows.
- **Option C (Được chọn): Journal-Based Staged Commit & Recovery kết hợp Ownership Manifest:**
  - Áp dụng quy trình 13 giai đoạn an toàn:
    1. *Inspect workspace* mục tiêu (kiểm tra quyền, symlinks, disk space).
    2. *Build generation plan* phân giải DAG artifacts.
    3. *Resolve ownership & conflict* đối chiếu mã băm với `.pfs-manifest.json`.
    4. *Prepare staging area* tại `.pfs/staging/<session_ulid>/`.
    5. *Generate staged artifacts* và tính SHA-256 trong thư mục tạm.
    6. *Validate staged artifacts* bằng linters và schema checkers.
    7. *Verify target pre-state* bảo đảm workspace không bị thay đổi bất ngờ.
    8. *Write durable journal* tại `.pfs/journal/<ulid>.json` với lời gọi `sync_all()`.
    9. *Apply platform changes* bằng primitive hoán đổi nguyên tử từng tệp kèm sao lưu tệp cũ vào `.pfs/backup/`.
    10. *Record completed operations* lũy tiến vào nhật ký.
    11. *Recover/compensate* khi xảy ra sự cố (hồi phục tệp từ backup).
    12. *Verify final state* đối soát mã băm Merkle toàn không gian làm việc.
    13. *Finalize journal* cập nhật manifest và niêm phong kiểm toán.

---

## 4. Decision & Rationale

**QUYẾT ĐỊNH:** Áp dụng **Option C: Journal-Based Staged Commit & Recovery kết hợp Ownership Manifest**.
- PFS lưu giữ tệp `.pfs-manifest.json` ghi lại mã băm ban đầu của mọi tệp tin do hệ thống sinh ra. Nếu phát hiện tệp tin đã bị người dùng sửa đổi thủ công, Generator lập tức tạm dừng và hiển thị Interactive Diff Preview để yêu cầu hướng dẫn xử lý (Giữ nguyên / Ghi đè / Hợp nhất).
- Toàn bộ các thao tác áp dụng được ghi vào Write-Ahead Journal bền vững trước khi chạm vào không gian làm việc. Nếu xảy ra sự cố, Recovery Engine tự động đọc journal và khôi phục không gian làm việc về trạng thái nguyên vẹn ban đầu.
- Ranh giới giữa M2 và M4: M2 chỉ hiện thực hóa **Minimal Generator Foundation** (staging cơ bản, sinh tệp đơn lẻ an toàn, xóa staging khi lỗi); M4 hiện thực hóa toàn bộ **Full Generator Engine** với đầy đủ 13 giai đoạn và crash recovery.

---

## 5. Consequences & Trade-offs

### 5.1. Tích cực (Positive Consequences)
- An toàn dữ liệu tối đa; người dùng hoàn toàn kiểm soát những gì được ghi lên đĩa; không bao giờ mất mã nguồn tự viết.
- Tính tương thích đa nền tảng vững chắc (chạy an toàn cả trên Windows NTFS lẫn Linux ext4/btrfs).
- Có thể phục hồi nhất quán sau sự cố sập nguồn hoặc crash tiến trình.

### 5.2. Thách thức (Negative Consequences)
- Yêu cầu dung lượng đĩa tạm thời trong quá trình staging và backup trước khi finalize giao dịch.
- Tốc độ sinh tệp có độ trễ I/O nhất định do việc gọi `sync_all()` để bảo đảm tính bền vững của Journal.

---

## 6. Security & Operational Implications

- **Path Traversal Protection:** Tất cả đường dẫn tệp tin đều được chuẩn hóa bằng `canonicalize()` và xác thực `path.starts_with(workspace_root)`. Tuyệt đối cấm ký tự `..` hoặc symlinks trỏ ra ngoài thư mục dự án.
- **Idempotency Key:** Mỗi phiên sinh tệp được gán một `generation_session_id` (ULID) duy nhất; nếu nhận lệnh trùng lặp, hệ thống trả về kết quả đã hoàn thành mà không ghi đè lại.

---

## 7. Dependencies & Compatibility

- **Phụ thuộc:** `MOD-20-ART` (Content-Addressed Storage), `MOD-21-TPL` (Template Management), `MOD-11-POL` (Authorization L3/L4 Check).
- **Hạ tầng tệp tin:** Tương thích Windows (NTFS, ReFS), Linux (ext4, xfs, btrfs), macOS (APFS).

---

## 8. Status & Owner Governance

- **Trạng thái:** `Proposed — Ready for Owner Review`.
- **Thẩm quyền phê duyệt:** Project Owner (Nguyễn Thế Thuận) — Bảo lưu cho quyết định OD-M1-01 / OD-M1-03.
- **Bằng chứng kiến trúc:** `E2 — Specified` (Đặc tả chi tiết tại `docs/M1-architecture/04-execution-architecture/18-GENERATION-AND-RECOVERY-ARCHITECTURE.md` và `DIA-012-generator-sequence.mmd`).

---

## 9. Revisit Conditions

Kiến trúc Journal-Based Staged Commit & Recovery sẽ được xem xét lại (Revisit) khi và chỉ khi xuất hiện một trong các điều kiện đo lường được sau đây:
1. **Hạn ngạch dung lượng ổ đĩa:** Khi các bài kiểm thử thực tế (Benchmarks) trên dự án lớn (> 50.000 tệp tin hoặc > 10GB Foundation Package) cho thấy chi phí staging và backup làm cạn kiệt dung lượng đĩa tạm và gây lỗi tràn ổ đĩa ở tỷ lệ > 5% các ca thử nghiệm.
2. **Hiệu năng I/O:** Khi thời gian hoàn tất quy trình 13 giai đoạn vượt quá 30 giây cho một Foundation Package tiêu chuẩn (< 500 tệp tin), đòi hỏi phải tối ưu hóa bằng streaming direct write kết hợp copy-on-write snapshot ở cấp độ hệ thống tệp tin (ví dụ: btrfs/zfs subvolume clones hoặc Windows VSS).
3. **Tiêu chuẩn công nghệ mới:** Khi hệ điều hành mục tiêu hoặc Rust standard library cung cấp một trừu tượng hóa giao dịch hệ thống tệp tin nguyên tử cấp không gian người dùng (User-space Transactional Filesystem Abstraction) được kiểm chứng chính thức trên cả Windows và POSIX.
