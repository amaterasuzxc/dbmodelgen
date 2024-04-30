package ru.amatemeow.dbmg.service.model;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.type.TypeFactory;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.util.StringUtils;
import ru.amatemeow.dbmg.common.exception.DbmgEmptyModelError;
import ru.amatemeow.dbmg.common.exception.DbmgInternalError;
import ru.amatemeow.dbmg.common.exception.DbmgNotFoundError;
import ru.amatemeow.dbmg.repository.model.ModelRepository;
import ru.amatemeow.dbmg.repository.model.entity.ModelEntity;
import ru.amatemeow.dbmg.repository.model.entity.info.LogicalEntityInfoAttribute;
import ru.amatemeow.dbmg.repository.model.entity.info.ModelInfoAttribute;
import ru.amatemeow.dbmg.repository.task.entity.TaskEntity;
import ru.amatemeow.dbmg.service.model.ddl.DdlService;
import ru.amatemeow.dbmg.service.model.mapper.ModelMapper;
import ru.amatemeow.dbmg.service.model.model.Model;

import java.util.List;
import java.util.UUID;

@Slf4j
@RequiredArgsConstructor
@Service
public class ModelServiceImpl implements ModelService {

  private final ModelMapper modelMapper;
  private final DdlService ddlService;
  private final ModelRepository modelRepository;

  @Transactional
  public void populateModel(TaskEntity task, String jsonString) {
    List<LogicalEntityInfoAttribute> entities = mapResponseStringToEntities(jsonString);
    ModelEntity model = task.getModel();
    ModelInfoAttribute modelInfo = model.getModelInfo();
    modelInfo.setTitle("Model-" + task.getTitle());
    modelInfo.setEntities(entities);
    model.setDdl(buildDdlForModel(model));
  }

  @Transactional
  @Override
  public Model getModel(UUID modelId) {
    return modelMapper.mapToModel(getModelById(modelId));
  }

  @Transactional
  private ModelEntity getModelById(UUID modelId) {
    return modelRepository.findById(modelId).orElseThrow(DbmgNotFoundError::new);
  }

  private String buildDdlForModel(ModelEntity model) {
    return ddlService.buildDdl(model);
  }

  private List<LogicalEntityInfoAttribute> mapResponseStringToEntities(String jsonString) {
    if (!StringUtils.hasText(jsonString)) {
      throw new DbmgEmptyModelError();
    }
    ObjectMapper mapper = new ObjectMapper();
    TypeFactory typeFactory = mapper.getTypeFactory();
    try {
      return mapper.readValue(jsonString, typeFactory.constructCollectionType(List.class, LogicalEntityInfoAttribute.class));
    } catch (JsonProcessingException ex) {
      throw new DbmgInternalError();
    }
  }
}
