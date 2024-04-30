package ru.amatemeow.dbmg.common.restclient.aiservice.dto.request;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class ProcessModelRequestDto {

  @JsonProperty("text")
  private String text;
}
