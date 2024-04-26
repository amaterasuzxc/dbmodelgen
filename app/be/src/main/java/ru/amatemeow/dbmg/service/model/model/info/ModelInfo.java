package ru.amatemeow.dbmg.service.model.model.info;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

@Data
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class ModelInfo {

  private String title;
  private List<LogicalEntityInfo> entities;
}
