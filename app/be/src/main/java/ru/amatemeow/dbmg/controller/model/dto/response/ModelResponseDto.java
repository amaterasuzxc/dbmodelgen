package ru.amatemeow.dbmg.controller.model.dto.response;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import ru.amatemeow.dbmg.controller.model.dto.info.ModelInfoDto;

import java.util.UUID;

@Data
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class ModelResponseDto {

  @JsonProperty("id")
  private UUID id;

  @JsonProperty("model_info")
  private ModelInfoDto modelInfo;
}
