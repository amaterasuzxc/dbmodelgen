package ru.amatemeow.dbmg.common.util;

import lombok.experimental.UtilityClass;

@UtilityClass
public class EnumUtils {

  public static <T extends Enum<?>> T searchEnum(Class<T> enumeration, String search, T defaultValue) {
    for (T val : enumeration.getEnumConstants()) {
      if (val.name().compareToIgnoreCase(search) == 0) {
        return val;
      }
    }
    return defaultValue;
  }
}
