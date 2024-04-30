package ru.amatemeow.dbmg.common.restclient.aiservice.dto.response;

import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import ru.amatemeow.dbmg.common.enumeration.AiServiceStatus;

@Data
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class StatusResponseDto {

  @JsonProperty("status")
  @NotNull
  private AiServiceStatus status;
}
