package ru.amatemeow.dbmg.service.task;

import ru.amatemeow.dbmg.service.task.model.Task;
import ru.amatemeow.dbmg.service.task.model.TaskMetadata;

import java.util.UUID;

public interface TaskService {

  Task pushTask(TaskMetadata metadata);
  Task getTask(UUID taskId);
}
