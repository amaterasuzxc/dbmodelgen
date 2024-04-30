package ru.amatemeow.dbmg.service.model.ddl;

import ru.amatemeow.dbmg.repository.model.entity.ModelEntity;

public interface DdlService {

  String buildDdl(ModelEntity model);
}
