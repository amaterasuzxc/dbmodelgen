package ru.amatemeow.dbmg.service.model.mapper;

import org.mapstruct.Mapper;
import org.mapstruct.MappingConstants;
import ru.amatemeow.dbmg.repository.model.entity.ModelEntity;
import ru.amatemeow.dbmg.service.model.model.Model;

@Mapper(componentModel = MappingConstants.ComponentModel.SPRING)
public interface ModelMapper {

  Model mapToModel(ModelEntity entity);
}
