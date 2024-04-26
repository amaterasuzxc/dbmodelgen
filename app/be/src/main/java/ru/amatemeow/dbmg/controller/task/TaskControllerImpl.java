package ru.amatemeow.dbmg.controller.task;

import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.web.bind.annotation.RestController;
import ru.amatemeow.dbmg.controller.task.dto.request.TaskRequestDto;
import ru.amatemeow.dbmg.controller.task.dto.response.TaskResponseDto;
import ru.amatemeow.dbmg.controller.task.mapper.TaskDtoMapper;
import ru.amatemeow.dbmg.service.task.TaskService;
import ru.amatemeow.dbmg.service.task.model.Task;
import ru.amatemeow.dbmg.service.task.model.TaskMetadata;

import java.util.UUID;

@Slf4j
@RestController
@RequiredArgsConstructor
public class TaskControllerImpl implements TaskController {

  private final TaskService taskService;
  private final TaskDtoMapper taskDtoMapper;

  @Override
  public TaskResponseDto pushTask(@Valid TaskRequestDto taskRequestDto) {
    TaskMetadata metadata = taskDtoMapper.mapToTaskMetadata(taskRequestDto);
    Task task = taskService.pushTask(metadata);
    return taskDtoMapper.mapToTaskResponseDto(task);
  }

  @Override
  public TaskResponseDto getTask(UUID id) {
    return taskDtoMapper.mapToTaskResponseDto(taskService.getTask(id));
  }
}
