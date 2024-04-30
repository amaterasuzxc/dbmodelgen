package ru.amatemeow.dbmg.service.task.queue;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Component;
import ru.amatemeow.dbmg.common.enumeration.AiServiceStatus;
import ru.amatemeow.dbmg.common.exception.DbmgModelProcessingException;
import ru.amatemeow.dbmg.common.restclient.aiservice.AiServiceClient;
import ru.amatemeow.dbmg.common.restclient.aiservice.dto.request.ProcessModelRequestDto;
import ru.amatemeow.dbmg.common.restclient.aiservice.dto.response.ProcessedModelDto;
import ru.amatemeow.dbmg.repository.task.entity.TaskEntity;
import ru.amatemeow.dbmg.service.model.ModelService;

import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

@Slf4j
@RequiredArgsConstructor
@Component
public class TextProcessingTask {

  private static final Lock LOCK = new ReentrantLock(true);

  private final AiServiceClient aiServiceClient;
  private final ModelService modelService;

  void runTask(TaskEntity task) {
    try {
      LOCK.lockInterruptibly();
    } catch (InterruptedException ignored) {
      throw new DbmgModelProcessingException("Task wait for model processing was interrupted");
    }
    try {
      String modelResponse = sendProcessingRequestAndGetResult(task);
      modelService.populateModel(task, modelResponse);
    } catch (Exception logged) {
      log.error("Problem occurred while processing task '{}': {}", task.getId(), logged.getMessage());
      throw new DbmgModelProcessingException(String.format("Task '%s' processing failed with following reason: ", task.getId()), logged);
    } finally {
      LOCK.unlock();
    }
  }

  private boolean isServiceReadyToAcceptTasks() {
    return HttpStatus.OK.isSameCodeAs(HttpStatus.valueOf(aiServiceClient.healthcheck().status()));
  }

  private boolean isNewTaskAllowed() {
    return aiServiceClient.getServiceStatus().getStatus() == AiServiceStatus.AVAILABLE;
  }

  private String sendProcessingRequestAndGetResult(TaskEntity task) {
    if (!isServiceReadyToAcceptTasks()) {
      throw new DbmgModelProcessingException("AI service is not ready to accept new tasks");
    }
    if (!isNewTaskAllowed()) {
      throw new DbmgModelProcessingException("Another task is already being processed by AI service");
    }
    ProcessModelRequestDto request = ProcessModelRequestDto.builder()
        .text(task.getText())
        .build();
    ProcessedModelDto response = aiServiceClient.applyModelToText(request);
    return response.getModel();
  }
}
