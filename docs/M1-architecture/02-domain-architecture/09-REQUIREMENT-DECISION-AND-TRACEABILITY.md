# PFS-M1-DOC-009 — Requirement, Decision and Traceability Architecture

| Thuộc tính | Giá trị |
|---|---|
| Document ID | PFS-M1-DOC-009 |
| Document Title | Requirement, Decision and Traceability Architecture Specification |
| Project | Project Foundation System (PFS) |
| Milestone | M1 — Documentation & Architecture Foundation |
| Version | 1.0.0 |
| Status | Proposed — Ready for Owner Review |
| Authority | Principal Systems Architect |
| Classification | Internal |
| Reference Architecture | Requirements Engineering (ISO/IEC/IEEE 29148), Architecture Decisions (MADR) |
| Related Decisions | ADR-004, ADR-015, ADR-016 |
| Parent Baseline | [PFS-M0-SPEC-006](file:///C:/Users/OK259/rust/docs/M0-foundation/06-AUTHORITY-AND-DECISION-MODEL.md), [PFS-M0-SPEC-007](file:///C:/Users/OK259/rust/docs/M0-foundation/07-ARTIFACT-AND-TRACEABILITY-MODEL.md) |

---

## 1. Traceability Architecture Philosophy

Trong các hệ thống kỹ thuật phức tạp, sự đứt gãy giữa Ý định ban đầu (Intent), Yêu cầu chi tiết (Requirements), Quyết định kiến trúc (Decisions), Công việc thực thi (Tasks) và Sản phẩm bàn giao (Artifacts) là nguyên nhân hàng đầu dẫn đến thất bại dự án.

**Project Foundation System (PFS)** thiết lập kiến trúc **Mạng lưới Truy vết Bất biến Hai chiều (Bidirectional Immutable Traceability Network)** được xây dựng dưới dạng Đồ thị có hướng không chu trình (Directed Acyclic Graph - DAG). Mỗi phần tử trong đồ thị đều sở hữu định danh bất biến (ULID) và các cạnh kết nối có ngữ nghĩa toán học chặt chẽ:

$$\mathbf{Intent} \longrightarrow \mathbf{Requirement} \longrightarrow \mathbf{Decision} \longrightarrow \mathbf{Task} \longrightarrow \mathbf{Artifact} \longrightarrow \mathbf{Evidence} \longrightarrow \mathbf{Quality\ Gate} \longrightarrow \mathbf{Foundation}$$

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                   Bidirectional Traceability Chain (DAG)                    │
├─────────────────────────────────────────────────────────────────────────────┤
│  [Project Intent]                                                          │
│        │ generates                                                          │
│        ▼                                                                    │
│  [Requirement DAG] <──── conflictsWith ────> [Requirement DAG]              │
│        │                                            │                       │
│        │ governedBy                                 │ supportedBy           │
│        ▼                                            ▼                       │
│  [Decision / ADR] ─── governs ───> [Task] ─── produces ───> [Artifact]      │
│        │                                                        │           │
│        │ evaluatedAt                                            │ verifiedBy│
│        ▼                                                        ▼           │
│  [Quality Gate] <───────────── validatedBy ───────────── [Evidence]         │
│        │                                                                    │
│        ▼ certifies                                                          │
│  [Foundation Package Baseline v1.0.0]                                       │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Requirement Modeling & Entity Specification

Yêu cầu (Requirement) trong PFS không phải là một dòng văn bản thuần túy, mà là một thực thể nghiệp vụ có cấu trúc (Formal Entity) tuân thủ JSON Schema tại `docs/M1-architecture/schemas/requirement-schema.json`:

### 2.1. Phân loại Yêu cầu (Requirement Categories)
1. **Functional Requirement (FR):** Hành vi hoặc chức năng mà hệ thống/dự án bắt buộc phải thực hiện.
2. **Quality / Non-Functional Requirement (NFR):** Thuộc tính chất lượng (hiệu năng, bảo mật, khả năng mở rộng, độ tin cậy).
3. **Constraint (CON):** Ràng buộc không thể thương lượng (luật định, chuẩn ISO, ngân sách tối đa, ngôn ngữ Rust).
4. **Assumption (ASM):** Giả định được đưa ra trong điều kiện thiếu thông tin; bắt buộc phải có chủ sở hữu và kế hoạch xác minh.
5. **Risk (RSK):** Rủi ro tiềm ẩn đe dọa mục tiêu dự án, đi kèm kế hoạch ứng phó.

### 2.2. Thuộc tính bắt buộc của một Requirement
- `req_id`: Định danh duy nhất (ví dụ: `M1-DOM-003`).
- `title`: Tên yêu cầu ngắn gọn, rõ ràng.
- `statement`: Nội dung đặc tả chi tiết sử dụng từ khóa chuẩn RFC 2119 (`MUST`, `SHOULD`, `MAY`).
- `category`: Phân loại yêu cầu.
- `priority`: `Critical`, `High`, `Medium`, `Low`.
- `source`: Nguồn gốc xuất phát (Intent ID, Stakeholder request, Regulatory document).
- `rationale`: Lý do tồn tại của yêu cầu.
- `verification_method`: Phương pháp kiểm chứng: `Inspection`, `Analysis`, `Demonstration`, `AutomatedTest`.
- `acceptance_criteria`: Danh sách các điều kiện cụ thể để coi là đạt.
- `lifecycle_status`: `Draft`, `Proposed`, `InReview`, `Approved`, `Superseded`, `Rejected`.

---

## 3. Architecture Decision Modeling (ADR Architecture)

Quyết định kiến trúc (Architecture Decision Record - ADR) là công cụ ghi lại các lựa chọn kỹ thuật và quản trị mang tính sống còn. Mọi quyết định trong PFS đều tuân thủ cấu trúc chuẩn hóa:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         ADR Anatomy & Lifecycle                             │
├─────────────────────────────────────────────────────────────────────────────┤
│  Header: ADR ID, Title, Status, Decision Date, Decision Authority          │
│  Context & Problem Statement: Bối cảnh, động lực kiến trúc, các thách thức │
│  Decision Drivers: Tiêu chí cốt lõi định hướng lựa chọn (Performance, Cost)│
│  Considered Options: Liệt kê tối thiểu 2-3 phương án khả thi               │
│  Decision Outcome: Lựa chọn được phê duyệt kèm Rationale chi tiết          │
│  Consequences: Hệ quả tích cực (Pros) và rủi ro/nợ kỹ thuật (Cons)         │
│  Traceability: Liên kết tới Requirements, Modules, Crates và Tests         │
│  Revisit Conditions: Điều kiện kích hoạt việc xem xét lại quyết định        │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 3.1. Các trạng thái quản trị của một ADR
> [!IMPORTANT]
> **Quy tắc phân định trạng thái thẩm quyền:**
> - `Proposed`: Đề xuất kỹ thuật do Kiến trúc sư hoặc AI Agent soạn thảo. Đang chờ xem xét.
> - `Accepted`: Quyết định ĐÃ ĐƯỢC PHÊ DUYỆT CHÍNH THỨC bởi Project Owner hoặc Hội đồng Kiến trúc.
> - `Deferred`: Quyết định được chủ động hoãn lại có chủ đích để thu thập thêm dữ liệu thực nghiệm.
> - `Open`: Vấn đề kiến trúc đang tranh luận, chưa thống nhất được phương án.
> - `Superseded`: Quyết định đã bị thay thế hoàn toàn bởi một ADR mới hơn.
> - `Rejected`: Phương án đề xuất bị bác bỏ sau khi thẩm định.
>
> **NGHIÊM CẤM:** AI Agent tuyệt đối không được tự ý đánh dấu một ADR là `Accepted` nếu chưa có biên bản phê duyệt chính thức từ Project Owner!

---

## 4. Conflict Resolution Protocol

Khi phát hiện sự xung đột giữa các yêu cầu (Requirement Conflict) hoặc bất đồng giữa các quyết định kiến trúc:

```mermaid
sequenceDiagram
    autonumber
    participant AG as Requirements Engine / Agent
    participant CR as Conflict Detector (Rust Core)
    participant REG as Requirement / ADR Registry
    participant QG as Quality Gate Engine
    participant PO as Project Owner (Human Authority)

    AG->>CR: Nạp danh sách yêu cầu và quan hệ phụ thuộc
    CR->>CR: Phát hiện xung đột (vd: Req_A đòi hỏi Stack X mâu thuẫn với Req_B đòi hỏi Stack Y)
    CR->>REG: Đánh dấu trạng thái 'Conflicted' trên cả 2 requirements
    CR->>QG: Gửi cảnh báo vi phạm; Khóa Quality Gate (Status: Blocked)
    CR->>PO: Tạo Conflict Arbitration Ticket kèm phân tích tác động (Impact Analysis)
    PO->>REG: Ban hành Architecture Decision (ADR) hòa giải và chọn phương án
    REG->>CR: Cập nhật quan hệ 'governs' và 'supersedes'
    CR->>QG: Giải phóng khóa Quality Gate sau khi xung đột được hòa giải
```

---

## 5. Automated Traceability Verification Engine

PFS Core tích hợp thuật toán kiểm tra tính toàn vẹn của chuỗi truy vết (Traceability Integrity Validator) chạy trên Rust:
1. **Orphan Requirement Check:** Mọi Requirement bắt buộc phải truy vết ngược về ít nhất một Intent hoặc Constraint hợp lệ.
2. **Unimplemented Requirement Check:** Mọi Requirement mức `Critical` hoặc `High` bắt buộc phải có ít nhất một Module/Artifact chịu trách nhiệm triển khai.
3. **Unverified Requirement Check:** Mọi Requirement bắt buộc phải có ít nhất một Test Specification hoặc Bằng chứng kiểm chứng (Evidence).
4. **Dangling Decision Check:** Mọi Quyết định (ADR) phải liên kết đến các Requirements chịu ảnh hưởng.
5. **Acyclic Graph Check:** Kiểm tra phát hiện chu trình (Cycle Detection) bằng thuật toán DFS/Tarjan; đảm bảo đồ thị là DAG 100%.
