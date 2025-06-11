package com.ael.paymentservice.dto.response;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;

@Data
@Builder
@AllArgsConstructor
public class PaymentResponse {
    private String status;
    private String paymentStatus;
    private String conversationId;
    private String authCode;
    private String hostReference;
    private String responseCode;
    private String responseMessage;
}
