package ru.amatemeow.dbmg.service.model;

import org.springframework.core.io.Resource;
import ru.amatemeow.dbmg.service.model.model.Model;

import java.util.UUID;

public interface ModelService {

  Model createModel(String jsonString);
  Model getModel(UUID modelId);
  Resource getModelAsDdl(UUID modelId);
}
