package ru.amatemeow.dbmg.controller.task;


import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import ru.amatemeow.dbmg.common.constants.Urls;
import ru.amatemeow.dbmg.controller.task.dto.request.TaskRequestDto;
import ru.amatemeow.dbmg.controller.task.dto.response.TaskResponseDto;

import java.util.UUID;

public interface TaskController {

  @PostMapping(path = Urls.TASK_URL, consumes = MediaType.APPLICATION_JSON_VALUE, produces = MediaType.APPLICATION_JSON_VALUE)
  TaskResponseDto pushTask(@RequestBody TaskRequestDto taskRequestDto);

  @GetMapping(path = Urls.TASK_BY_ID_URL, produces = MediaType.APPLICATION_JSON_VALUE)
  TaskResponseDto getTask(@PathVariable UUID id);
}
