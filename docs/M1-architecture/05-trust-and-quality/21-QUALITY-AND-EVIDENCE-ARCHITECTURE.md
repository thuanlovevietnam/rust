# PFS-M1-DOC-021 — Quality Engine, Gates & Evidence Architecture

| Thuộc tính | Giá trị |
|---|---|
| Document ID | PFS-M1-DOC-021 |
| Document Title | Quality Engine, Gates and Evidence Architecture Specification |
| Project | Project Foundation System (PFS) |
| Milestone | M1 — Documentation & Architecture Foundation |
| Version | 1.0.0 |
| Status | Proposed — Ready for Owner Review |
| Authority | Principal Systems Architect & Quality Assurance Lead |
| Classification | Internal |
| Reference Architecture | Evidence-Based Software Engineering, ISO/IEC 25010 (System and Software Quality) |
| Related Decisions | ADR-016, ADR-015 |
| Parent Baseline | [PFS-M0-SPEC-010](file:///C:/Users/OK259/rust/docs/M0-foundation/10-QUALITY-AND-ACCEPTANCE-MODEL.md) |
| Invariant Reference | INV-07 |

---

## 1. Quality Architecture Principles & Invariants

Trong **Project Foundation System (PFS)**, chất lượng của một dự án nền tảng không được đánh giá bằng cảm tính, không dựa trên những lời khen ngợi chủ quan của AI chatbot, và tuyệt đối không được che đậy bằng điểm số trung bình cộng.

Theo bất biến kiến trúc **INV-07**, PFS hiện thực hóa một **Kiến trúc Chất lượng Dựa trên Bằng chứng (Evidence-Based Quality Architecture)**:
1. **No Evidence, No Pass:** Một tiêu chí nghiệm thu chỉ được công nhận là `Passed` khi có **Bằng chứng Kiểm chứng Độc lập (Independent Evidence Artifact)** đi kèm.
2. **Critical Severity Strict Blocking:** Một phát hiện vi phạm mức `Critical` (ví dụ: phát hiện lỗ hổng an ninh nghiêm trọng hoặc chu trình phụ thuộc) sẽ **LẬP TỨC KHÓA TOÀN BỘ CỔNG CHUYỂN GIAI ĐOẠN (Quality Gate Blocked)**. Tuyệt đối không cho phép bù đắp lỗi Critical bằng điểm số cao ở các tiêu chí khác!
3. **Formal Findings Taxonomy:** Phân biệt rạch ròi giữa Lỗi sản phẩm (Defect), Rủi ro tiềm ẩn (Risk), Điểm lưu ý (Finding), và Ngoại lệ được cấp phép (Waiver).
4. **Distinction between Fact, Assertion, and Assumption:** Phân định rõ ràng giữa **Bằng chứng thực nghiệm (Empirical Fact)**, **Khẳng định do AI sinh ra (AI Assertion)**, và **Giả định chưa xác minh (Unverified Assumption)**.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       Quality Engine Verification Flow                      │
├─────────────────────────────────────────────────────────────────────────────┤
│  [ Stage Deliverables & Artifacts ]                                         │
│        │                                                                    │
│  Phase 1: Deterministic Static Analysis (Schema, Lint, Link Checks)        │
│        │                                                                    │
│  Phase 2: Automated Structural Verification (DAG Acyclicity, Traceability)  │
│        │                                                                    │
│  Phase 3: Evidence Collection & Cryptographic Hashing (SHA-256 Digest)      │
│        │                                                                    │
│  Phase 4: Quality Gate Rule Evaluation (Pass / Fail / Blocked)              │
│        ├── Any Critical Finding? ──> YES ──> [ GATE BLOCKED ] (Halt Flow)   │
│        └── All Criteria Satisfied?──> YES ──> [ GATE PASSED ] (Ready Review)│
│                                                                             │
│  Phase 5: Human Inspection & Verification Sign-off (Auditor / Owner)        │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Comprehensive Quality Dimensions

Chất lượng của một Project Foundation Package được đo lường toàn diện qua 10 chiều không gian (Quality Dimensions):

| Chiều chất lượng | Mục tiêu kiểm chứng | Phương pháp đo lường & Tiêu chuẩn |
|---|---|---|
| **1. Structural Quality** | Cấu trúc thư mục, định dạng tệp và quy ước đặt tên chuẩn xác. | Kiểm tra bằng công cụ phân tích tĩnh (Static linter); 100% tệp tuân thủ lược đồ. |
| **2. Semantic Quality** | Tính mạch lạc, phi mâu thuẫn về mặt ý nghĩa nghiệp vụ giữa các phần mục. | Đối soát chéo các định nghĩa thực thể; không có thuật ngữ mơ hồ hoặc định nghĩa kép. |
| **3. Completeness** | Không bỏ sót bất kỳ thành phần bắt buộc nào của giai đoạn. | Đối chiếu với danh mục Required Deliverables trong Capability Profile; 100% độ phủ. |
| **4. Consistency** | Tính nhất quán giữa yêu cầu, quyết định kiến trúc, sơ đồ và mã nguồn. | Ma trận truy vết hai chiều (Bidirectional Traceability Matrix); 0 liên kết mồ côi. |
| **5. Traceability** | Mọi tạo tác đều truy vết ngược được về nguồn gốc ý tưởng (Project Intent). | Đồ thị Directed Acyclic Graph (DAG) từ Intent đến Artifact không bị đứt đoạn. |
| **6. Security & Privacy** | Tuân thủ mô hình an ninh STRIDE-AI; không có lỗ hổng hoặc lộ lọt dữ liệu. | Quét Secret Redaction; kiểm tra phân quyền L0–L5; 0 lỗi Critical/High tồn đọng. |
| **7. Compatibility** | Tính tương thích phiên bản SemVer giữa Core, Schemas, Templates và Packages.| Ma trận tương thích (Compatibility Matrix); kiểm tra tính tương thích xuôi/ngược. |
| **8. Reproducibility** | Kết quả sinh ra có thể tái lập chính xác 100% trong tương lai từ cùng cấu hình. | Chạy lại Generator trên cùng snapshot; đối soát mã băm SHA-256 trùng khớp 100%. |
| **9. Evidence Sufficiency** | Độ tin cậy và tính đầy đủ của các bằng chứng nộp kèm. | 100% tiêu chí nghiệm thu có tệp bằng chứng thực tế; không chấp nhận khẳng định suông. |
| **10. Human Review** | Đánh giá chuyên môn sâu sắc từ các chuyên gia kiến trúc và chủ sở hữu dự án.| Biên bản đánh giá độc lập (Review Report) có chữ ký số của cấp thẩm quyền. |

---

## 3. Formal Quality Gate Specification

Mỗi Quality Gate trong PFS là một rào chắn kiểm soát xác định (định nghĩa tại `docs/M1-architecture/schemas/quality-gate-schema.json`):

### 3.1. Cấu trúc Hợp đồng Cổng Chất lượng
- `gate_id`: Định danh duy nhất (ví dụ: `QG-04-ARCH-CONSISTENCY`).
- `stage_id`: Giai đoạn vòng đời được bảo vệ (ví dụ: `STG-04-ARCH`).
- `purpose`: Mục đích kiểm soát của cổng.
- `required_inputs`: Danh sách các artifacts và báo cáo bắt buộc phải nạp.
- `validation_rules`: Bộ quy tắc kiểm tra logic (Rules Engine).
- `evidence_requirements`: Danh mục các loại bằng chứng bắt buộc phải có.
- `pass_criteria`: Điều kiện để cổng mở: 100% quy tắc Passed, 0 Critical findings, 0 High findings chưa có waiver.
- `fail_criteria`: Có ít nhất 1 lỗi Critical hoặc thiếu bằng chứng bắt buộc.
- `blocking_behavior`: Khóa toàn bộ workflow; không cho phép chuyển sang giai đoạn tiếp theo.
- `waiver_authority`: Cấp thẩm quyền tối thiểu có quyền cấp ngoại lệ tạm thời (mặc định: `L4` hoặc `L5`).

---

## 4. Evidence Metamodel (Mô hình Bằng chứng Kiểm chứng)

Bằng chứng (Evidence) trong PFS là một thực thể độc lập được bảo vệ tính toàn vẹn bằng mật mã học:

```json
{
  "evidence_id": "evi_01HQZ9G8K5E7B9A3F1M4R2V0W8",
  "project_id": "pfs:project:ws_corp:prj_alpha",
  "evidence_type": "AutomatedTestExecutionReport",
  "source_system": "tools/validation/validate_m1.py",
  "collection_method": "DeterministicProcessExitCode",
  "timestamp": "2026-11-17T13:20:00Z",
  "content_hash_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "raw_output_uri": ".pfs/evidence/m1-validation-output.json",
  "associated_requirements": ["M1-DOM-003", "M1-SEC-001"],
  "associated_gates": ["QG-04-ARCH-CONSISTENCY"],
  "verification_status": "VerifiedPass",
  "verifier_principal": "user_qa_lead_nguyen_the_thuan",
  "attestation_signature": "ed25519_sig_..."
}
```

### 4.1. Phân cấp Độ tin cậy của Bằng chứng (Evidence Reliability Hierarchy)
1. **Tier 1 — Empirical Artifacts (Độ tin cậy cao nhất):** Nhật ký kiểm thử tự động với mã thoát (Exit Code 0), báo cáo quét an ninh tự động, mã băm SHA-256 đối soát trực tiếp trên hệ thống tệp.
2. **Tier 2 — Human Expert Attestation (Độ tin cậy cao):** Báo cáo phản biện độc lập do chuyên gia con người ký duyệt sau khi thẩm định kỹ lưỡng.
3. **Tier 3 — AI-Generated Formal Assertion (Độ tin cậy trung bình):** Kết quả do AI suy luận nhưng đã được kiểm chứng lại bằng bộ xác thực JSON Schema.
4. **Tier 4 — Unverified Assumption (Không được coi là Evidence):** Các nhận định, phỏng đoán hoặc khẳng định chưa được kiểm chứng; chỉ được phép tồn tại trong Assumption Registry kèm kế hoạch xác minh.
