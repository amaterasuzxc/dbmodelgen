package ru.amatemeow.dbmg.common.exception;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

@ResponseStatus(HttpStatus.NOT_FOUND)
public class DbmgNotFoundError extends DbmgCustomError {

  public DbmgNotFoundError() {
    super();
  }

  public DbmgNotFoundError(String message) {
    super(message);
  }

  public DbmgNotFoundError(String message, Throwable cause) {
    super(message, cause);
  }

  public DbmgNotFoundError(Throwable cause) {
    super(cause);
  }
}
