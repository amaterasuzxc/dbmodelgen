package ru.amatemeow.dbmg.controller.task.dto.response;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import ru.amatemeow.dbmg.common.enumeration.TaskStatus;

import java.util.UUID;

@Data
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class TaskResponseDto {

  @JsonProperty("id")
  private UUID id;

  @JsonProperty("title")
  private String title;

  @JsonProperty("text")
  private String text;

  @JsonProperty("status")
  private TaskStatus status;

  @JsonProperty("model_id")
  private UUID modelId;
}
