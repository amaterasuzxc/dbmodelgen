package ru.amatemeow.dbmg.common.exception;

public class DmbgCustomError extends DmbgError {

  public DmbgCustomError() {
    super();
  }

  public DmbgCustomError(String message) {
    super(message);
  }

  public DmbgCustomError(String message, Throwable cause) {
    super(message, cause);
  }

  public DmbgCustomError(Throwable cause) {
    super(cause);
  }
}
