# PFS-M1-DOC-016 — Agent Orchestration & Task Execution Architecture

| Thuộc tính | Giá trị |
|---|---|
| Document ID | PFS-M1-DOC-016 |
| Document Title | Agent Orchestration and Task Execution Architecture Specification |
| Project | Project Foundation System (PFS) |
| Milestone | M1 — Documentation & Architecture Foundation |
| Version | 1.0.0 |
| Status | Proposed — Ready for Owner Review |
| Authority | Principal Systems Architect |
| Classification | Internal |
| Reference Architecture | Multi-Agent Coordination, Role-Based Autonomous Systems |
| Related Diagrams | DIA-009-agent-task-sequence.mmd |
| Related Decisions | ADR-011, ADR-012, ADR-013, ADR-014 |
| Invariant Reference | INV-02, INV-04, INV-05, INV-06 |

---

## 1. Multi-Agent Orchestration Philosophy

Trong **Project Foundation System (PFS)**, AI Agents không phải là những thực thể tự do (unconstrained chatbots) tự ý đưa ra quyết định hoặc tự kích hoạt các thay đổi hệ thống. Ngược lại, Agents trong PFS là các **Chuyên viên Nhiệm vụ Có Giới hạn (Bounded Task Specialists)** hoạt động dưới sự kiểm soát chặt chẽ của Core Engine bằng ngôn ngữ Rust.

PFS thiết lập 4 nguyên tắc bất biến cho hệ thống Multi-Agent:
1. **Agent Consensus Is NOT Owner Approval:** Sự đồng thuận giữa 10 hay 100 AI Agents không có giá trị thay thế quyền quyết định của con người (INV-04). Thẩm quyền phê duyệt chỉ thuộc về các vai trò được ủy quyền hợp lệ (L3–L5).
2. **Least Privilege & Role Isolation:** Mỗi Agent chỉ được cấp quyền tối thiểu cần thiết để hoàn thành nhiệm vụ cụ thể; mặc định bị giới hạn ở quyền Đọc (L0), Phân tích (L1) và Soạn thảo nháp (L2) (INV-06).
3. **Provider-Agnostic Operation:** Agent không bị ràng buộc vào mã nguồn hoặc API của bất kỳ nhà cung cấp LLM cụ thể nào; toàn bộ giao tiếp đi qua cổng Gateway chuẩn hóa (INV-05).
4. **Deterministic Validation of Agent Outputs:** Mọi kết quả do Agent đề xuất đều được kiểm tra tính hợp lệ bằng các bộ xác thực xác định (JSON Schema, Rust type checker, Linting tools) trước khi được đưa vào hệ thống.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      Multi-Agent Coordination Topology                      │
├─────────────────────────────────────────────────────────────────────────────┤
│  [Workflow Engine] ──> [Task Planner & Decomposer] ──> [Agent Router]       │
│                                                              │              │
│               ┌──────────────────┬───────────────────────────┘              │
│               ▼                  ▼                                          │
│       ┌───────────────┐  ┌───────────────┐                                  │
│       │ Architect Agt │  │ Discovery Agt │ (Specialized Task Agents)        │
│       └───────┬───────┘  └───────┬───────┘                                  │
│               │                  │                                          │
│               ▼                  ▼                                          │
│  [Context Builder & Secret Redactor] (Lọc bí mật & tối ưu context)          │
│               │                                                             │
│               ▼                                                             │
│  [Provider Gateway] ──> External LLMs (OpenAI, Anthropic, vLLM)             │
│               │                                                             │
│               ▼                                                             │
│  [Tool Gateway & Sandbox] ──> Isolated Execution (WASM / Docker)            │
│               │                                                             │
│               ▼                                                             │
│  [Result Validator & Conflict Resolver] ──> [Human Escalation if Needed]    │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Agent Architectural Subcomponents

Hệ thống điều phối Multi-Agent bao gồm 16 thành phần chuyên biệt:
1. **Agent Registry:** Quản lý danh mục các hồ sơ Agent Profiles, kỹ năng và lịch sử hoạt động.
2. **Agent Profile:** Bản đặc tả định danh, vai trò nghiệp vụ, giới hạn thẩm quyền (L0–L2) và ngân sách token.
3. **Agent Capability Catalog:** Danh mục các kỹ năng cụ thể mà Agent có thể thực thi.
4. **Task Planner:** Phân rã mục tiêu cấp cao của giai đoạn thành mạng lưới Task DAG có thể thực thi song song.
5. **Task Decomposer:** Chia nhỏ một task phức tạp thành các bước nguyên tử có hợp đồng rõ ràng.
6. **Agent Router:** Thuật toán định tuyến nhiệm vụ đến Agent phù hợp nhất dựa trên năng lực và chi phí.
7. **Agent Orchestrator:** Điều phối vòng đời thực thi, quản lý luồng thông điệp giữa các agents.
8. **Provider Gateway:** Trừu tượng hóa kết nối tới các nhà cung cấp mô hình AI bên ngoài.
9. **Tool Gateway:** Quản lý danh sách công cụ được phép (Allowlist) và chuyển tiếp lệnh gọi công cụ.
10. **Context Builder:** Xây dựng cửa sổ ngữ cảnh, trích xuất thông tin liên quan từ Knowledge Store.
11. **Permission Evaluator:** Kiểm tra phân quyền thời gian thực (L0–L5) trước mỗi hành động của Agent.
12. **Result Validator:** Đánh giá kết quả trả về của Agent đối chiếu với JSON Schema đầu ra mong muốn.
13. **Conflict Resolver:** Ghi nhận và xử lý khi các Agents có kết luận hoặc khuyến nghị trái ngược nhau.
14. **Execution Monitor:** Giám sát thời gian thực tiến độ, phát hiện tác vụ chạy quá giờ (Timeout).
15. **Cost Monitor:** Theo dõi và áp đặt trần chi phí token tiêu thụ của từng Agent và Task.
16. **Audit Recorder:** Ghi nhận nhật ký kiểm toán bất biến về mọi prompt, response và công cụ đã gọi.

---

## 3. Agent Lifecycle State Machine

Vòng đời của một Agent hoặc Phiên làm việc của Agent (Agent Session) tuân thủ 10 trạng thái chuẩn:

```
[Registered] ──> [Available] ──> [Assigned] ──> [Running] ──> [Waiting] ──> [Completed]
      │               │              │             │              │
      ▼               ▼              ▼             ▼              ▼
  [Disabled]      [Retired]     [Cancelled]     [Failed]     [TimedOut]
```

1. `Registered`: Agent Profile đã được cấu hình trong hệ thống nhưng chưa kích hoạt.
2. `Available`: Sẵn sàng tiếp nhận nhiệm vụ từ Task Router.
3. `Assigned`: Đã được gán một Task Contract cụ thể; đang chuẩn bị nạp ngữ cảnh.
4. `Running`: Đang suy luận (Inference) hoặc đang gọi công cụ trong Sandbox.
5. `Waiting`: Tạm dừng chờ phản hồi từ công cụ ngoại vi hoặc chờ phê duyệt của con người.
6. `Completed`: Tác vụ hoàn thành thành công và kết quả đã vượt qua bước kiểm định xác định.
7. `Failed`: Tác vụ thất bại do lỗi mô hình, lỗi công cụ hoặc vi phạm schema kết quả.
8. `Cancelled`: Bị hủy bỏ giữa chừng bởi người vận hành hoặc tín hiệu hủy bỏ của hệ thống.
9. `Disabled`: Bị vô hiệu hóa tạm thời do vượt hạn ngạch chi phí hoặc phát hiện bất thường an ninh.
10. `Retired`: Ngừng sử dụng vĩnh viễn (ví dụ: phiên bản prompt/model cũ lỗi thời).

---

## 4. Formal Agent Task Contract Specification

Mọi nhiệm vụ giao cho Agent bắt buộc phải được đóng gói trong một **Task Contract** có cấu trúc rõ ràng:

| Thuộc tính hợp đồng | Kiểu dữ liệu | Ý nghĩa và Ràng buộc |
|---|---|---|
| `task_id` | ULID | Định danh duy nhất toàn cầu của nhiệm vụ. |
| `project_scope` | ProjectId | Định danh dự án sở hữu (Cách ly phạm vi tuyệt đối). |
| `objective` | String | Mục tiêu nghiệp vụ ngắn gọn, rõ ràng mà Agent cần đạt được. |
| `assigned_role` | Enum | Vai trò chuyên biệt: `RequirementsAnalyst`, `C4Architect`, `SecurityAuditor`, `TechWriter`. |
| `allowed_tools` | Array<String> | Danh sách cho phép (Allowlist) các công cụ Agent được gọi (vd: `read_file`, `validate_schema`). |
| `permission_level`| AuthorityLevel| Mức phân quyền tối đa (mặc định: `L1_AnalyzePropose` hoặc `L2_DraftArtifacts`). |
| `context_sources` | Array<Uri> | Danh sách các tài liệu và tri thức được tiêm vào ngữ cảnh. |
| `output_schema` | Ref (Schema) | Lược đồ JSON Schema mà kết quả trả về bắt buộc phải tuân thủ nghiêm ngặt. |
| `token_budget` | Integer | Số lượng token tối đa được phép tiêu thụ cho task này. |
| `timeout_seconds` | Integer | Thời gian tối đa cho phép thực thi trước khi bị ngắt cưỡng bức (Timeout). |
| `retry_policy` | Object | Số lần thử lại tối đa (mặc định: 2 lần) và chiến lược backoff. |

---

## 5. Context Architecture & Data Privacy Controls

Kiến trúc quản lý ngữ cảnh (Context Architecture) của PFS bảo đảm tối ưu hóa độ chính xác và bảo vệ an toàn dữ liệu:
- **Secret Redaction Pipeline:** Trước khi ngữ cảnh rời khỏi máy chủ PFS sang bất kỳ AI Provider nào, dữ liệu bắt buộc phải đi qua bộ lọc làm sạch tự động (RegEx pattern matching + Entropy analysis) để che dấu toàn bộ API keys, passwords, chứng chỉ số và dữ liệu phân loại `Restricted`.
- **Context Relevance Scoring:** Sử dụng tìm kiếm ngữ nghĩa (BM25 + Semantic Embeddings) để chỉ trích xuất các phân đoạn tri thức có liên quan trực tiếp đến nhiệm vụ, tránh làm loãng ngữ cảnh và giảm 40% chi phí token.
- **Stale Context Detection:** So sánh mã băm của các tài liệu nguồn; nếu tài liệu trong ngữ cảnh đã bị cập nhật bởi một người dùng khác, Task lập tức bị hủy bỏ và tái nạp ngữ cảnh mới nhất.

---

## 6. Multi-Agent Conflict Arbitration Protocol

Khi hai hay nhiều Agents đưa ra các khuyến nghị kiến trúc hoặc phân tích mâu thuẫn nhau:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    Multi-Agent Conflict Arbitration Flow                    │
├─────────────────────────────────────────────────────────────────────────────┤
│ 1. Conflict Detection: Result Validator phát hiện 2 outputs mâu thuẫn logic │
│ 2. Disagreement Record: Hệ thống tạo bản ghi bất đồng, ghi nhận:            │
│    - Lập luận và bằng chứng của Agent A                                     │
│    - Lập luận và bằng chứng của Agent B                                     │
│    - Mức độ tin cậy và các giả định (Assumptions) của từng bên             │
│ 3. Automated Rebuttal Round: Cho phép Agent A và B phản biện chéo 1 lần duy │
│    nhất kèm yêu cầu trích dẫn tiêu chuẩn kỹ thuật (RFC/ISO)                │
│ 4. Deterministic Tie-Breaker: Nếu vẫn mâu thuẫn, chuyển giao cho:          │
│    HUMAN ESCALATION TICKET gửi trực tiếp tới Project Owner / Lead Architect │
│ 5. Binding Resolution: Con người ban hành ADR; ghi nhận vào Audit Ledger   │
└─────────────────────────────────────────────────────────────────────────────┘
```
