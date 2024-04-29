package ru.amatemeow.dbmg.common.exception;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

@ResponseStatus(HttpStatus.INTERNAL_SERVER_ERROR)
public class DbmgInternalError extends DmbgError {

  public DbmgInternalError() {
    super("Something went wrong");
  }
}
