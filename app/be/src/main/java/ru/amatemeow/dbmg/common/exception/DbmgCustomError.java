package ru.amatemeow.dbmg.common.exception;

public class DbmgCustomError extends DbmgError {

  public DbmgCustomError() {
    super();
  }

  public DbmgCustomError(String message) {
    super(message);
  }

  public DbmgCustomError(String message, Throwable cause) {
    super(message, cause);
  }

  public DbmgCustomError(Throwable cause) {
    super(cause);
  }
}
