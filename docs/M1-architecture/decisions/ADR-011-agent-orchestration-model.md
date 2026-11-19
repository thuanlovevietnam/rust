# ADR-011 — Agent Orchestration Model: Multi-Agent Task Planning and Role-Based Routing

| Thuộc tính | Giá trị |
|---|---|
| ADR ID | ADR-011 |
| Title | Agent Orchestration Model: Multi-Agent Task Planning and Role-Based Routing |
| Status | Proposed — Ready for Owner Review |
| Decision Authority | Principal Systems Architect |
| Date | 2026-11-17 |
| Target Milestone | M1 — Documentation & Architecture Foundation |
| Related Modules | `MOD-14-AGT`, `MOD-15-ORC`, `MOD-13-TSK` |
| Related Requirements | M1-EXE-001, M1-DOM-001 |
| Related Diagrams | DIA-009-agent-task-sequence.mmd |
| Invariant Reference | INV-04, INV-06 |

---

## 1. Context & Problem Statement

Khi ứng dụng trí tuệ nhân tạo vào việc thiết kế nền tảng dự án, việc sử dụng duy nhất một "Agent toàn năng" (Monolithic Generalist Agent) với một prompt khổng lồ gặp nhiều thất bại:
- Cửa sổ ngữ cảnh bị quá tải, dẫn đến hiện tượng quên thông tin (Context Rot / Lost-in-the-Middle).
- Agent dễ bị ảo giác (Hallucination) khi phải đồng thời đóng vai Kiến trúc sư, Chuyên gia Bảo mật, Kỹ sư Yêu cầu và Chuyên gia Kiểm toán.
- Khó kiểm soát chi phí và không thể phân quyền độc lập cho từng vai trò.

Hệ thống đòi hỏi một mô hình điều phối đa Agent (Multi-Agent Orchestration) chuyên môn hóa sâu, hoạt động theo hợp đồng nhiệm vụ xác định.

## 2. Decision Drivers
- **Chuyên môn hóa vai trò (Role Specialization):** Mỗi Agent đảm nhiệm một vai trò hẹp với prompt chuyên biệt, bộ công cụ allowlist riêng và giới hạn quyền hạn L0–L2.
- **Lập kế hoạch phân rã nhiệm vụ (Task Planning & Decomposition):** Khả năng chia nhỏ mục tiêu của giai đoạn thành mạng lưới Task DAG thực thi song song.
- **Bất biến quản trị (Governance Invariant):** Sự đồng thuận giữa các Agents tuyệt đối KHÔNG thay thế được quyết định phê duyệt của Project Owner (INV-04).

## 3. Options Considered
- **Option A: Unconstrained Conversational Swarm (AutoGPT / ChatDev Style):**
  - Các agents tự do chat qua lại với nhau trong một phòng chat chung cho đến khi tự cho là xong.
  - *Nhược điểm:* Vô định, dễ rơi vào vòng lặp vô tận (Infinite Loops), chi phí token bùng nổ, không có ranh giới kiểm soát xác định.
- **Option B (Được chọn): Deterministic Supervisor & Task-Contract Routing:**
  - Lõi điều phối được lập trình bằng Rust (Crate `pfs-agent`), đóng vai trò Nhạc trưởng (Supervisor).
  - Nhiệm vụ được giao cho Agent thông qua **Task Contract** có cấu trúc nghiêm ngặt (Input Schema, Output Schema, Token Budget, Timeout).
  - Kết quả trả về bắt buộc phải vượt qua bộ xác thực JSON Schema trước khi chuyển giao cho Agent tiếp theo hoặc trình duyệt con người.

## 4. Decision & Rationale

**QUYẾT ĐỊNH:** Áp dụng **Option B: Deterministic Supervisor & Task-Contract Routing**.
- Hệ thống duy trì một danh mục các Agent Profiles chuẩn hóa: `RequirementsAnalyst`, `C4Architect`, `SecurityAuditor`, `TechWriter`.
- Khi hai Agent có kết luận mâu thuẫn (ví dụ: Architect đề xuất công nghệ X nhưng Security Auditor cảnh báo rủi ro lỗ hổng): Hệ thống ghi nhận một **Disagreement Record** kèm lập luận của hai bên và leo thang thành **Human Escalation Ticket** để con người (Project Owner/Lead) đưa ra quyết định cuối cùng. Không dùng cơ chế biểu quyết đa số giữa các AI models.

## 5. Consequences & Trade-offs
- *Tích cực:* Tiết kiệm 40% chi phí token nhờ ngữ cảnh tinh gọn; ngăn chặn hallucination; kiểm soát an ninh và tiến độ chính xác.
- *Thách thức:* Cần viết và duy trì nhiều Agent Profiles và prompt templates chuyên biệt thay vì một prompt chung chung.

## 6. Revisit Conditions

Mô hình điều phối Multi-Agent có giám sát sẽ được xem xét điều chỉnh khi và chỉ khi xuất hiện một trong các điều kiện đo lường được sau:
1. Khi tỷ lệ leo thang tranh chấp (Human Escalation Rate) vượt quá 20% tổng số tác vụ do các agent chuyên trách đưa ra các nhận định mâu thuẫn về cùng một tập tiêu chí thiết kế, đòi hỏi phải bổ sung một lớp Meta-Arbiter Agent có tri thức tổng hợp sâu trước khi gửi tới con người.
2. Khi các tiến bộ về mô hình nền tảng (Foundation Models) đạt đến khả năng suy luận tự kiểm chứng (Internal Formal Self-Verification) với tỷ lệ hallucination đã được chứng minh thực nghiệm < 0.01% trên các bài kiểm tra logic hình thức.
