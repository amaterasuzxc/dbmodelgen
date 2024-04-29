package ru.amatemeow.dbmg.common.errorhandling;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.core.annotation.AnnotationUtils;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseStatus;
import ru.amatemeow.dbmg.common.exception.DmbgError;

@Slf4j
@RequiredArgsConstructor
@ControllerAdvice
public class DbmgControllerAdvice {

  private final ErrorProcessor errorProcessor;

  @ExceptionHandler({DmbgError.class})
  public ResponseEntity<ErrorMessage> handleGenericException(DmbgError ex) {
    logError(ex);
    return makeErrorResponse(errorProcessor.processError(ex));
  }

  private ResponseEntity<ErrorMessage> makeErrorResponse(ErrorMessage errorMessage) {
    return ResponseEntity.status(errorMessage.getStatusCode())
        .contentType(MediaType.APPLICATION_JSON)
        .body(errorMessage);
  }

  private void logError(Exception ex) {
    ResponseStatus responseStatusAnnotation =
        AnnotationUtils.findAnnotation(ex.getClass(), ResponseStatus.class);
    String errorMessage = "Caught unhandled exception";
    if (responseStatusAnnotation != null) {
      errorMessage =
          "Caught unhandled exception with status code '"
              + responseStatusAnnotation.code()
              + "' and reason '"
              + responseStatusAnnotation.reason()
              + "'";
    }
    log.error(errorMessage, ex);
  }
}
