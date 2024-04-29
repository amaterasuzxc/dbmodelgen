package ru.amatemeow.dbmg.common.restclient.modelservice;

import feign.Response;
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import ru.amatemeow.dbmg.common.restclient.modelservice.dto.request.ProcessModelRequestDto;
import ru.amatemeow.dbmg.common.restclient.modelservice.dto.response.ProcessedModelDto;
import ru.amatemeow.dbmg.config.ModelServiceClientConfiguration;

@FeignClient(
    name = "model-service-client",
    url = "${rest-client.model-service.url}",
    configuration = ModelServiceClientConfiguration.class)
public interface ModelServiceClient {

  @GetMapping("/healthcheck")
  Response healthcheck();

  @PostMapping("/apply")
  ResponseEntity<ProcessedModelDto> applyModelToText(ProcessModelRequestDto request);
}
