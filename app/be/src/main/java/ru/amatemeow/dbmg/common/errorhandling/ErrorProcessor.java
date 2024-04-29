package ru.amatemeow.dbmg.common.errorhandling;

import lombok.extern.slf4j.Slf4j;
import org.springframework.core.annotation.AnnotationUtils;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Component;
import org.springframework.web.bind.annotation.ResponseStatus;
import ru.amatemeow.dbmg.common.exception.DmbgCustomError;

@Slf4j
@Component
public class ErrorProcessor {

  public ErrorMessage processError(Exception ex) {
    HttpStatus status = extractStatusOrDefault(ex, HttpStatus.INTERNAL_SERVER_ERROR);
    return processError(ex, status);
  }

  public ErrorMessage processError(Exception ex, HttpStatus status) {
    if (ex instanceof DmbgCustomError dmbgCustomError) {
      return processDmbgCustomError(dmbgCustomError, status);
    }
    return processGenericError(status);
  }

  private ErrorMessage processGenericError(HttpStatus status) {
    return ErrorMessage.builder()
        .status(status)
        .message("Something went wrong")
        .build();
  }

  private ErrorMessage processDmbgCustomError(DmbgCustomError ex, HttpStatus status) {
    return ErrorMessage.builder()
        .status(status)
        .message(ex.getMessage())
        .build();
  }

  private HttpStatus extractStatusOrDefault(Exception ex, HttpStatus defaultStatus) {
    ResponseStatus responseStatusAnnotation =
        AnnotationUtils.findAnnotation(ex.getClass(), ResponseStatus.class);
    if (responseStatusAnnotation != null) {
      return responseStatusAnnotation.code();
    }
    return defaultStatus;
  }
}
