package ru.amatemeow.dbmg.service.model.model;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.core.io.Resource;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import ru.amatemeow.dbmg.common.exception.DmbgNotFoundError;
import ru.amatemeow.dbmg.repository.model.ModelRepository;
import ru.amatemeow.dbmg.repository.model.entity.ModelEntity;
import ru.amatemeow.dbmg.service.DdlService.DdlService;
import ru.amatemeow.dbmg.service.model.ModelService;
import ru.amatemeow.dbmg.service.model.mapper.ModelMapper;

import java.util.UUID;

@Slf4j
@RequiredArgsConstructor
@Service
public class ModelServiceImpl implements ModelService {

  private final ModelMapper modelMapper;
  private final DdlService ddlService;
  private final ModelRepository modelRepository;

  @Transactional
  public Model createModel(String jsonString) { // TODO
    return null;
  }

  @Transactional
  @Override
  public Model getModel(UUID modelId) {
    return modelMapper.mapToModel(getModelById(modelId));
  }

  @Transactional
  @Override
  public Resource getModelAsDdl(UUID modelId) {
    return null;
  }

  @Transactional
  private ModelEntity getModelById(UUID modelId) {
    return modelRepository.findById(modelId).orElseThrow(DmbgNotFoundError::new);
  }

  private Resource buildDdlForModel(UUID modelId) {
    ModelEntity modelEntity = getModelById(modelId);
    String ddl = ddlService.buildDdl(modelEntity);
    return null; // TODO
  }
}
