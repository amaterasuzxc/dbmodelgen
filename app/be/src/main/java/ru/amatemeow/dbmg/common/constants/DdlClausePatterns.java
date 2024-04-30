package ru.amatemeow.dbmg.common.constants;

import lombok.experimental.UtilityClass;

@UtilityClass
public class DdlClausePatterns {

  public static final String TABLE_PATTERN = "CREATE TABLE \"{0}\"";
  public static final String COLUMN_PATTERN = "\n\t\"{0}\" {1}";

  public static final String CREATE_TABLE_CLAUSE_PATTERN = "{0} ({1}\n);";

}
