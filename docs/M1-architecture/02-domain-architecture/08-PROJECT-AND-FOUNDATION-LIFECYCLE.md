# PFS-M1-DOC-008 — Project and Foundation Lifecycle Model

| Thuộc tính | Giá trị |
|---|---|
| Document ID | PFS-M1-DOC-008 |
| Document Title | Project and Foundation Lifecycle Model Specification |
| Project | Project Foundation System (PFS) |
| Milestone | M1 — Documentation & Architecture Foundation |
| Version | 1.0.0 |
| Status | Proposed — Ready for Owner Review |
| Authority | Principal Systems Architect |
| Classification | Internal |
| Reference Architecture | Finite State Machine (FSM), Long-Running Saga Pattern |
| Related Diagrams | DIA-007-foundation-lifecycle.mmd, DIA-008-workflow-state-machine.mmd |
| Related Decisions | ADR-009, ADR-015, ADR-016 |
| Parent Baseline | [PFS-M0-SPEC-004](file:///C:/Users/OK259/rust/docs/M0-foundation/04-FOUNDATION-METHODOLOGY.md) §3 |

---

## 1. Lifecycle Overview & Invariant Preservation

Milestone M1 bảo toàn tuyệt đối **Vòng đời Nền tảng 11 Giai đoạn (11-Stage Foundation Lifecycle)** đã được phê duyệt tại Milestone M0. Mô hình này bảo đảm rằng mọi dự án được PFS quản lý đều phải trải qua quá trình tuần tự, có kiểm soát, có bằng chứng kiểm chứng và có sự tham gia của thẩm quyền con người tại các nút thắt quyết định:

$$\mathbf{Initialize} \to \mathbf{Discover} \to \mathbf{Requirements} \to \mathbf{Architecture} \to \mathbf{Governance} \to \mathbf{Documentation} \to \mathbf{Agents} \to \mathbf{Quality} \to \mathbf{Bootstrap} \to \mathbf{Audit} \to \mathbf{Baseline}$$

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                   11-Stage Foundation Lifecycle Pipeline                    │
├─────────────────────────────────────────────────────────────────────────────┤
│  [01] Initialize  ──>  [02] Discover     ──>  [03] Requirements            │
│          │                     │                     │                      │
│  [04] Architecture<──  [05] Governance   <──  [06] Documentation            │
│          │                     │                     │                      │
│  [07] Agents      ──>  [08] Quality      ──>  [09] Bootstrap                │
│                                                      │                      │
│  [11] Baseline    <──  [10] Audit        <───────────┘                      │
└─────────────────────────────────────────────────────────────────────────────┘
```

> [!CRITICAL]
> **Quy tắc phân định trạng thái:** Hệ thống phân biệt rạch ròi giữa trạng thái **Completed (Hoàn thành kỹ thuật)** và **Approved (Chính thức phê duyệt)**. Một giai đoạn sau khi thực thi xong các tác vụ tự động chỉ đạt trạng thái `Ready for Review` hoặc `Completed`; giai đoạn đó TUYỆT ĐỐI CHƯA ĐƯỢC COI LÀ HOÀN TẤT nếu chưa có bản ghi phê duyệt `Approved` từ cấp thẩm quyền hợp lệ.

---

## 2. Comprehensive 11-Stage Detailed Specifications

Dưới đây là đặc tả chi tiết cho từng giai đoạn trong vòng đời 11 bước:

### Stage 1: Initialize Project (`STG-01-INIT`)
- **Mục đích:** Thiết lập định danh dự án, tiếp nhận Project Intent ban đầu, xác lập Project Owner và khởi tạo Project Profile.
- **Inputs:** Project Brief, Raw Intent text/document, Creator Identity.
- **Preconditions:** Creator có tài khoản hợp lệ trong Workspace.
- **Responsible Role:** Project Operator / Creator.
- **Allowed Actions:** Tạo Project, gán Project Owner, cấu hình phân loại bảo mật ban đầu.
- **Outputs:** Initial Project Profile, Project Intent Record, Initial Stakeholder Register.
- **Evidence:** Intent Schema Validation Report, Creator Signature.
- **Approval Requirement:** Project Owner xác nhận tiếp nhận dự án (L3).
- **Exit Criteria:** Project ID hợp lệ, Owner được chỉ định, Intent vượt qua kiểm tra cấu trúc.
- **Next Stage:** `STG-02-DISC`.

### Stage 2: Discover Context (`STG-02-DISC`)
- **Mục đích:** Khám phá bối cảnh dự án, phân tích thị trường/công nghệ/quy chuẩn, thu thập giả định và ràng buộc ban đầu.
- **Inputs:** Initial Project Profile, Domain Context documents, Industry References.
- **Preconditions:** Stage 1 đã được Approved.
- **Responsible Role:** Domain Specialist / Discovery Agent (L1).
- **Allowed Actions:** Phân tích tài liệu, đặt câu hỏi làm rõ (Interactive Clarification), ghi nhận Assumptions/Constraints.
- **Outputs:** Context Document, Assumption Registry, Constraint Registry, Initial Risk Log.
- **Evidence:** Context Completeness Checklist, Discovery Summary Report.
- **Approval Requirement:** Project Operator duyệt báo cáo bối cảnh (L2/L3).
- **Exit Criteria:** Toàn bộ giả định có chủ sở hữu; không còn câu hỏi làm rõ cấp thiết bị bỏ ngỏ.
- **Next Stage:** `STG-03-REQS`.

### Stage 3: Specify Requirements (`STG-03-REQS`)
- **Mục đích:** Mô hình hóa yêu cầu chi tiết (chức năng, phi chức năng, nghiệp vụ), xây dựng đồ thị quan hệ phụ thuộc (DAG).
- **Inputs:** Context Document, Capability Profile ban đầu.
- **Preconditions:** Stage 2 đã được Approved.
- **Responsible Role:** Requirements Engineer / Requirements Agent (L1/L2).
- **Allowed Actions:** Tạo, chỉnh sửa, phân loại yêu cầu; phát hiện xung đột yêu cầu; ánh xạ Capability.
- **Outputs:** Requirement Registry (Formal Schema), Requirement Traceability Graph, Conflict Matrix.
- **Evidence:** Requirement Ambiguity & Consistency Verification Report.
- **Approval Requirement:** Project Owner / Lead Architect ký duyệt Requirement Baseline (L3).
- **Exit Criteria:** 100% requirements có tiêu chí kiểm chứng (Verification Method); 0 xung đột chưa xử lý.
- **Next Stage:** `STG-04-ARCH`.

### Stage 4: Design Architecture (`STG-04-ARCH`)
- **Mục đích:** Thiết kế kiến trúc tổng thể, lựa chọn giải pháp kỹ thuật, phân rã module và ban hành các quyết định ADRs.
- **Inputs:** Requirement Baseline, Capability Profile, Architectural Constraints.
- **Preconditions:** Stage 3 đã được Approved.
- **Responsible Role:** Principal Systems Architect / Architecture Agent (L1/L2).
- **Allowed Actions:** Thiết lập sơ đồ kiến trúc C4, lập ADR Proposals, định nghĩa Module Boundaries.
- **Outputs:** Architecture Specification, System Context & Container Views, ADR Catalog.
- **Evidence:** Architecture Consistency Audit, Dependency Cycle Analysis Report (0 cycles).
- **Approval Requirement:** Principal Systems Architect và Project Owner phê duyệt ADRs chiến lược (L4).
- **Exit Criteria:** Toàn bộ yêu cầu kiến trúc có giải pháp tương ứng; ADRs được phân loại rõ ràng.
- **Next Stage:** `STG-05-GOVN`.

### Stage 5: Establish Governance (`STG-05-GOVN`)
- **Mục đích:** Thiết lập cơ chế quản trị, phân bổ quyền hạn L0–L5, quy định chính sách bảo mật và quy trình phê duyệt.
- **Inputs:** Stakeholder Register, Architecture Specification, Security Constraints.
- **Preconditions:** Stage 4 đã được Approved.
- **Responsible Role:** Governance Officer / Project Owner (L4/L5).
- **Allowed Actions:** Thiết lập Authority Matrix, phân vai trò cho thành viên và Agent, định nghĩa Approval Rules.
- **Outputs:** Governance Policy Specification, Authority Registry, Policy Engine Rulesets.
- **Evidence:** Separation of Duties (SoD) Audit Report, Least Privilege Verification.
- **Approval Requirement:** Project Owner ký duyệt chính thức mô hình quản trị (L5).
- **Exit Criteria:** 100% tài nguyên hệ thống có chính sách truy cập tường minh; không có quyền ẩn.
- **Next Stage:** `STG-06-DOCS`.

### Stage 6: Author Documentation (`STG-06-DOCS`)
- **Mục đích:** Soạn thảo bộ hồ sơ tài liệu nền tảng chuẩn hóa (Specs, Guides, Runbooks, Data Dictionaries).
- **Inputs:** Architecture Specification, Governance Policies, Domain Models.
- **Preconditions:** Stage 5 đã được Approved.
- **Responsible Role:** Technical Writer / Documentation Agent (L2).
- **Allowed Actions:** Sinh tài liệu từ mẫu (Templates), kiểm tra liên kết chéo (Cross-references).
- **Outputs:** Project Documentation Package, User Guides, Architecture Handbooks.
- **Evidence:** Markdown Linting Report, Broken Link Check Report, Glossary Consistency Report.
- **Approval Requirement:** Lead Architect duyệt nội dung tài liệu (L3).
- **Exit Criteria:** Không có broken links; 100% tài liệu có đầy đủ metadata và document ID duy nhất.
- **Next Stage:** `STG-07-AGNT`.

### Stage 7: Configure Agents (`STG-07-AGNT`)
- **Mục đích:** Thiết lập danh mục AI Agents, gắn kết vai trò, giới hạn công cụ (Tool Allowlist) và ngân sách token.
- **Inputs:** Task Breakdown, Governance Policy, Agent Capability Catalog.
- **Preconditions:** Stage 6 đã được Approved.
- **Responsible Role:** Agent Systems Engineer / Security Reviewer.
- **Allowed Actions:** Đăng ký Agent Profiles, thiết lập Sandbox Execution limits, định cấu hình Provider Gateway.
- **Outputs:** Agent Registry, Agent Permission Bindings, Tool Gateway Configurations.
- **Evidence:** Agent Security & Least Privilege Compliance Scan, Prompt Injection Defense Test.
- **Approval Requirement:** Security Officer phê duyệt danh sách công cụ và phân quyền của Agent (L4).
- **Exit Criteria:** 100% Agents bị hạn chế quyền L0–L2; các thao tác L3+ yêu cầu con người phê duyệt.
- **Next Stage:** `STG-08-QUAL`.

### Stage 8: Define Quality & Gates (`STG-08-QUAL`)
- **Mục đích:** Thiết lập hệ thống cổng kiểm định chất lượng (Quality Gates), tiêu chí chấp thuận và quy trình thu thập bằng chứng.
- **Inputs:** Requirement Acceptance Criteria, Architecture Constraints, Compliance Standards.
- **Preconditions:** Stage 7 đã được Approved.
- **Responsible Role:** QA Lead / Quality Engineer.
- **Allowed Actions:** Định nghĩa Gate Pass/Fail Criteria, cấu hình bài kiểm tra xác định (Deterministic Tests).
- **Outputs:** Quality Gate Manifest, Evidence Collection Rules, Verification Test Harness.
- **Evidence:** Quality Gate Self-Consistency Audit, Test Suite Dry-run Report.
- **Approval Requirement:** QA Lead và Project Owner ký duyệt cổng chất lượng (L4).
- **Exit Criteria:** 100% yêu cầu mức Critical có bài kiểm tra tự động và tiêu chuẩn bằng chứng tương ứng.
- **Next Stage:** `STG-09-BOOT`.

### Stage 9: Bootstrap & Generate (`STG-09-BOOT`)
- **Mục đích:** Thực thi việc sinh Foundation Package thực tế: tạo cấu trúc thư mục, sinh artifacts, mã nguồn khởi tạo.
- **Inputs:** Template Registry, Resolved Capability Set, Architecture Models.
- **Preconditions:** Stage 8 đã được Approved.
- **Responsible Role:** Foundation Generator Engine (Deterministic Rust Core) / Operator.
- **Allowed Actions:** Staged Generation, Dry-run Preview, Conflict Detection, Atomic Commit.
- **Outputs:** Generated Project Foundation Package, Ownership Manifest, Generation Operation Log.
- **Evidence:** Generation Dry-run Hash Diff, File Collision Check (0 collisions), SHA-256 Manifest.
- **Approval Requirement:** Project Operator duyệt Dry-run Preview trước khi Commit (L3).
- **Exit Criteria:** Toàn bộ artifacts sinh thành công; 0 file ngoài phạm vi bị tác động; commit nguyên tử hoàn tất.
- **Next Stage:** `STG-10-AUDT`.

### Stage 10: Audit & Verify (`STG-10-AUDT`)
- **Mục đích:** Tiến hành kiểm định độc lập toàn diện: chạy test suites, kiểm tra an ninh, đối soát ma trận truy vết.
- **Inputs:** Generated Foundation Package, Evidence Store, Quality Gates.
- **Preconditions:** Stage 9 đã được Approved.
- **Responsible Role:** Independent Quality Auditor / Security Reviewer.
- **Allowed Actions:** Chạy automated validators, rà soát mã nguồn, ghi nhận findings và waivers.
- **Outputs:** Independent Architecture Audit Report, Findings Log, Remediation Plan.
- **Evidence:** Automated Validation Tool Output (Exit Code 0), Security Penetration Scan.
- **Approval Requirement:** Independent Auditor ký xác nhận báo cáo kiểm toán (L4).
- **Exit Criteria:** 0 lỗi Critical/High tồn đọng; mọi ngoại lệ (Waivers) có chữ ký duyệt hợp lệ.
- **Next Stage:** `STG-11-BASE`.

### Stage 11: Establish Baseline (`STG-11-BASE`)
- **Mục đích:** Đóng gói Foundation Baseline chính thức, gắn thẻ phiên bản (v1.0.0), bàn giao cho đội ngũ triển khai.
- **Inputs:** Audited Foundation Package, Final Audit Report, Owner Decisions.
- **Preconditions:** Stage 10 đã được Approved; toàn bộ tiêu chuẩn nghiệm thu đều PASS.
- **Responsible Role:** Project Owner (L5 Authority).
- **Allowed Actions:** Gắn thẻ phiên bản Git tag bất biến, xuất gói lưu trữ (Distribution Archive), kích hoạt trạng thái Active.
- **Outputs:** Signed Foundation Baseline Release, Final Closure Report, Public Artifact Package.
- **Evidence:** Cryptographic Signature của Project Owner, Append-only Release Ledger Record.
- **Approval Requirement:** **PROJECT OWNER ACCEPTANCE APPROVAL RECORD (L5) — DUY NHẤT VÀ TỐI CAO.**
- **Exit Criteria:** Project Owner chính thức ký biên bản nghiệm thu; hệ thống sẵn sàng cho Milestone tiếp theo.
- **Next Stage:** Chuyển giao sang giai đoạn Implementation (Triển khai dự án thực tế).

---

## 3. Workflow Engine Architecture & State Machine

Hệ thống Workflow Engine trong PFS Core được xây dựng bằng Rust, quản lý vòng đời theo mô hình **Hierarchical Finite State Machine (HFSM)**:

```
    ┌──────────┐     trigger      ┌───────────┐     tasks ok     ┌───────────┐
    │  Draft   ├─────────────────>│   Ready   ├─────────────────>│  Running  │
    └──────────┘                  └─────┬─────┘                  └─────┬─────┘
                                        │                              │
                                        │ error                        │ tasks done
                                        ▼                              ▼
                                  ┌───────────┐                  ┌───────────┐
                                  │  Failed   │                  │ In Review │
                                  └─────┬─────┘                  └─────┬─────┘
                                        │                              │
                                        │ retry                        ├───────────────┐
                                        ▼                              │ approved      │ rejected
                                  ┌───────────┐                  ┌─────▼─────┐   ┌─────▼─────┐
                                  │ Suspended │                  │ Approved  │   │ Rejected  │
                                  └───────────┘                  └─────┬─────┘   └───────────┘
                                                                       │ next stage
                                                                       ▼
                                                                 ┌───────────┐
                                                                 │ Completed │
                                                                 └───────────┘
```

### 3.1. Phân loại 12 trạng thái Workflow chuẩn
1. `Draft`: Đang trong quá trình cấu hình hoặc khởi tạo dữ liệu ban đầu.
2. `Ready`: Đã thỏa mãn toàn bộ điều kiện đầu vào (Preconditions), sẵn sàng thực thi.
3. `Running`: Các tác vụ tự động hoặc tác vụ của Agent đang diễn ra.
4. `In Review`: Các tác vụ kỹ thuật đã xong, đang chờ thẩm quyền kiểm tra và đánh giá.
5. `Approved`: Được cấp thẩm quyền hợp lệ ký duyệt chính thức.
6. `Rejected`: Bị từ chối bởi người duyệt; yêu cầu chỉnh sửa và thực thi lại.
7. `Blocked`: Bị khóa do phát hiện lỗi nghiêm trọng (Critical Finding) hoặc xung đột chưa giải quyết.
8. `Suspended`: Bị tạm dừng bởi người vận hành (Operator Pause) để bảo trì hoặc kiểm tra.
9. `Failed`: Gặp sự cố kỹ thuật không thể tự phục hồi (Timeout, API sập, lỗi hệ thống).
10. `Cancelled`: Bị hủy bỏ dứt điểm bởi Project Owner.
11. `Completed`: Toàn bộ các công việc và phê duyệt của giai đoạn đã kết thúc hoàn hảo.
12. `Superseded`: Trạng thái cũ bị thay thế khi có một phiên bản Foundation mới được kích hoạt.

---

## 4. Failure Scenarios & Resilience Modeling

Kiến trúc Workflow của PFS mô hình hóa và xử lý tự động 14 kịch bản lỗi điển hình trong môi trường sản xuất:

| Mã lỗi | Kịch bản sự cố (Failure Scenario) | Cơ chế xử lý và Phục hồi (Resilience Strategy) |
|---|---|---|
| **FL-01** | AI Provider không khả dụng (503 / Network Timeout) | Exponential Backoff (3 lần); nếu không thành công, tự động kích hoạt Secondary Fallback Adapter qua Gateway. |
| **FL-02** | Công cụ thực thi trong Sandbox bị sập hoặc trả về mã lỗi | Đóng băng Task, ghi nhận lỗi vào Execution Record; không làm sập tiến trình PFS Core. |
| **FL-03** | Tiến trình Agent chạy quá thời gian (Task Timeout) | Ngắt kết nối Agent bằng CancellationToken; thu hồi quyền thuê Task (Lease); định tuyến lại cho Agent khác. |
| **FL-04** | Tiến trình máy chủ PFS bị tắt đột ngột (Crash / SIGKILL) | Khi khởi động lại, Saga Recovery Engine đọc Transaction Log và phục hồi trạng thái về Checkpoint hợp lệ gần nhất. |
| **FL-05** | Thực thi một phần (Partial Generation Failure) | Kích hoạt Compensation Saga; xóa bỏ toàn bộ tệp tin tạm trong Staging Directory; không commit ra workspace. |
| **FL-06** | Thực thi trùng lặp (Duplicate Execution Request) | Sử dụng Idempotency Key (ULID) lưu trong Database; từ chối thực thi lần 2 và trả về kết quả đang chạy. |
| **FL-07** | Kết quả cũ bị gửi muộn (Stale Result Delivery) | So sánh Version Token của Task; nếu Task đã được cấp phát lại (reassigned), từ chối và hủy bỏ kết quả cũ. |
| **FL-08** | Yêu cầu thay đổi khi workflow đang chạy | Chuyển trạng thái Workflow sang `Suspended`; thông báo cho Operator; đánh giá lại Dependency Graph trước khi tiếp tục. |
| **FL-09** | Quyết định kiến trúc bị thay thế (Superseded Decision) | Khóa các Tasks phụ thuộc vào quyết định cũ; yêu cầu đánh giá lại tác động (Impact Re-assessment). |
| **FL-10** | Xung đột tệp tin khi sinh Foundation (File Conflict) | So sánh mã băm SHA-256; nếu file đích bị thay đổi bởi người dùng, dừng commit và hiển thị Diff Interactive Preview. |
| **FL-11** | Thẩm quyền người dùng bị thu hồi giữa chừng | Policy Engine kiểm tra Token hiệu lực trước mỗi Command; từ chối thao tác ngay lập tức (HTTP 403 Forbidden). |
| **FL-12** | Cổng chất lượng bị thất bại (Quality Gate Failed) | Chuyển trạng thái sang `Blocked`; xuất danh sách Findings; ngăn cấm chuyển giai đoạn. |
| **FL-13** | Con người từ chối phê duyệt (Approval Rejected) | Ghi nhận lý do từ chối vào Audit Trail; hoàn trả Workflow về trạng thái `Ready` của giai đoạn tương ứng để sửa đổi. |
| **FL-14** | Tác vụ ngoài thành công nhưng giao dịch nội bộ lỗi | Áp dụng Outbox Pattern: hoàn tác tác vụ ngoài thông qua Compensation Webhook hoặc đánh dấu cần can thiệp thủ công. |
