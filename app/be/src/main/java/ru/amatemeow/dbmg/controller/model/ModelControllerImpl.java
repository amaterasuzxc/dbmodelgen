package ru.amatemeow.dbmg.controller.model;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.core.io.Resource;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.RestController;
import ru.amatemeow.dbmg.controller.model.dto.response.ModelResponseDto;
import ru.amatemeow.dbmg.controller.model.mapper.ModelDtoMapper;
import ru.amatemeow.dbmg.service.model.ModelService;

import java.util.UUID;

@Slf4j
@RestController
@RequiredArgsConstructor
public class ModelControllerImpl implements ModelController {

  private final ModelService modelService;
  private final ModelDtoMapper modelDtoMapper;

  @Override
  public ModelResponseDto getById(UUID id) {
    return modelDtoMapper.mapToModelResponseDto(modelService.getModel(id));
  }

  @Override
  public ResponseEntity<Resource> getModelAsDDL(UUID id) {
    return ResponseEntity.ok(modelService.getModelAsDdl(id));
  }
}
