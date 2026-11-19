# PFS-M1-DOC-002 — Architecture Method, Standards and Quality Attributes

| Thuộc tính | Giá trị |
|---|---|
| Document ID | PFS-M1-DOC-002 |
| Document Title | Architecture Method, Standards Basis and Quality Attributes Specification |
| Project | Project Foundation System (PFS) |
| Milestone | M1 — Documentation & Architecture Foundation |
| Version | 1.0.0 |
| Status | Proposed — Ready for Owner Review |
| Authority | Principal Systems Architect |
| Classification | Internal |
| Reference Standards | ISO/IEC/IEEE 42010:2022, C4 Model, arc42, NIST SP 800-218 (SSDF), RFC 2119 |

---

## 1. Architectural Method & Methodological Framework

Thiết kế kiến trúc hệ thống PFS được xây dựng dựa trên sự kết hợp có chọn lọc của 4 chuẩn mực kiến trúc phần mềm hàng đầu thế giới, được tinh chỉnh chuyên biệt cho bài toán Universal Project Foundation Engine:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       PFS Unified Architectural Method                       │
├──────────────────────┬──────────────────────┬───────────────────────────────┤
│ ISO/IEC/IEEE 42010   │ C4 Model             │ arc42 & NIST SSDF             │
│ Systems & Software   │ Hierarchical Visual  │ Structured Documentation      │
│ Architecture Desc.   │ Architecture Model   │ & Secure Engineering Baseline │
│ - Stakeholders       │ - Level 1: Context   │ - Structural Views & Dec.     │
│ - Concerns           │ - Level 2: Container │ - Threat Modeling & Security  │
│ - Viewpoints & Views │ - Level 3: Component │ - Supply-Chain Integrity      │
│ - Architecture Rtn.  │ - Level 4: Code/Rust │ - Quality Scenarios & Gates   │
└──────────────────────┴──────────────────────┴───────────────────────────────┘
```

1. **ISO/IEC/IEEE 42010:2022 (Architecture Description):** Xác lập cơ sở định nghĩa tường minh về các Bên liên quan (Stakeholders), Mối quan tâm (Concerns), Góc nhìn kiến trúc (Viewpoints), Khung nhìn thực tế (Views) và Biên bản quyết định kiến trúc (Architecture Decision Records - ADRs).
2. **C4 Model (Simon Brown):** Sử dụng phương pháp mô hình hóa phân cấp 4 tầng:
   - **Context (L1):** Vị thế của PFS trong hệ sinh thái tương tác với người dùng, hệ thống bên ngoài và AI providers.
   - **Container (L2):** Phân rã thành các đơn vị thực thi độc lập (CLI, Core Daemon `pfsd`, Storage, Sidecar Sandbox).
   - **Component (L3):** Cấu trúc module và crates bên trong PFS Core (Intent Engine, Workflow Engine, Governance Engine,...).
   - **Code/Contracts (L4):** Đặc tả interfaces, traits, command/query schemas và state machines trong Rust.
3. **arc42 Documentation Framework:** Tổ chức cấu trúc tài liệu kiến trúc rõ ràng, logic, có khả năng tra cứu nhanh chóng và kết nối mạch lạc từ mục tiêu sản phẩm đến giải pháp kỹ thuật.
4. **NIST SP 800-218 (Secure Software Development Framework - SSDF):** Tích hợp an ninh ngay từ thiết kế kiến trúc (Security-by-Design), định nghĩa mô hình đe dọa (Threat Modeling), kiểm soát chuỗi cung ứng (Software Supply Chain Security) và lưu vết kiểm toán bất biến.

---

## 2. Stakeholders and Architectural Concerns

Bảng dưới đây xác định ma trận các bên liên quan và mối quan tâm cốt lõi được hệ thống kiến trúc PFS trực tiếp giải quyết:

| Stakeholder Role | Đại diện điển hình | Mối quan tâm kiến trúc chính (Concerns) | Khung nhìn giải quyết |
|---|---|---|---|
| **Project Owner** | Nhà đầu tư, Founder, Trưởng dự án | Kiểm soát mục tiêu, chi phí, quyền quyết định tối cao, tính minh bạch và tránh phụ thuộc nhà cung cấp (Vendor Lock-in). | Governance, Product Architecture, ADR-001, ADR-015 |
| **Project Operator** | Quản lý dự án, Scrum Master, Lead | Tiến độ tạo lập foundation, khả năng lặp lại, giám sát trạng thái workflow, quy trình phê duyệt trực quan. | Workflow Architecture, CLI/UI Architecture |
| **End User** | Developer, Researcher, Business Analyst | Tính tiện dụng, tốc độ phản hồi, thông điệp lỗi rõ ràng, không bị ghi đè dữ liệu bất ngờ, tài liệu chuẩn xác. | CLI/UI Architecture, Generator Safety |
| **Principal Systems Architect** | Kiến trúc sư hệ thống trưởng | Tính nhất quán của mô hình miền, ranh giới module rõ ràng, không có cyclic dependency, khả năng mở rộng. | Universal Domain Model, Logical & Module Architecture |
| **Agent Designer** | Kỹ sư thiết kế AI / Prompts | Hợp đồng giao tiếp rõ ràng giữa Agent và Core, cơ chế cung cấp ngữ cảnh (Context Injection), phân định vai trò Agent. | Multi-Agent Architecture, Provider Gateway |
| **Security Reviewer** | Chuyên gia an toàn thông tin | Ranh giới tin cậy (Trust boundaries), ngăn chặn Prompt Injection, cô lập công cụ (Sandbox), bảo vệ bí mật (Secret Redaction). | Security Architecture, Threat Model, ADR-013, ADR-014 |
| **Quality Reviewer** | QA Lead, Compliance Officer | Khả năng kiểm chứng bằng chứng (Evidence sufficiency), tiêu chí đóng mở cổng chất lượng (Quality Gates), truy vết yêu cầu. | Quality & Evidence Architecture, Traceability |
| **Rust Core Developer** | Kỹ sư phát triển PFS Core | Đặc tả Crate chi tiết, trait contracts tường minh, mô hình luồng & bất đồng bộ rõ ràng, chiến lược kiểm thử khả thi. | Core Architecture, Implementation Blueprint |
| **System Administrator** | DevOps / SRE Engineer | Triển khai gọn nhẹ, tài nguyên tối thiểu, cấu hình linh hoạt, khả năng sao lưu/phục hồi, tính năng giám sát (Observability). | Deployment & Operations, Observability |
| **External AI Provider** | OpenAI, Anthropic, Local vLLM | Chuẩn hóa định dạng request/response, kiểm soát rate limit, streaming phản hồi an toàn, quản lý chi phí token. | AI Provider Adapters, ADR-012 |

---

## 3. Comprehensive Quality Attributes Matrix

Hệ thống kiến trúc PFS được đo lường và đánh giá theo 19 thuộc tính chất lượng (Quality Attributes), mỗi thuộc tính đi kèm với kịch bản kiểm thử cụ thể (Scenario), phương pháp đo lường (Measurement) và chỉ tiêu chấp thuận (Acceptance Target):

| Thuộc tính chất lượng | Kịch bản kiến trúc (Scenario) | Phương pháp đo lường (Measurement) | Chỉ tiêu chấp thuận (Target) |
|---|---|---|---|
| **1. Correctness** | Tiếp nhận Project Intent và đối soát với kết quả sinh Foundation package. | Kiểm tra đối sánh ngữ nghĩa và ràng buộc logic bằng bộ validator xác định. | 100% quy tắc nghiệp vụ và ràng buộc quan hệ được thỏa mãn. |
| **2. Completeness** | Dự án trải qua toàn bộ 11 giai đoạn Foundation Lifecycle. | Kiểm tra danh mục deliverables bắt buộc của từng stage và capability. | Không thiếu bất kỳ artifact bắt buộc nào không có lý do được duyệt. |
| **3. Consistency** | Đối soát giữa yêu cầu, quyết định, sơ đồ kiến trúc và artifact mã nguồn. | Kiểm tra tính nhất quán thông qua ma trận truy vết hai chiều tự động. | 0 xung đột logic giữa requirement, decision và artifact. |
| **4. Security** | Tấn công giả lập Prompt Injection hoặc path traversal qua prompt/công cụ. | Đánh giá mức độ phát hiện và ngăn chặn tại Tool Sandbox và Input Sanitizer. | 100% hành vi truy cập vượt quyền hoặc path traversal bị chặn tại ranh giới L0–L5. |
| **5. Privacy** | Xử lý dữ liệu chứa API keys, mật khẩu, PII trong tài liệu dự án. | Tự động quét Secret Redaction trước khi dữ liệu rời khỏi Core sang LLM. | 0 bí mật hoặc dữ liệu phân loại Restricted bị rò rỉ sang AI Provider bên ngoài. |
| **6. Reliability** | Máy chủ hoặc tiến trình PFS bị ngắt đột ngột (SIGKILL) khi đang sinh artifact. | Khởi động lại hệ thống và thực hiện quy trình phục hồi (Crash Recovery). | Trạng thái hệ thống phục hồi về checkpoint an toàn gần nhất; 0 file bị hỏng hoặc ghi đè một phần. |
| **7. Availability** | AI Provider chính (vd: OpenAI) bị sập mạng hoặc trả về mã lỗi 503. | Kích hoạt cơ chế Circuit Breaker và tự động chuyển sang Secondary Model Adapter. | Hệ thống chuyển đổi nhà cung cấp dự phòng trong vòng < 2 giây không gián đoạn workflow. |
| **8. Performance** | Khởi chạy lệnh CLI kiểm tra tính hợp lệ và thẩm quyền của một Foundation Package. | Thời gian thực thi lệnh kiểm tra xác định (Deterministic Validation) trên Core Rust. | Thời gian phản hồi < 100ms đối với bộ dự án chứa 1.000 artifacts. |
| **9. Scalability** | Xử lý dự án quy mô doanh nghiệp với hơn 5.000 requirements và 100 capabilities. | Đo lường mức tiêu thụ bộ nhớ RAM và thời gian đánh giá đồ thị phụ thuộc (DAG). | Bộ nhớ RAM < 256MB; thuật toán topo giải quyết đồ thị < 500ms. |
| **10. Maintainability** | Bổ sung thêm một module nghiệp vụ mới hoặc thay đổi một trait contract. | Đo lường mức độ phụ thuộc lỏng (Loose Coupling) và tính cục bộ của các crates. | Việc thay đổi nội bộ module không làm ảnh hưởng đến các modules khác ngoài interface public. |
| **11. Extensibility** | Người dùng đăng ký một Domain Profile mới và một Capability mở rộng từ bên ngoài. | Đăng ký qua plugin configuration mà không cần biên dịch lại mã nguồn PFS Core. | Hoàn tất cấu hình và nhận diện capability mới trong < 1 phút qua Dynamic Registry. |
| **12. Portability** | Phân phối và thực thi nhị phân PFS Core trên các hệ điều hành khác nhau. | Chạy bộ test suite trên Linux (x86_64, aarch64), macOS (Apple Silicon), Windows (x64). | 100% tests vượt qua; nhị phân đơn lập không phụ thuộc thư viện runtime động bên ngoài. |
| **13. Interoperability** | Tích hợp PFS với các IDEs (Cursor/VS Code) và các công cụ CI/CD (GitHub Actions). | Giao tiếp thông qua chuẩn REST API, CLI JSON output và Headless Agent Tool Interface. | Tuân thủ 100% chuẩn OpenAPI 3.1 và JSON Schema Draft 2020-12. |
| **14. Reproducibility** | Chạy lại quy trình sinh Foundation từ cùng một tập đầu vào và cấu hình đã lưu. | Đối soát mã hash SHA-256 của toàn bộ cây artifacts được sinh ra. | Tính xác định 100% đối với phần sinh cấu trúc và template (Deterministic Core). |
| **15. Observability** | Điều tra nguyên nhân một tác vụ của Agent bị thất bại hoặc chạy quá thời gian. | Tra cứu Distributed Tracing qua OpenTelemetry Correlation ID và Span Context. | Truy xuất toàn bộ lịch sử ngữ cảnh, prompt, token usage và nhật ký lỗi trong 1 click. |
| **16. Recoverability** | Hoàn tác một thao tác sinh Foundation Package bị người dùng từ chối. | Thực thi lệnh Rollback dựa trên Snapshot và Change Manifest lưu trữ trong Transaction log. | Hoàn trả hệ thống tập tin về nguyên trạng 100% không để lại tệp rác. |
| **17. Auditability** | Thanh tra toàn bộ các quyết định phê duyệt và thay đổi cấu hình trong 12 tháng qua. | Xuất Append-only Audit Log và kiểm tra chữ ký số toàn vẹn của từng bản ghi. | Mọi thay đổi trạng thái đều có liên kết định danh: Who, When, Why, What Authority. |
| **18. Usability** | Người dùng mới tiếp nhận PFS và tạo lập Foundation đầu tiên từ câu tóm tắt ý tưởng. | Thời gian từ khi nhập Intent đến khi nhận được Foundation Draft đầu tiên kèm hướng dẫn. | < 5 phút với người dùng lần đầu thông qua hướng dẫn từng bước của CLI/UI wizard. |
| **19. Cost Efficiency** | Giám sát và tối ưu hóa chi phí token gọi LLM trong suốt vòng đời dự án. | Áp dụng Semantic Caching, tối ưu hóa Context Window và lựa chọn model theo tác vụ. | Giảm tối thiểu 40% chi phí token so với việc gửi toàn bộ ngữ cảnh thô không chọn lọc. |
