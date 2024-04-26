package ru.amatemeow.dbmg.service.task.mapper;

import org.mapstruct.Mapper;
import org.mapstruct.MappingConstants;
import ru.amatemeow.dbmg.repository.task.entity.TaskEntity;
import ru.amatemeow.dbmg.service.task.model.Task;

@Mapper(componentModel = MappingConstants.ComponentModel.SPRING)
public interface TaskMapper {

  Task mapToTask(TaskEntity entity);
}
