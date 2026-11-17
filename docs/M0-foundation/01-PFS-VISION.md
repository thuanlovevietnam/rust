# PFS-M0-SPEC-001 — PFS Vision

**Document ID:** PFS-M0-SPEC-001  
**Document Type:** Product Vision Specification  
**Project:** Project Foundation System (PFS)  
**Version:** 1.1.0  
**Status:** Accepted  
**Target Milestone:** M0 — Foundation Methodology  
**Related Documents:** PFS-M0-SPEC-000, PFS-M0-SPEC-002, PFS-M0-SPEC-003, PFS-M0-SPEC-004  
**Amendment Reference:** PFS-M0-REVIEW-001 v1.0.0

---

## 1. Executive Vision

Project Foundation System (PFS) là một hệ thống giúp con người và AI xây dựng nền móng dự án một cách có phương pháp, có cấu trúc, có thể kiểm chứng, có thể tái lập và có thể phát triển lâu dài.

PFS không chỉ tạo tài liệu. PFS giúp chuyển một ý tưởng hoặc yêu cầu ban đầu thành một nền móng dự án có thể vận hành, bao gồm:

- Mục tiêu và phạm vi rõ ràng.
- Requirements có định danh và truy vết.
- Architecture phù hợp với bản chất dự án.
- Governance và decision authority.
- Documentation có cấu trúc.
- Agent system có quyền hạn được kiểm soát.
- Quality model và validation.
- Bootstrap và baseline có thể tái lập.

Tầm nhìn cốt lõi:

**Bất kỳ dự án nào, dù nhỏ hay phức tạp, đều có thể bắt đầu bằng một nền móng đúng đắn thay vì xây dựng tùy hứng rồi sửa chữa khi vấn đề đã xuất hiện.**

## 2. The Problem

Nhiều dự án bắt đầu từ ý tưởng, yêu cầu rời rạc hoặc một tập hợp chỉ dẫn chưa đầy đủ.

Những vấn đề thường gặp:

### 2.1. Requirements are fragmented

- Mục tiêu không rõ.
- Yêu cầu thay đổi nhưng không có lịch sử.
- Giả định bị nhầm với sự thật.
- Các yêu cầu mâu thuẫn không được phát hiện sớm.
- Không biết một quyết định kiến trúc phục vụ yêu cầu nào.

### 2.2. Architecture is premature or incomplete

- Chọn công nghệ trước khi hiểu bài toán.
- Thiết kế theo thói quen thay vì nhu cầu thực tế.
- Bỏ sót security, operations, data hoặc integration.
- Không có lý do rõ ràng cho các quyết định quan trọng.
- Kiến trúc không tương thích với năng lực và nguồn lực dự án.

### 2.3. Documentation is unreliable

- Tài liệu trùng lặp.
- Không rõ file nào là nguồn chuẩn.
- Quyết định mới không cập nhật vào tài liệu liên quan.
- Agent sử dụng thông tin cũ.
- Không thể xác định ai đã thay đổi và vì sao.

### 2.4. AI agents are powerful but insufficiently governed

- Agent tự suy diễn requirement.
- Agent thay đổi kiến trúc ngoài phạm vi.
- Nhiều agent tạo ra kết quả mâu thuẫn.
- Agent thực thi thao tác vượt quyền.
- Không có evidence để đánh giá kết quả.

### 2.5. Quality is checked too late

- Chỉ kiểm thử sau khi đã triển khai nhiều.
- Không có acceptance criteria rõ ràng.
- Không thể tái lập quá trình tạo dự án.
- Lỗi nền tảng lan sang nhiều module hoặc giai đoạn.

PFS được xây dựng để giải quyết những vấn đề này ngay từ giai đoạn hình thành dự án.

## 3. Vision Outcomes

PFS hướng đến sáu kết quả chính.

### 3.1. Clarity

Dự án có mục tiêu, phạm vi, requirements, assumptions, constraints và success criteria rõ ràng.

### 3.2. Architectural Fitness

Kiến trúc được lựa chọn dựa trên đặc điểm dự án, không áp đặt một kiến trúc duy nhất cho mọi loại dự án.

### 3.3. Governed Intelligence

AI có thể phân tích, đề xuất, soạn thảo và thực hiện các tác vụ được ủy quyền, nhưng không tự chiếm quyền quyết định của chủ dự án.

### 3.4. Verifiable Quality

Mỗi yêu cầu quan trọng có phương pháp kiểm chứng và evidence phù hợp.

### 3.5. Reproducibility

Một nền móng dự án có thể được kiểm tra, tái tạo hoặc cập nhật theo quy trình xác định, với khả năng phát hiện thay đổi ngoài dự kiến.

### 3.6. Sustainable Evolution

Dự án có thể thay đổi mà vẫn giữ được lịch sử quyết định, quan hệ phụ thuộc, tính tương thích và khả năng truy vết.

## 4. Universal Scope

PFS được định hướng là một hệ thống universal.

PFS không giới hạn vào:

- Software engineering.
- Web application.
- Mobile application.
- Desktop application.
- API hoặc SaaS.
- Một ngành kinh doanh cụ thể.
- Một quy trình quản lý dự án cụ thể.

PFS có thể hỗ trợ các loại dự án như:

- Sản phẩm phần mềm.
- Dự án nghiên cứu.
- Dự án kinh doanh.
- Hệ thống vận hành.
- Quy trình tổ chức.
- Dự án nội dung và sáng tạo.
- Dự án dữ liệu.
- Các sáng kiến cần requirements, governance, planning và validation.

Tuy nhiên, universal không có nghĩa mọi dự án phải có cùng một bộ tài liệu, cùng một architecture hoặc cùng một quy trình chi tiết.

PFS MUST xác định những thành phần nền tảng chung và cho phép tailoring theo loại dự án, risk, complexity, constraints và capabilities.

Chi tiết được định nghĩa trong `PFS-M0-SPEC-003`.

## 5. Product Philosophy

PFS được xây dựng dựa trên các nguyên tắc:

### 5.1. Requirements Before Architecture

Không thiết kế giải pháp chi tiết trước khi hiểu vấn đề, mục tiêu, constraints và yêu cầu.

### 5.2. Fit-for-Purpose, Not One-Size-Fits-All

Không áp đặt công nghệ, cấu trúc hoặc quy trình không cần thiết.

### 5.3. Human Authority, AI Assistance

Con người giữ quyền quyết định đối với những vấn đề cần thẩm quyền; AI hỗ trợ phân tích và thực thi trong phạm vi được cấp.

### 5.4. Evidence Over Confidence

Một kết luận có vẻ hợp lý không đồng nghĩa với kết luận đã được kiểm chứng.

### 5.5. Explicit Over Implicit

Quyết định, giả định, quyền hạn, trạng thái và ngoại lệ quan trọng phải được ghi nhận rõ ràng.

### 5.6. Safe Evolution

Thay đổi phải có kiểm soát, có thể đánh giá tác động và có phương án phục hồi phù hợp.

### 5.7. Progressive Detail

Không yêu cầu mọi dự án phải tạo ra toàn bộ tài liệu chi tiết ngay từ đầu. Mức độ chi tiết tăng theo complexity, risk và nhu cầu.

## 6. Hybrid Intelligence Vision

PFS sử dụng mô hình Hybrid:

1. **AI Reasoning:** Phân tích ngôn ngữ tự nhiên, tổng hợp thông tin, tìm mâu thuẫn, đề xuất giải pháp, tạo bản nháp và đánh giá các phương án.
2. **Deterministic Automation:** Thực hiện các thao tác có quy tắc rõ ràng như kiểm tra schema, validate metadata, kiểm tra traceability, phát hiện file conflict, quản lý version và tạo artifact theo manifest.

Hai thành phần bổ trợ cho nhau.

AI không được xem là nguồn xác thực duy nhất cho dữ liệu có thể kiểm tra bằng quy tắc xác định.

Deterministic automation không thay thế việc đánh giá ngữ nghĩa, mục tiêu hoặc bối cảnh cần reasoning.

Mô hình này được mô tả chi tiết trong `PFS-M0-SPEC-008`.

## 7. Technology Vision

### 7.1. PFS Core

Rust là công nghệ triển khai lõi PFS được lựa chọn.

Định hướng:

- Core logic.
- Deterministic processing.
- Validation.
- Artifact management.
- Generation orchestration.
- Security-sensitive operations.
- CLI và automation infrastructure khi được thiết kế ở milestone phù hợp.

### 7.2. AI Provider Independence

PFS MUST không phụ thuộc vào một AI provider duy nhất.

Việc tích hợp model hoặc agent provider phải thông qua adapter/contract được xác định ở milestone thiết kế tương ứng.

PFS không giả định mọi provider có cùng khả năng, context window, tool support, privacy policy hoặc execution behavior.

### 7.3. Generated Project Technology Independence

Rust là công nghệ xây dựng PFS, không phải yêu cầu bắt buộc cho các dự án được PFS hỗ trợ.

PFS MUST cho phép nền móng dự án sử dụng công nghệ phù hợp với yêu cầu của chính dự án đó.

## 8. Long-Term Direction

PFS có thể phát triển thành một nền tảng có khả năng:

- Tiếp nhận ý tưởng và yêu cầu từ nhiều nguồn.
- Xây dựng Project Profile.
- Phân tích và quản lý requirements.
- Đề xuất architecture phù hợp.
- Tạo và duy trì documentation.
- Quản lý AI agents, skills, workflows và policies.
- Kiểm tra tính nhất quán.
- Tự động hóa các thao tác an toàn.
- Đánh giá quality và acceptance.
- Theo dõi thay đổi và compatibility.
- Tái lập foundation từ một baseline có kiểm soát.

Đây là định hướng dài hạn, không phải cam kết mọi khả năng đều nằm trong M0.

## 9. Success Definition

PFS thành công khi tạo ra nền móng giúp giảm đáng kể:

- Sự mơ hồ trong yêu cầu.
- Quyết định thiếu căn cứ.
- Mâu thuẫn kiến trúc và tài liệu.
- Hành động AI vượt quyền.
- Công việc phải làm lại do sai từ nền tảng.
- Lỗi không thể truy nguyên.
- Chi phí thay đổi do thiếu quản trị.

PFS phải cải thiện khả năng:

- Hiểu đúng dự án.
- Chọn đúng phương án.
- Kiểm soát thực thi.
- Xác minh kết quả.
- Duy trì dự án theo thời gian.

Các chỉ số định lượng cụ thể phải được xác định theo project profile và quality model; không đặt ra một con số thành công chung thiếu cơ sở cho mọi loại dự án.

## 10. Non-Goals

PFS không đặt mục tiêu:

- Thay thế hoàn toàn Project Owner.
- Tự động đưa ra mọi quyết định kinh doanh hoặc kiến trúc.
- Buộc mọi dự án dùng cùng một stack.
- Đảm bảo AI không bao giờ mắc lỗi.
- Thay thế chuyên gia pháp lý, tài chính, y tế, bảo mật hoặc các chuyên môn có yêu cầu thẩm quyền.
- Cam kết mọi thao tác đều có thể rollback tuyệt đối.
- Tự động triển khai hoặc phát hành sản phẩm mà không có governance phù hợp.
- Tạo ra một hệ thống agent tự do thực thi lệnh không giới hạn.

## 11. Vision Constraints

Tầm nhìn PFS phải được hiện thực hóa trong các giới hạn:

- Quyền quyết định phải rõ ràng.
- Quyền thực thi phải giới hạn theo scope.
- Dữ liệu nhạy cảm phải được phân loại và bảo vệ.
- Tài liệu và artifact phải có provenance.
- Kết quả quan trọng phải có evidence.
- Tính tương thích phải được xem xét khi thay đổi.
- Mọi automation có rủi ro phải có cơ chế kiểm soát phù hợp.

## 12. Vision-Level Requirements

| ID | Requirement |
|---|---|
| PFS-VIS-001 | PFS MUST hỗ trợ nhiều loại dự án. |
| PFS-VIS-002 | PFS MUST cho phép tailoring theo project context. |
| PFS-VIS-003 | PFS MUST kết hợp AI reasoning và deterministic automation. |
| PFS-VIS-004 | PFS MUST không khóa vào một AI provider. |
| PFS-VIS-005 | PFS MUST phân biệt đề xuất của AI với quyết định đã được phê duyệt. |
| PFS-VIS-006 | PFS MUST hỗ trợ traceability giữa requirements, decisions, artifacts và verification. |
| PFS-VIS-007 | PFS MUST có quality và acceptance model dựa trên evidence. |
| PFS-VIS-008 | PFS MUST kiểm soát quyền thực thi của agent. |
| PFS-VIS-009 | PFS MUST hỗ trợ evolution có quản lý phiên bản và compatibility. |
| PFS-VIS-010 | PFS MUST không ép các dự án được hỗ trợ sử dụng Rust. |

## 13. Vision Governance

Tài liệu Vision xác định định hướng sản phẩm, không tự cấp quyền triển khai hoặc phê duyệt các quyết định kiến trúc chi tiết.

Các thay đổi làm thay đổi mục tiêu, phạm vi universal, nguyên tắc human authority hoặc provider independence MUST được trình Project Owner phê duyệt.

AI Agent MAY đề xuất sửa Vision nhưng MUST NOT tự thay đổi nội dung đã được phê duyệt.

---

**End of Document — PFS-M0-SPEC-001 v1.1.0**