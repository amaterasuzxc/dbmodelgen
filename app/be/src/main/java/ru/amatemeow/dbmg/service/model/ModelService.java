package ru.amatemeow.dbmg.service.model;

import ru.amatemeow.dbmg.repository.task.entity.TaskEntity;
import ru.amatemeow.dbmg.service.model.model.Model;

import java.util.UUID;

public interface ModelService {

  void populateModel(TaskEntity task, String jsonString);
  Model getModel(UUID modelId);
}
