package ru.amatemeow.dbmg.service.task.queue;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Component;
import ru.amatemeow.dbmg.common.exception.DbmgModelProcessingException;
import ru.amatemeow.dbmg.common.restclient.modelservice.ModelServiceClient;
import ru.amatemeow.dbmg.common.restclient.modelservice.dto.request.ProcessModelRequestDto;
import ru.amatemeow.dbmg.common.restclient.modelservice.dto.response.ProcessedModelDto;
import ru.amatemeow.dbmg.repository.task.entity.TaskEntity;
import ru.amatemeow.dbmg.service.model.ModelService;

import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

@Slf4j
@RequiredArgsConstructor
@Component
public class TextProcessingTask {

  private static final Lock LOCK = new ReentrantLock(true);

  private final ModelServiceClient modelServiceClient;
  private final ModelService modelService;

  void runTask(TaskEntity task) {
    try {
      LOCK.lockInterruptibly();
    } catch (InterruptedException ignored) {
      throw new DbmgModelProcessingException("Task wait for model processing was interrupted");
    }
    try {
      String modelResponse = sendProcessingRequestAndGetResult(task);
      modelService.createModel(task, modelResponse);
    } catch (Exception logged) {
      log.error("Problem occurred while processing task '{}': {}", task.getId(), logged.getMessage());
      throw new DbmgModelProcessingException(String.format("Task '%s' processing failed with following reason: ", task.getId()), logged.getCause());
    } finally {
      LOCK.unlock();
    }
  }

  private boolean isServiceReadyToAcceptTasks() {
    return HttpStatus.OK.isSameCodeAs(HttpStatus.valueOf(modelServiceClient.healthcheck().status()));
  }

  private String sendProcessingRequestAndGetResult(TaskEntity task) {
    if (!isServiceReadyToAcceptTasks()) {
      throw new DbmgModelProcessingException("AI service is not ready to accept new tasks");
    }
    ProcessModelRequestDto request = ProcessModelRequestDto.builder()
        .text(task.getText())
        .build();
    ResponseEntity<ProcessedModelDto> response = modelServiceClient.applyModelToText(request);
    if (response.getStatusCode().isSameCodeAs(HttpStatus.CONFLICT)) {
      throw new DbmgModelProcessingException("Another task is already being processed by AI service");
    } else {
      return response.getBody().getModel();
    }
  }
}
