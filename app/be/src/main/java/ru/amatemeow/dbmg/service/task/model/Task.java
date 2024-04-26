package ru.amatemeow.dbmg.service.task.model;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import ru.amatemeow.dbmg.common.enumeration.TaskStatus;
import ru.amatemeow.dbmg.service.model.model.Model;

import java.util.UUID;

@Data
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class Task {

  private UUID id;
  private String title;
  private String text;
  private TaskStatus status;
  private Model model;
}
