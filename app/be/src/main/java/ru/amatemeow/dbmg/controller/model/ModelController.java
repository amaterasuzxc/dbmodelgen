package ru.amatemeow.dbmg.controller.model;

import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import ru.amatemeow.dbmg.common.constants.Urls;
import ru.amatemeow.dbmg.controller.model.dto.response.ModelResponseDto;

import java.util.UUID;

public interface ModelController {

  @GetMapping(path = Urls.MODEL_BY_ID_URL, produces = MediaType.APPLICATION_JSON_VALUE)
  ModelResponseDto getById(@PathVariable UUID id);
}
