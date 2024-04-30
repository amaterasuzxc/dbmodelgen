package ru.amatemeow.dbmg.common.exception;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

@ResponseStatus(HttpStatus.UNPROCESSABLE_ENTITY)
public class DbmgEmptyModelError extends DbmgCustomError {

  public DbmgEmptyModelError() {
    super("An empty model response was received from AI service");
  }
}
