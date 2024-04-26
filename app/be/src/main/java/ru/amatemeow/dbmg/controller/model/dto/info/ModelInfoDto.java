package ru.amatemeow.dbmg.controller.model.dto.info;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

@Data
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class ModelInfoDto {

  @JsonProperty("title")
  private String title;

  @JsonProperty("entities")
  private List<LogicalEntityInfoDto> entities;
}
