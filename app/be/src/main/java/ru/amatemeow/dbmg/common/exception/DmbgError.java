package ru.amatemeow.dbmg.common.exception;

public class DmbgError extends RuntimeException {

  public DmbgError() {
    super();
  }

  public DmbgError(String message) {
    super(message);
  }

  public DmbgError(String message, Throwable cause) {
    super(message, cause);
  }

  public DmbgError(Throwable cause) {
    super(cause);
  }
}
