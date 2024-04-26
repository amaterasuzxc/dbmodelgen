package ru.amatemeow.dbmg.repository.model.entity.info;

import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.validation.Valid;
import jakarta.validation.constraints.NotEmpty;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import ru.amatemeow.dbmg.controller.model.dto.info.LogicalAttributeInfoDto;

import java.util.ArrayList;
import java.util.List;

@Data
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class LogicalEntityInfoAttribute {

  @JsonProperty("name")
  @NotEmpty
  private String name;

  @JsonProperty("attributes")
  @Valid
  @Builder.Default
  private List<LogicalAttributeInfoDto> attributes = new ArrayList<>();
}
