package ru.amatemeow.dbmg.service.task.queue;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Component;
import ru.amatemeow.dbmg.common.constants.TaskExecutorNames;
import ru.amatemeow.dbmg.common.enumeration.TaskStatus;
import ru.amatemeow.dbmg.repository.model.entity.ModelEntity;
import ru.amatemeow.dbmg.repository.task.TaskRepository;
import ru.amatemeow.dbmg.repository.task.entity.TaskEntity;

import java.util.UUID;
import java.util.concurrent.CompletableFuture;

@Slf4j
@RequiredArgsConstructor
@Component
public class TaskExecutor {

  private final TaskRepository taskRepository;
  private final TextProcessingTask textProcessingTask;

  @Async(TaskExecutorNames.TASK_EXECUTOR)
  public CompletableFuture<Void> execute(UUID taskId) {

    log.info("Executing task {}", taskId);

    TaskEntity task = taskRepository.findById(taskId).get();
    task.setStatus(TaskStatus.RUNNING);
    task = taskRepository.saveAndFlush(task);

    try {
      ModelEntity model = textProcessingTask.runTask(task);
      task.setModel(model);
      model.setTask(task);
    } catch (Exception e) {
      task.setStatus(TaskStatus.FAILED);
      taskRepository.saveAndFlush(task);
      log.error("Pipeline {} execution failed with", taskId, e);
    }

    return CompletableFuture.completedFuture(null);
  }
}
