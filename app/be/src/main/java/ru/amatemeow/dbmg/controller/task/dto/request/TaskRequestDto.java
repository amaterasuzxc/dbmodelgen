package ru.amatemeow.dbmg.controller.task.dto.request;

import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.validation.constraints.NotEmpty;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class TaskRequestDto {

  @JsonProperty("title")
  @NotEmpty
  private String title;

  @JsonProperty("text")
  @NotEmpty
  private String text;
}
