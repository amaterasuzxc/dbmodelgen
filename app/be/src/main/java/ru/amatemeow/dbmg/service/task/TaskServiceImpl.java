package ru.amatemeow.dbmg.service.task;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import ru.amatemeow.dbmg.common.enumeration.TaskStatus;
import ru.amatemeow.dbmg.common.exception.DmbgNotFoundError;
import ru.amatemeow.dbmg.repository.task.TaskRepository;
import ru.amatemeow.dbmg.repository.task.entity.TaskEntity;
import ru.amatemeow.dbmg.service.task.mapper.TaskMapper;
import ru.amatemeow.dbmg.service.task.model.Task;
import ru.amatemeow.dbmg.service.task.model.TaskMetadata;

import java.util.UUID;

@Slf4j
@RequiredArgsConstructor
@Service
public class TaskServiceImpl implements TaskService {

  private final TaskMapper taskMapper;
  private final TaskRepository taskRepository;

  @Transactional
  @Override
  public Task pushTask(TaskMetadata metadata) {
    TaskEntity taskEntity = createTask(metadata);
    taskEntity = setTaskForProcessing(taskEntity);
    return taskMapper.mapToTask(taskEntity);
  }

  @Transactional
  @Override
  public Task getTask(UUID taskId) {
    return taskMapper.mapToTask(getTaskById(taskId));
  }

  @Transactional
  private TaskEntity createTask(TaskMetadata metadata) {
    TaskEntity taskEntity = TaskEntity.builder()
        .title(metadata.getTitle())
        .text(metadata.getText())
        .status(TaskStatus.CREATED)
        .build();
    return taskRepository.saveAndFlush(taskEntity);
  }

  @Transactional
  private TaskEntity getTaskById(UUID taskId) {
    return taskRepository.findById(taskId).orElseThrow(DmbgNotFoundError::new);
  }

  @Transactional
  private TaskEntity setTaskForProcessing(TaskEntity taskEntity) {
    taskEntity.setStatus(TaskStatus.PENDING);
    return taskRepository.saveAndFlush(taskEntity);
  }
}
