package ru.amatemeow.dbmg.service.model.model;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import ru.amatemeow.dbmg.service.model.model.info.ModelInfo;

import java.util.UUID;

@Data
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class Model {

  private UUID id;
  private ModelInfo modelInfo;
}
