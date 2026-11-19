# PFS-M1-DOC-004 — PFS Product Architecture & Layered Engine

| Thuộc tính | Giá trị |
|---|---|
| Document ID | PFS-M1-DOC-004 |
| Document Title | PFS Product Architecture & Layered Engine Specification |
| Project | Project Foundation System (PFS) |
| Milestone | M1 — Documentation & Architecture Foundation |
| Version | 1.0.0 |
| Status | Proposed — Ready for Owner Review |
| Authority | Principal Systems Architect |
| Classification | Internal |
| Reference Architecture | Layered Architecture, Clean Hexagonal Architecture (Ports & Adapters) |
| Related Decisions | ADR-001, ADR-002, ADR-003, ADR-018 |

---

## 1. Product Architectural Vision

Kiến trúc sản phẩm của **Project Foundation System (PFS)** được tổ chức theo mô hình phân tầng chặt chẽ (Strict Layered Architecture) kết hợp với nguyên lý Kiến trúc Lục giác (Hexagonal Architecture / Ports & Adapters). Thiết kế này bảo đảm sự phân tách rạch ròi giữa giao diện người dùng, điều phối ứng dụng, quy tắc nghiệp vụ cốt lõi và hạ tầng tích hợp ngoại vi.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. EXPERIENCE LAYER                                                         │
│  - Project Workspace      - Foundation Viewer       - Approval Interface    │
│  - Intent Input Wizard    - Requirement Explorer    - Agent Monitoring      │
│  - CLI Interactive & JSON - Decision Review Board   - Quality Dashboard     │
├─────────────────────────────────────────────────────────────────────────────┤
│ 2. APPLICATION & ORCHESTRATION LAYER                                        │
│  - Project Intake Service - Agent Task Planner      - Quality Coordinator   │
│  - Workflow Orchestrator  - Approval Workflow       - Generation Pipeline   │
│  - Job Scheduler          - Governance Service      - Import/Export Service │
├─────────────────────────────────────────────────────────────────────────────┤
│ 3. DOMAIN & CORE SERVICES LAYER (Pure Rust Engine)                          │
│  - Project & Profile Aggregate   - Governance & Policy Aggregate            │
│  - Capability Registry Aggregate - Agent & Execution State Machine          │
│  - Foundation & Stage Aggregate  - Quality Gate & Evidence Aggregate        │
│  - Requirement & Decision DAG    - Template & Generation Engine             │
│  - Artifact & Merkle Provenance  - Version & Compatibility Engine           │
├─────────────────────────────────────────────────────────────────────────────┤
│ 4. INFRASTRUCTURE & ADAPTERS LAYER (Pluggable Ports)                        │
│  - AI Provider Gateway Adapters  - Filesystem & Sandbox Execution Adapter   │
│  - Dual Database Drivers         - OpenTelemetry & Structured Logger        │
│  - Event Bus & In-Memory Broker  - External Tool Registry Drivers           │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Layer 1 — Experience Layer (Giao diện và Trải nghiệm)

Experience Layer là tầng ngoài cùng, chịu trách nhiệm tương tác trực tiếp với người dùng (con người), hệ thống CI/CD hoặc các AI agents bên ngoài.

### 2.1. Thành phần chức năng
- **Project Workspace & Explorer:** Cho phép người dùng duyệt cây cấu trúc dự án, khám phá các artifacts, xem trạng thái tổng thể và điều hướng qua các giai đoạn vòng đời.
- **Intent Input Wizard:** Giao diện tiếp nhận Project Intent dưới dạng câu lệnh, biểu mẫu thông tin, tài liệu thô hoặc kịch bản phỏng vấn có định hướng.
- **Foundation & Artifact Viewer:** Trình trực quan hóa các tài liệu kiến trúc, sơ đồ tương tác, file cấu hình và gói Foundation Package được sinh ra.
- **Requirement & Decision Explorer:** Bảng điều khiển tra cứu yêu cầu, kiểm tra cây phân cấp (DAG) và theo dõi các quyết định kiến trúc kèm lý do (rationale).
- **Approval & Governance Interface:** Giao diện dành cho Project Owner và các cấp thẩm quyền thực hiện ký duyệt (L3–L5 Approval), xem xét ngoại lệ (Waivers) và phê duyệt các cổng chất lượng.
- **Agent & Execution Monitor:** Bảng theo dõi trực tiếp tiến độ thực thi của các tác vụ AI, chi phí token, thời gian chạy và các xung đột giữa các agents.
- **Quality Review Dashboard:** Bảng hiển thị kết quả kiểm định của Quality Engine, danh sách phát hiện (findings), tỷ lệ hoàn thành tiêu chuẩn và độ bao phủ bằng chứng.

### 2.2. Bất biến kiến trúc tầng giao diện
> [!IMPORTANT]
> **Experience Layer tuyệt đối KHÔNG chứa Business Logic cốt lõi.** Mọi hành động từ UI/CLI đều phải được chuyển hóa thành các **Command** hoặc **Query** có cấu trúc, gửi đến Application Layer để kiểm tra quyền hạn (Authorization) và xác thực tính hợp lệ (Validation). UI chỉ đóng vai trò trình diễn dữ liệu và tiếp nhận phản hồi từ người dùng.

---

## 3. Layer 2 — Application and Orchestration Layer

Tầng Ứng dụng và Điều phối đóng vai trò là nhạc trưởng (Conductor), kết nối các tương tác của người dùng với các quy tắc nghiệp vụ trong Domain Layer và điều phối các tác vụ bất đồng bộ dài hạn (long-running sagas).

### 3.1. Thành phần chức năng
- **Project Intake Service:** Tiếp nhận raw intent, điều phối việc chuẩn hóa dữ liệu, kích hoạt tác vụ phân tích ban đầu và khởi tạo Project Aggregate.
- **Foundation Workflow Orchestrator:** Điều phối việc chuyển đổi trạng thái qua 11 giai đoạn của Foundation Lifecycle, kiểm tra điều kiện đầu vào/đầu ra và kích hoạt các tasks tương ứng.
- **Task Planning & Agent Orchestrator:** Tiếp nhận mục tiêu từ workflow, phân rã mục tiêu thành các Task contracts cụ thể, định tuyến task đến Agent phù hợp và kiểm soát tài nguyên thực thi.
- **Governance & Approval Coordinator:** Quản lý quy trình phê duyệt đa cấp, tạm dừng workflow khi cần thẩm quyền con người (Human-in-the-Loop) và tiếp tục thực thi khi có chữ ký số hợp lệ.
- **Quality Coordinator:** Điều phối việc kích hoạt các bài kiểm tra tự động, tổng hợp kết quả kiểm thử và cung cấp báo cáo đánh giá cho Quality Gates.
- **Generation Coordinator:** Quản lý quy trình sinh mã và tài liệu, điều phối dry-run preview, phát hiện xung đột tệp tin và thực thi commit nguyên tử (Atomic Commit).

---

## 4. Layer 3 — Domain and Core Services Layer (Lõi Nghiệp vụ Thuần túy)

Domain Layer là trái tim của PFS, được hiện thực hoàn toàn bằng ngôn ngữ Rust mà không phụ thuộc vào bất kỳ framework web, cơ sở dữ liệu hay thư viện hạ tầng cụ thể nào.

### 4.1. Các Domain Aggregates cốt lõi
1. **Project & Profile Aggregate:** Quản lý vòng đời thực thể Project, Project Intent, phân loại domain, các thông số bối cảnh và ràng buộc tổng thể.
2. **Capability Model & Registry Aggregate:** Quản lý danh mục các năng lực của dự án, kiểm tra tính phụ thuộc, loại trừ xung đột và xác định tính áp dụng (Applicability).
3. **Foundation & Stage Aggregate:** Biểu diễn trạng thái của 11 giai đoạn vòng đời, bảo đảm các điều kiện chuyển đổi trạng thái (State Transition Guards).
4. **Requirement & Decision Aggregate:** Quản lý mạng lưới đồ thị có hướng (DAG) của Requirements, Assumptions, Constraints và Architecture Decisions.
5. **Governance & Policy Aggregate:** Mô hình hóa phân quyền L0–L5, nguyên tắc Least Privilege, Separation of Duties và chính sách phân định thẩm quyền.
6. **Artifact & Knowledge Aggregate:** Quản lý định danh toàn cầu (ULID), cây cấu trúc Merkle DAG, metadata phân loại dữ liệu và lịch sử phiên bản bất biến.
7. **Quality & Evidence Aggregate:** Định nghĩa các tiêu chí cổng chất lượng, lưu trữ bằng chứng kiểm chứng độc lập và phân loại findings (Defect, Risk, Exception).
8. **Generation Model & Template Engine:** Định nghĩa cấu trúc template trừu tượng, mô hình ánh xạ biến và cơ chế phát hiện xung đột tệp.

---

## 5. Layer 4 — Infrastructure and Adapters Layer

Tầng Hạ tầng hiện thực hóa các Ports do Domain và Application Layers định nghĩa, quản lý giao tiếp với thế giới bên ngoài thông qua các Adapters độc lập.

### 5.1. Danh mục Adapters
- **AI Provider Adapters:** Cung cấp kết nối đến OpenAI, Anthropic, Google Gemini và các máy chủ LLM nội bộ (vLLM, Ollama), chuẩn hóa các giao thức gọi hàm (Tool Calling) và structured outputs.
- **Database Adapters:** Cung cấp kết nối dữ liệu qua SQLx: SQLite (cho môi trường local/CLI) và PostgreSQL (cho môi trường máy chủ tập trung).
- **Filesystem & Staging Storage Adapter:** Quản lý thao tác đọc/ghi tệp an toàn, cô lập vùng nhớ tạm (Staging Directory) và tính toán mã băm SHA-256.
- **Execution Sandbox Adapter:** Cung cấp môi trường thực thi lệnh cô lập (WASM runtime hoặc isolated container) nhằm ngăn chặn mã độc thực thi trên máy chủ chủ quản.
- **Observability Adapter:** Tích hợp bộ thu thập dữ liệu viễn trắc (OpenTelemetry SDK), phân bổ trace context và xuất log có cấu trúc chuẩn JSON.
