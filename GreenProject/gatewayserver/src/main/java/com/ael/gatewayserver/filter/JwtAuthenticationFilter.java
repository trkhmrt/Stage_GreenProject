package com.ael.gatewayserver.filter;

import com.ael.gatewayserver.util.JwtUtil;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.cloud.gateway.filter.GatewayFilter;
import org.springframework.cloud.gateway.filter.factory.AbstractGatewayFilterFactory;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.server.reactive.ServerHttpRequest;
import org.springframework.stereotype.Component;
import org.springframework.web.server.ServerWebExchange;
import reactor.core.publisher.Mono;

@Component
public class JwtAuthenticationFilter extends AbstractGatewayFilterFactory<JwtAuthenticationFilter.Config> {

    private static final Logger logger = LoggerFactory.getLogger(JwtAuthenticationFilter.class);

    @Autowired
    private JwtUtil jwtUtil;

    @Override
    public GatewayFilter apply(Config config) {
        return (exchange, chain) -> {
            // Check if JwtUtil is properly injected
            if (jwtUtil == null) {
                logger.error("JwtUtil is null! Dependency injection failed.");
                return onError(exchange, "JWT service not available", HttpStatus.INTERNAL_SERVER_ERROR);
            }

            ServerHttpRequest request = exchange.getRequest();

            // Authorization header'ı kontrol et
            String authHeader = request.getHeaders().getFirst(HttpHeaders.AUTHORIZATION);

            if (authHeader == null || !authHeader.startsWith("Bearer ")) {
                logger.debug("No valid authorization header found");
                return onError(exchange, "No valid authorization header", HttpStatus.UNAUTHORIZED);
            }

            String token = authHeader.substring(7);
            logger.debug("Processing JWT token: {}", token.substring(0, Math.min(10, token.length())) + "...");

            try {
                // Token'ı doğrula
                if (!jwtUtil.validateToken(token)) {
                    logger.warn("Invalid token provided");
                    return onError(exchange, "Invalid token", HttpStatus.UNAUTHORIZED);
                }

                // Token'dan bilgileri çıkar
                String username = jwtUtil.extractUsername(token);
                String role = jwtUtil.extractRole(token);
                Integer customerId = jwtUtil.extractCustomerId(token);

                if (username == null || role == null || customerId == null) {
                    logger.warn("Failed to extract required information from token");
                    return onError(exchange, "Invalid token content", HttpStatus.UNAUTHORIZED);
                }

                logger.debug("Token validated successfully for user: {}, role: {}, customerId: {}", username, role, customerId);

                // Request header'larına bilgileri ekle
                ServerHttpRequest modifiedRequest = request.mutate()
                        .header("X-User-Name", username)
                        .header("X-User-Role", role)
                        .header("X-Customer-Id", customerId.toString())
                        .build();

                return chain.filter(exchange.mutate().request(modifiedRequest).build());

            } catch (Exception e) {
                logger.error("Token validation failed: {}", e.getMessage(), e);
                return onError(exchange, "Token validation failed", HttpStatus.UNAUTHORIZED);
            }
        };
    }

    private Mono<Void> onError(ServerWebExchange exchange, String err, HttpStatus httpStatus) {
        logger.error("JWT Authentication Error: {} - Status: {}", err, httpStatus);
        exchange.getResponse().setStatusCode(httpStatus);
        return exchange.getResponse().setComplete();
    }

    public static class Config {
        // Konfigürasyon ayarları buraya eklenebilir
    }
}