package ru.amatemeow.dbmg.common.enumeration;

import lombok.Getter;
import lombok.RequiredArgsConstructor;

@Getter
@RequiredArgsConstructor
public enum PostgresDataType {

  TIMESTAMP("timestamp"),
  STRING("varchar(255)"),
  BOOLEAN("boolean"),
  INTEGER("integer"),
  DOUBLE("double precision");

  private final String value;
}
