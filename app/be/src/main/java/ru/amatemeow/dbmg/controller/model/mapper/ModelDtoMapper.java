package ru.amatemeow.dbmg.controller.model.mapper;

import org.mapstruct.Mapper;
import org.mapstruct.MappingConstants;
import ru.amatemeow.dbmg.controller.model.dto.response.ModelResponseDto;
import ru.amatemeow.dbmg.service.model.model.Model;

@Mapper(componentModel = MappingConstants.ComponentModel.SPRING)
public interface ModelDtoMapper {

  ModelResponseDto mapToModelResponseDto(Model model);
}
