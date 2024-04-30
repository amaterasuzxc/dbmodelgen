package ru.amatemeow.dbmg.common.restclient.aiservice;

import feign.Response;
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import ru.amatemeow.dbmg.common.restclient.aiservice.dto.request.ProcessModelRequestDto;
import ru.amatemeow.dbmg.common.restclient.aiservice.dto.response.ProcessedModelDto;
import ru.amatemeow.dbmg.common.restclient.aiservice.dto.response.StatusResponseDto;
import ru.amatemeow.dbmg.config.restclient.AiServiceClientConfiguration;

@FeignClient(
    name = "ai-service-client",
    url = "${rest-client.ai-service.url}",
    configuration = AiServiceClientConfiguration.class)
public interface AiServiceClient {

  @GetMapping("/healthcheck")
  Response healthcheck();

  @GetMapping("/status")
  StatusResponseDto getServiceStatus();

  @PostMapping("/apply")
  ProcessedModelDto applyModelToText(ProcessModelRequestDto request);
}
