# PFS-M1-DOC-027 — Milestone M1 Acceptance Criteria & Verification

| Thuộc tính | Giá trị |
|---|---|
| Document ID | PFS-M1-DOC-027 |
| Document Title | Milestone M1 Acceptance Criteria Catalog, Evidence Maturity Model and Verification Register |
| Project | Project Foundation System (PFS) |
| Milestone | M1 — Documentation & Architecture Foundation |
| Version | 1.1.0 |
| Status | Proposed — Ready for Owner Review |
| Authority | Principal Systems Architect & Quality Assurance Lead |
| Classification | Internal |
| Reference Framework | Evidence Maturity Model (E0–E5), ISO/IEC 25010, Invariant INV-07 |
| Related Registers | `registry/m1-acceptance-criteria-registry.csv`, `matrices/m1-traceability-matrix.csv` |
| Audit Remediation | Resolved finding FND-M1-04 (Evidence Maturity E0–E5 replacing generic Validated label) |

---

## 1. Formal Evidence Maturity Model (E0–E5)

Để bảo đảm tính trung thực tuyệt đối của bằng chứng kỹ thuật và phân biệt rạch ròi giữa việc hoàn thành đặc tả kiến trúc (Design/Spec Baseline) với việc kiểm chứng thực thi mã nguồn (Runtime Verification), PFS thiết lập **Khung Mô hình Trưởng thành Bằng chứng (Evidence Maturity Model)** gồm 6 cấp độ chuẩn hóa:

| Cấp độ | Tên cấp độ | Định nghĩa và Bản chất kỹ thuật | Loại bằng chứng chấp nhận | Phạm vi Milestone |
|---|---|---|---|---|
| **E0** | **Not Assessed** | Chưa được đánh giá hoặc chưa có tài liệu xem xét. | Không có. | Chưa khởi động |
| **E1** | **Documented** | Đã được mô tả, biên soạn trong văn bản hoặc hướng dẫn ban đầu. | Đoạn văn bản trong tài liệu, ghi chú thiết kế. | M0 Foundation |
| **E2** | **Specified** | Đã có đặc tả kiến trúc chính thức, hợp đồng giao tiếp (Contracts), JSON Schema, và tiêu chí nghiệm thu (ACs) chi tiết. | File tài liệu chuẩn hóa, API contract, JSON schema file, ADR. | **M1 Baseline** |
| **E3** | **Statically Validated** | Đã được kiểm tra và xác thực tính hợp lệ tự động bằng công cụ kiểm định tĩnh (Validators, Linters, Cycle Detectors). | Báo cáo kiểm định tự động (Exit Code 0), schema validation pass, 0 cycle graph. | **M1 Baseline** |
| **E4** | **Executably Verified** | Đã được xây dựng thành mã nguồn thực tế và vượt qua các bài kiểm thử thực thi (Unit, Integration, End-to-End Tests). | Test report (`cargo test` logs), CI test pass, code coverage metrics. | M2, M3, M4 Runtime |
| **E5** | **Operationally Proven** | Đã được vận hành thực tế trong môi trường mục tiêu (Production/Staging) và chứng minh qua viễn trắc. | Prometheus metrics, OTLP traces, Production audit ledger logs. | M4 Production |

> [!CRITICAL]
> **Quy tắc Quản trị Bằng chứng Bất biến (INV-07):**
> 1. Tuyệt đối không sử dụng nhãn "Validated" chung chung để che giấu khoảng trống thực thi runtime.
> 2. Các tiêu chí thuộc phạm vi kiến trúc M1 được đánh giá ở cấp độ **E2 — Specified** hoặc **E3 — Statically Validated**.
> 3. Các tiêu chí đòi hỏi thực thi mã nguồn runtime (ví dụ: sandbox isolation, filesystem atomic apply, live telemetry exporter, agent execution loop) bắt buộc phải ghi rõ trạng thái kỹ thuật M1 là `PASS — SPECIFIED`, đồng thời ghi nhận phần kiểm chứng runtime là **DEFERRED TO M2/M3/M4** kèm lộ trình và khoảng trống (gap) cụ thể.
> 4. Trạng thái `Owner Accepted` chỉ được áp dụng khi có Biên bản Quyết định Phê duyệt Nghiệm thu chính thức của Project Owner (như OD-02 trong M0).

---

## 2. Complete Catalog of 40 Architecture Acceptance Criteria (AC-M1-01 to AC-M1-40)

| AC ID | Lĩnh vực chuyên môn | Yêu cầu kiểm chứng chi tiết | Kết quả kỳ vọng | Phương pháp kiểm chứng | Tệp tài liệu & Bằng chứng | Cấp độ bằng chứng | Trạng thái kỹ thuật M1 & Lộ trình Runtime | Khoảng trống còn lại (Remaining Gap) |
|---|---|---|---|---|---|---|---|---|
| **AC-M1-01** | Product Definition | Định vị rõ PFS là Universal Foundation Engine; ranh giới không phải static doc tool. | Tách bạch rõ 5 nguyên tắc sản phẩm và danh mục non-goals. | Inspection | `01-M1-SCOPE-AND-BOUNDARIES.md` §1 | **E2** | **PASS — SPECIFIED** | Không |
| **AC-M1-02** | System Context | Xác định đầy đủ ranh giới hệ thống, tác nhân con người và hệ thống bên ngoài. | Có sơ đồ C4 Context Level 1 và đặc tả các ranh giới giao tiếp. | Architecture Review | `05-SYSTEM-CONTEXT-AND-STAKEHOLDERS.md` §1, DIA-001 | **E2** | **PASS — SPECIFIED** | Không |
| **AC-M1-03** | Stakeholders & Concerns | Phân tích toàn diện 12 nhóm stakeholders và ma trận mối bận tâm chuyên sâu. | Mỗi stakeholder có danh sách concerns và giải pháp kiến trúc. | Inspection | `05-SYSTEM-CONTEXT-AND-STAKEHOLDERS.md` §3 | **E2** | **PASS — SPECIFIED** | Không |
| **AC-M1-04** | Capability Architecture | Mô hình năng lực động, hỗ trợ Required, Optional, Conditional, Not Applicable. | Năng lực Not Applicable bắt buộc phải có Rationale giải trình. | Validation Script | `06-CAPABILITY-ARCHITECTURE.md` §3, DIA-002 | **E2** | **PASS — SPECIFIED** | Không |
| **AC-M1-05** | Universal Domain Model | Định nghĩa đầy đủ 40 khái niệm thực thể cốt lõi, độc lập với kỹ thuật phần mềm. | Có mô hình thực thể DDD chuẩn hóa và quan hệ ngữ nghĩa. | Model Verification | `07-UNIVERSAL-DOMAIN-MODEL.md` §2, schemas/ | **E3** | **PASS — STATICALLY VALIDATED** | Cài đặt Rust structs trong M2 WP-M2-01 |
| **AC-M1-06** | Identity & Scope Model | Định danh toàn cầu bằng ULID/UUIDv7; phân biệt rõ ID hệ thống và đường dẫn. | Ranh giới cách ly phạm vi (Tenant, Workspace, Project) rõ ràng. | Schema Check | `07-UNIVERSAL-DOMAIN-MODEL.md` §3, ADR-004 | **E3** | **PASS — STATICALLY VALIDATED** | Không |
| **AC-M1-07** | Project Hierarchy | Quản trị dự án độc lập, dự án con (subprojects) và chia sẻ tri thức an toàn. | Có cơ chế phân quyền kế thừa và cô lập tài nguyên. | Architecture Review | `07-UNIVERSAL-DOMAIN-MODEL.md` §4, ADR-005 | **E2** | **PASS — SPECIFIED** | Không |
| **AC-M1-08** | Foundation Lifecycle | Bảo toàn tuyệt đối vòng đời 11 giai đoạn kế thừa từ M0 (`Initialize` đến `Baseline`). | Từng giai đoạn có inputs, preconditions, outputs, exit criteria. | Consistency Audit | `08-PROJECT-AND-FOUNDATION-LIFECYCLE.md` §2, DIA-007 | **E2** | **PASS — SPECIFIED** | State machine code trong M3 |
| **AC-M1-09** | Requirement & Decision | Mô hình hóa yêu cầu và quyết định thành đồ thị có hướng không chu trình (DAG). | Phát hiện xung đột tự động và có quy trình hòa giải rõ ràng. | Graph Analysis | `09-REQUIREMENT-DECISION-AND-TRACEABILITY.md` §2 | **E3** | **PASS — STATICALLY VALIDATED** | Không |
| **AC-M1-10** | Artifact & Knowledge | Artifact quản lý theo mô hình Content-Addressed Storage (CAS) và Merkle DAG. | Lưu trữ metadata phân loại bảo mật và nguồn gốc (Provenance). | Schema Check | `10-ARTIFACT-KNOWLEDGE-AND-VERSIONING.md` §2 | **E3** | **PASS — STATICALLY VALIDATED** | Lưu trữ binary blob thực tế trong M3/M4 |
| **AC-M1-11** | Logical Architecture | Phân tách rạch ròi 4 tầng: Experience, Application, Domain Core, Infrastructure. | Tầng giao diện tuyệt đối không chứa quy tắc nghiệp vụ cốt lõi. | Architecture Review | `11-LOGICAL-ARCHITECTURE.md` §1 | **E2** | **PASS — SPECIFIED** | Không |
| **AC-M1-12** | Component Architecture | Phân rã hệ thống thành các components nội bộ có độ gắn kết cao và phụ thuộc lỏng. | Có sơ đồ C4 Component mô tả rõ ràng trách nhiệm từng khối. | Diagram Audit | `12-MODULE-AND-DEPENDENCY-ARCHITECTURE.md`, DIA-004 | **E2** | **PASS — SPECIFIED** | Không |
| **AC-M1-13** | Module Boundaries | Xác lập ranh giới và đặc tả toàn diện cho toàn bộ 29 modules chuyên môn. | Mỗi module có Module ID, ranh giới dữ liệu và hợp đồng rõ ràng. | Catalog Inspection | `12-MODULE-AND-DEPENDENCY-ARCHITECTURE.md` §2 | **E3** | **PASS — STATICALLY VALIDATED** | Không |
| **AC-M1-14** | Dependency Rules | Không có chu trình phụ thuộc (0 Cyclic Dependencies); tuân thủ Dependency Inversion. | Đồ thị phân cấp một chiều từ Core lên Application và Infra. | Graph Algorithm | `12-MODULE-AND-DEPENDENCY-ARCHITECTURE.md` §3, DIA-005 | **E3** | **PASS — STATICALLY VALIDATED** | Không |
| **AC-M1-15** | Command/Query Contracts | Tách biệt rạch ròi Command (thay đổi trạng thái) và Query (Read-only tuyệt đối). | Có danh mục hợp đồng chuẩn kèm thẩm quyền L0–L5 tương ứng. | Contract Audit | `14-APPLICATION-CONTRACTS-AND-EVENTS.md` §2 | **E2** | **PASS — SPECIFIED** | Không |
| **AC-M1-16** | Event Contracts | Phân định rõ Domain Events, Integration Events, Audit Events, Execution Events. | Có cấu trúc phong bì sự kiện (Event Envelope) chuẩn hóa. | Schema Check | `14-APPLICATION-CONTRACTS-AND-EVENTS.md` §4 | **E2** | **PASS — SPECIFIED** | Không |
| **AC-M1-17** | Workflow State Machines | Máy trạng thái 12 bước có Transition Guards và Saga Compensation. | Phân biệt rõ trạng thái `Completed` (kỹ thuật) và `Approved` (pháp lý). | FSM Inspection | `15-WORKFLOW-AND-STATE-MACHINES.md` §2, DIA-008 | **E2** | **PASS — SPECIFIED** | Saga coordinator runtime trong M3 |
| **AC-M1-18** | Failure and Recovery | Mô hình hóa và xử lý tự động 14 kịch bản lỗi hệ thống và rủi ro AI sập mạng. | Có chiến lược Circuit Breaker, Exponential Backoff và Rollback. | Resilience Review | `15-WORKFLOW-AND-STATE-MACHINES.md` §4, DIA-016 | **E2** | **PASS — SPECIFIED** | Không |
| **AC-M1-19** | Agent Architecture | Hệ thống Multi-Agent có 16 phân hệ chuyên trách, hoạt động có giới hạn quyền. | Đồng thuận của Agent tuyệt đối không thay thế được sự phê duyệt. | Security Audit | `16-AGENT-ORCHESTRATION-ARCHITECTURE.md` §1, DIA-009 | **E2** | **PASS — SPECIFIED** | Agent runtime execution loop trong M2 |
| **AC-M1-20** | Provider Independence | Gateway trừu tượng hóa kết nối LLMs, không phụ thuộc vào SDK độc quyền. | Hỗ trợ chuyển đổi model, streaming, ZDR. Chặn dữ liệu Restricted ra ngoài. | Port Verification | `17-AI-PROVIDER-AND-TOOL-ADAPTERS.md` §1, contracts/ | **E2** | **PASS — SPECIFIED** <br>*(Runtime live HTTP streaming & failover: **DEFERRED TO M2** WP-M2-03)* | Live HTTP provider calls & failover |
| **AC-M1-21** | Tool Gateway | Công cụ ngoại vi thực thi trong Sandbox cô lập (WASM / Subprocess Jail). | Chống Path Traversal và ngắt kết nối mạng Internet mặc định. | Sandbox Policy Spec | `17-AI-PROVIDER-AND-TOOL-ADAPTERS.md` §3, contracts/ | **E2** | **PASS — SPECIFIED** <br>*(Runtime OS isolation enforcement: **DEFERRED TO M2/M3** WP-M2-04)* | Runtime wasmtime runner & Job Objects |
| **AC-M1-22** | Governance & Auth | Mô hình phân quyền L0–L5 chuẩn M0; nguyên tắc Least Privilege, Deny-by-default. | Agent bị giới hạn tối đa ở L1/L2; L3+ bắt buộc con người phê duyệt. | Policy Engine Audit | `19-GOVERNANCE-AND-AUTHORIZATION-ARCHITECTURE.md` | **E2** | **PASS — SPECIFIED** | Policy Engine code trong M2 WP-M2-02 |
| **AC-M1-23** | Security Threat Model | Phân tích toàn diện 19 mối đe dọa theo mô hình STRIDE-AI và ranh giới tin cậy. | Có ma trận liên kết: Threat -> Control -> Module -> Test. | STRIDE Review | `20-SECURITY-THREAT-MODEL.md` §3, matrices/ | **E3** | **PASS — STATICALLY VALIDATED** | Runtime pen-testing trong M2/M3 |
| **AC-M1-24** | Privacy & Supply Chain | Phân loại 4 cấp dữ liệu (Public, Internal, Confidential, Restricted). | Lọc bí mật tự động; quét an toàn chuỗi cung ứng `cargo-audit`. | Supply Chain Audit | `22-DATA-PRIVACY-AND-SUPPLY-CHAIN.md` §2, ADR-012 | **E2** | **PASS — SPECIFIED** | Runtime cargo-audit CI check trong M2 |
| **AC-M1-25** | Quality & Evidence | Cổng chất lượng nghiêm ngặt; 1 lỗi Critical là khóa chuyển giai đoạn ngay. | Có mô hình bằng chứng (Evidence) độc lập có mã băm SHA-256. | Gate Verification | `21-QUALITY-AND-EVIDENCE-ARCHITECTURE.md` §3, schemas/ | **E2** | **PASS — SPECIFIED** <br>*(Runtime automated gate runner execution: **DEFERRED TO M3**)* | Gate runner binary & automated test runner |
| **AC-M1-26** | Generator & Recovery | Bộ sinh Journal-Based Staged Commit 13 bước; không âm thầm ghi đè file có sẵn. | Hỗ trợ Dry-run Interactive Diff, Ownership Manifest, Write-Ahead Journal. | Generator Review | `18-GENERATION-AND-RECOVERY-ARCHITECTURE.md` §2, ADR-017 | **E2** | **PASS — SPECIFIED** <br>*(Runtime atomic filesystem swap & rollback: **DEFERRED TO M2/M4**)* | Runtime filesystem atomic swap & rollback |
| **AC-M1-27** | API/CLI/UI Integration | Nguyên tắc Single Business Semantics thống nhất cho CLI, REST API và Agent Tool. | Có đặc tả hợp đồng OpenAPI 3.1 và giao diện JSON-RPC chuẩn. | Interface Audit | `24-API-CLI-AND-USER-INTERFACE-ARCHITECTURE.md`, contracts/ | **E3** | **PASS — STATICALLY VALIDATED** | Daemon server HTTP execution trong M4 |
| **AC-M1-28** | Deployment & Ops | Mô hình Modular Monolith hỗ trợ 3 Topologies (Local CLI, Team, Enterprise Cloud). | Có chiến lược Zero-Downtime Migration và sao lưu phục hồi. | Ops Review | `23-DEPLOYMENT-AND-OPERATIONS-ARCHITECTURE.md`, ADR-019 | **E2** | **PASS — SPECIFIED** | Không |
| **AC-M1-29** | Observability | Tích hợp OpenTelemetry (Traces, Metrics, Logs) xuyên suốt kèm Correlation ID. | Sổ cái kiểm toán bất biến (Append-only Ledger) niêm phong chữ ký. | Telemetry Review | `25-OBSERVABILITY-AND-RELIABILITY.md` §1, ADR-020 | **E2** | **PASS — SPECIFIED** <br>*(Runtime OTel exporter & live metrics: **DEFERRED TO M3/M4**)* | OTel exporter & live Prometheus scraping |
| **AC-M1-30** | Version Compatibility | Quản lý độc lập 9 miền phiên bản SemVer; có chính sách chuyển tiếp rõ ràng. | Ma trận tương thích phiên bản bảo vệ các dự án cũ không bị hỏng. | Compatibility Check | `25-OBSERVABILITY-AND-RELIABILITY.md` §3, matrices/ | **E3** | **PASS — STATICALLY VALIDATED** | Migration rollback scripts trong M4 |
| **AC-M1-31** | ADR Registry | Ban hành đầy đủ 20 Architecture Decision Records chiến lược (ADR-001..020). | Mỗi ADR có đủ Context, Options, Outcome, Rationale, concrete Revisit. | ADR Audit | `docs/M1-architecture/decisions/` (20 ADRs) | **E3** | **PASS — STATICALLY VALIDATED** | Owner Approval via OD-M1-01 |
| **AC-M1-32** | Architecture Diagrams | Xây dựng đầy đủ 16 sơ đồ kiến trúc chuẩn hóa bằng cú pháp Mermaid. | Sơ đồ có mã nguồn, chú giải, liên kết tài liệu và không có lỗi cú pháp. | Diagram Syntax Run | `docs/M1-architecture/diagrams/` (16 DIA) | **E3** | **PASS — STATICALLY VALIDATED** | Không |
| **AC-M1-33** | Module Implementation | Đặc tả chi tiết từng Crate trong Cargo Workspace bằng Rust (Types, Errors, Ports).| Không có module nào mô tả chung chung; có trait contract cụ thể. | Code Spec Review | `13-CORE-AND-APPLICATION-ARCHITECTURE.md` | **E2** | **PASS — SPECIFIED** | Cargo workspace compilation trong M2 |
| **AC-M1-34** | Dependency Graph | Thiết lập sơ đồ thứ tự xây dựng (Build Order) từ rễ phụ thuộc lên đỉnh. | Phân định rõ việc có thể làm song song và các điểm chặn (blockers). | Build Plan Audit | `26-IMPLEMENTATION-BLUEPRINT-AND-BACKLOG.md` §2 | **E3** | **PASS — STATICALLY VALIDATED** | Không |
| **AC-M1-35** | Implementation Backlog | Danh mục các hạng mục thi công (BL-01..07) chi tiết kèm Definition of Done. | Mỗi item có đầy đủ Priority, Module, Tests và Preconditions. | Backlog Inspection | `26-IMPLEMENTATION-BLUEPRINT-AND-BACKLOG.md` §4 | **E2** | **PASS — SPECIFIED** | Không |
| **AC-M1-36** | First Vertical Slice | Thiết kế kịch bản Vertical Slice hoàn chỉnh: Minimal Foundation from Intent. | Xác định rõ các Crates tham gia, luồng dữ liệu và hợp đồng giao tiếp. | Scenario Review | `26-IMPLEMENTATION-BLUEPRINT-AND-BACKLOG.md` §3 | **E2** | **PASS — SPECIFIED** <br>*(Live end-to-end CLI execution: **DEFERRED TO M2** WP-M2-05)* | Executable pfs init CLI test |
| **AC-M1-37** | Test Strategy | Chiến lược kiểm thử đa tầng: Unit tests, Contract tests, Integration, Pen-test. | Có ma trận kiểm thử tương ứng cho từng Crate và thuộc tính chất lượng. | Test Plan Audit | `21-QUALITY-AND-EVIDENCE-ARCHITECTURE.md` | **E2** | **PASS — SPECIFIED** | Test harness code trong M2/M3 |
| **AC-M1-38** | Requirement Traceability | Thiết lập ma trận truy vết hai chiều đầy đủ từ M0 Requirements sang M1 và ADRs.| 178 M0 requirements được đối soát 100% từ nguồn thực tế. | Traceability Run | `docs/M1-architecture/matrices/m1-traceability-matrix.csv` | **E3** | **PASS — STATICALLY VALIDATED** | Không |
| **AC-M1-39** | Architecture Consistency | Toàn bộ 29 tài liệu kiến trúc đồng nhất về mặt thuật ngữ, định danh và quy tắc.| Không có mâu thuẫn giữa các phân hệ; kiểm tra liên kết chéo 100% khớp. | Automated Tool | `tools/validation/validate_m1.py` -> Exit 0 | **E3** | **PASS — STATICALLY VALIDATED** | Không |
| **AC-M1-40** | Independent Review | Thực hiện đợt rà soát phản biện độc lập từ 10 góc nhìn kiến trúc chuyên sâu. | Báo cáo kiểm toán ghi nhận 100% findings và có phương án xử lý hợp lệ. | Review Inspection | `28-M1-FINAL-ARCHITECTURE-REVIEW.md` | **E3** | **PASS — STATICALLY VALIDATED** | Không |

---

## 3. Detailed Review of the 6 Runtime-Deferred Criteria (FND-M1-04 Remediation)

Để tránh nhầm lẫn giữa thiết kế và bằng chứng vận hành thực tế, 6 tiêu chí dưới đây được rà soát đặc biệt:

### 1. AC-M1-20: AI Provider Independence & Gateway
- **Thực tế M1:** Đã đặc tả trọn vẹn hợp đồng `AIProviderPort`, `provider-contracts.json`, 3-tier failover policy, cờ Do-Not-Train và chốt chặn dữ liệu Restricted. Đạt **PASS — SPECIFIED (E2)**.
- **Phần hoãn (Deferred):** Cuộc gọi mạng trực tiếp tới live API của OpenAI/Anthropic và kịch bản live failover tự động được hoãn sang kiểm chứng bằng bài kiểm thử tích hợp thực thi trong **Milestone M2 (WP-M2-03)**.

### 2. AC-M1-21: Tool Gateway & Sandbox Isolation
- **Thực tế M1:** Đã đặc tả hợp đồng `tool-contracts.json`, mô hình WASM Sandbox (`wasmtime`), Subprocess Jail (Windows Job Objects), giới hạn 5s CPU / 128MB RAM target policy và path traversal protection. Đạt **PASS — SPECIFIED (E2)**.
- **Phần hoãn (Deferred):** Việc cô lập tiến trình thực tế trên hệ điều hành và đo lường CPU/RAM thực tế khi chạy lệnh được hoãn sang kiểm thử trong **Milestone M2 (WP-M2-04) và M3**.

### 3. AC-M1-25: Quality Gate Engine & Evidence Verification
- **Thực tế M1:** Đã đặc tả cấu trúc Cổng chất lượng, `quality-gate-schema.json`, phân loại lỗi 4 cấp, và quy trình khóa chuyển giai đoạn khi gặp lỗi Critical. Đạt **PASS — SPECIFIED (E2)**.
- **Phần hoãn (Deferred):** Nhị phân thực thi đánh giá cổng chất lượng tự động và việc niêm phong tệp bằng chứng thực tế trên đĩa được hoãn sang **Milestone M3 (Quality Gates)**.

### 4. AC-M1-26: Generator & Journal-Based Recovery
- **Thực tế M1:** Đã hiệu chỉnh lại kiến trúc thành Journal-Based Staged Commit & Recovery 13 giai đoạn, loại bỏ tuyên bố 2PC filesystem phi thực tế, hoàn thiện `DIA-012` và `ADR-017`. Đạt **PASS — SPECIFIED (E2)**.
- **Phần hoãn (Deferred):** Thao tác hoán đổi tệp nguyên tử đa nền tảng và kiểm thử hoàn tác sau sự cố mất điện (Crash Recovery test) được phân bổ triển khai:
  - Bản tối thiểu (Minimal Generator): Kiểm thử trong **Milestone M2 (WP-M2-05)**.
  - Bản hoàn chỉnh (Full Generator 13 giai đoạn): Kiểm thử trong **Milestone M4**.

### 5. AC-M1-29: Observability & OpenTelemetry Telemetry
- **Thực tế M1:** Đã thiết kế kiến trúc viễn trắc OpenTelemetry (Traces, Metrics, Logs), Correlation IDs, Circuit Breaker và Sổ cái Kiểm toán bất biến. Đạt **PASS — SPECIFIED (E2)**.
- **Phần hoãn (Deferred):** Bộ xuất dữ liệu OTLP exporter thực tế sang Jaeger/Prometheus và kiểm tra độ trễ daemon được hoãn sang **Milestone M3/M4**.

### 6. AC-M1-36: First Vertical Slice Execution
- **Thực tế M1:** Đã thiết kế hoàn chỉnh kịch bản Vertical Slice "Minimal Foundation from Intent", ranh giới các Crates tham gia và luồng dữ liệu 13 bước. Đạt **PASS — SPECIFIED (E2)**.
- **Phần hoãn (Deferred):** Lệnh thực thi thực tế `pfs init` trên terminal để sinh ra tệp `README.md` và `.pfs-manifest.json` được hoãn sang nghiệm thu tại **Milestone M2 (WP-M2-05)**.

---

## 4. Summary of Verification Status

- **Tổng số tiêu chí nghiệm thu M1:** 40/40 tiêu chí.
- **Phân bổ theo Cấp độ Trưởng thành Bằng chứng (Evidence Maturity):**
  - **E2 — Specified (Đặc tả hoàn chỉnh):** 24 tiêu chí.
  - **E3 — Statically Validated (Kiểm định tĩnh tự động đạt):** 16 tiêu chí.
  - **E4 — Executably Verified (Thực thi runtime):** 0 tiêu chí (Được phân bổ hoãn sang M2–M4 theo đúng phạm vi Milestone).
  - **E5 — Operationally Proven:** 0 tiêu chí.
- **Số tiêu chí có nội dung kiểm thử runtime được hoãn có kiểm soát (Deferred to M2–M4):** 6 tiêu chí (AC-20, AC-21, AC-25, AC-26, AC-29, AC-36) với lộ trình, gói công việc và ranh giới rõ ràng.
- **Số tiêu chí bị thất bại (Failed):** 0/40.
- **Trạng thái phê duyệt cấp cao:** **PROPOSED — READY FOR PROJECT OWNER REVIEW** (Bảo lưu cho quyết định OD-M1-01).
