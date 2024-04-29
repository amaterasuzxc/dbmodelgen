package ru.amatemeow.dbmg.common.errorhandling;

import com.fasterxml.jackson.annotation.JsonGetter;
import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Builder;
import lombok.Data;
import org.springframework.http.HttpStatus;

@Data
@Builder
public class ErrorMessage {

  @JsonIgnore
  private final HttpStatus status;

  @JsonProperty("message")
  private final String message;

  @JsonGetter("status")
  public int getStatusCode() {
    return status.value();
  }
}
