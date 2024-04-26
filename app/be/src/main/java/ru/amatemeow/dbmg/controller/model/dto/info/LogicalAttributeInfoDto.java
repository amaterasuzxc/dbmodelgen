package ru.amatemeow.dbmg.controller.model.dto.info;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class LogicalAttributeInfoDto {

  @JsonProperty("name")
  private String name;

  @JsonProperty("type")
  private String type;
}
