package ru.amatemeow.dbmg.common.exception;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

@ResponseStatus(HttpStatus.NOT_FOUND)
public class DmbgNotFoundError extends DmbgCustomError {

  public DmbgNotFoundError() {
    super();
  }

  public DmbgNotFoundError(String message) {
    super(message);
  }

  public DmbgNotFoundError(String message, Throwable cause) {
    super(message, cause);
  }

  public DmbgNotFoundError(Throwable cause) {
    super(cause);
  }
}
