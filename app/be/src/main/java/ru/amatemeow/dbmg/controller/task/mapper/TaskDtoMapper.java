package ru.amatemeow.dbmg.controller.task.mapper;

import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.MappingConstants;
import org.mapstruct.Mappings;
import ru.amatemeow.dbmg.controller.task.dto.request.TaskRequestDto;
import ru.amatemeow.dbmg.controller.task.dto.response.TaskResponseDto;
import ru.amatemeow.dbmg.service.task.model.Task;
import ru.amatemeow.dbmg.service.task.model.TaskMetadata;

@Mapper(componentModel = MappingConstants.ComponentModel.SPRING)
public interface TaskDtoMapper {

  @Mappings({
      @Mapping(source = "model.id", target = "modelId")
  })
  TaskResponseDto mapToTaskResponseDto(Task task);

  TaskMetadata mapToTaskMetadata(TaskRequestDto dto);
}
