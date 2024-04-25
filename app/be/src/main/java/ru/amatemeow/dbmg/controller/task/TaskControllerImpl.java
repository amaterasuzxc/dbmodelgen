package ru.amatemeow.dbmg.controller.task;

import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.web.bind.annotation.RestController;
import ru.amatemeow.dbmg.controller.task.dto.request.TaskRequestDto;
import ru.amatemeow.dbmg.controller.task.dto.response.TaskResponseDto;

@Slf4j
@RestController
@RequiredArgsConstructor
public class TaskControllerImpl implements TaskController {

  @Override
  public TaskResponseDto upload(@Valid TaskRequestDto taskRequestDto) {
    return null;
  }
}
