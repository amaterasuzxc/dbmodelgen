package ru.amatemeow.dbmg.repository.model.entity.info;

import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.validation.Valid;
import jakarta.validation.constraints.NotEmpty;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.ArrayList;
import java.util.List;

@Data
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class ModelInfoAttribute {

  @JsonProperty("title")
  @NotEmpty
  private String title;

  @JsonProperty("entities")
  @Valid
  @Builder.Default
  private List<LogicalEntityInfoAttribute> entities = new ArrayList<>();
}
