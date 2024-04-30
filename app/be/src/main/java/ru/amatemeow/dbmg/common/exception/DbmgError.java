package ru.amatemeow.dbmg.common.exception;

public class DbmgError extends RuntimeException {

  public DbmgError() {
    super();
  }

  public DbmgError(String message) {
    super(message);
  }

  public DbmgError(String message, Throwable cause) {
    super(message, cause);
  }

  public DbmgError(Throwable cause) {
    super(cause);
  }
}
