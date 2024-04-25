package ru.amatemeow.dbmg.controller.task;


import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import ru.amatemeow.dbmg.common.constants.Urls;
import ru.amatemeow.dbmg.controller.task.dto.request.TaskRequestDto;
import ru.amatemeow.dbmg.controller.task.dto.response.TaskResponseDto;

public interface TaskController {

  @PostMapping(path = Urls.TASK_URL, consumes = MediaType.APPLICATION_JSON_VALUE)
  TaskResponseDto upload(@RequestBody TaskRequestDto taskRequestDto);
}
