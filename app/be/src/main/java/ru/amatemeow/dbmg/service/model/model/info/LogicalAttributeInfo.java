package ru.amatemeow.dbmg.service.model.model.info;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class LogicalAttributeInfo {

  private String name;
  private String type;
}
