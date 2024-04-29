package ru.amatemeow.dbmg.service.model;

import ru.amatemeow.dbmg.repository.task.entity.TaskEntity;
import ru.amatemeow.dbmg.service.model.model.Model;

import java.util.UUID;

public interface ModelService {

  Model createModel(TaskEntity task, String jsonString);
  Model getModel(UUID modelId);
}
