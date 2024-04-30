package ru.amatemeow.dbmg.service.task.queue;

import jakarta.annotation.Nullable;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.core.task.TaskRejectedException;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;
import ru.amatemeow.dbmg.repository.task.TaskRepository;

import java.util.Arrays;
import java.util.Set;
import java.util.UUID;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.TimeUnit;

@Slf4j
@RequiredArgsConstructor
@Component
public class TaskExecutionEnqueuer {

  private final Set<UUID> tasksInProgress = ConcurrentHashMap.newKeySet();

  private final AiTaskExecutor aiExecutor;
  private final TaskRepository taskRepository;

  @Transactional(readOnly = true)
  @Scheduled(
      fixedDelayString = "${dbmg.task.polling-interval:30}",
      timeUnit = TimeUnit.SECONDS)
  public void enqueueTasksForExecution() {
    log.info("Start polling for unfinished tasks");
    for (UUID taskId : taskRepository.findAllUnfinishedTaskIds()) {
      if (!tasksInProgress.contains(taskId) && !tryExecute(taskId)) {
        break;
      }
    }
    log.info("Polling for unfinished tasks completed.");
    log.info("Currently processing tasks: {}", Arrays.toString(tasksInProgress.toArray()));
  }

  private boolean tryExecute(UUID taskId) {
    tasksInProgress.add(taskId);
    CompletableFuture<Void> baseExecutionFuture = execute(taskId);
    if (baseExecutionFuture == null) {
      tasksInProgress.remove(taskId);
      return false;
    }
    baseExecutionFuture
        .thenRunAsync(
            () -> {
              log.info("Task '{}' execution finished without exception", taskId);
              tasksInProgress.remove(taskId);
            })
        .exceptionallyAsync(
            (Throwable t) -> {
              log.error("Task '{}' execution finished with exception", taskId, t);
              tasksInProgress.remove(taskId);
              return null;
            });
    return true;
  }

  @Nullable
  private CompletableFuture<Void> execute(UUID taskId) {
    try {
      CompletableFuture<Void> future = aiExecutor.execute(taskId);
      log.info("Enqueued task {} for execution", taskId);
      return future;
    } catch (TaskRejectedException e) {
      log.info("Can't enqueue task {} for execution. Queue is full", taskId);
      return null;
    } catch (Exception e) {
      log.error("Can't enqueue task {} for execution. Unknown error", taskId, e);
      return null;
    }
  }
}
