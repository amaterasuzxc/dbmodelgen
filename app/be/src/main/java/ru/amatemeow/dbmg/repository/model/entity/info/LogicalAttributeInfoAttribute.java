package ru.amatemeow.dbmg.repository.model.entity.info;

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
public class LogicalAttributeInfoAttribute {

  @JsonProperty("name")
  @NotEmpty
  private String name;

  @JsonProperty("type")
  @NotEmpty
  private String type;
}
