package ru.amatemeow.dbmg.common.constants;

import lombok.experimental.UtilityClass;

@UtilityClass
public class Urls {

  public static final String BASIC_URL = "rest/v1";

  public static final String TASK_URL = BASIC_URL + "/tasks";
  public static final String TASK_BY_ID_URL = TASK_URL + "/{id}";

  public static final String MODEL_URL = BASIC_URL + "/models";
  public static final String MODEL_BY_ID_URL = MODEL_URL + "/{id}";
  public static final String MODEL_DDL_URL = MODEL_BY_ID_URL + "/ddl";
}
