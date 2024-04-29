package ru.amatemeow.dbmg.common.exception;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

@ResponseStatus(HttpStatus.INTERNAL_SERVER_ERROR)
public class DbmgModelProcessingException extends DmbgCustomError {

  public DbmgModelProcessingException() {
    super();
  }

  public DbmgModelProcessingException(String message) {
    super(message);
  }

  public DbmgModelProcessingException(String message, Throwable cause) {
    super(message, cause);
  }

  public DbmgModelProcessingException(Throwable cause) {
    super(cause);
  }
}
