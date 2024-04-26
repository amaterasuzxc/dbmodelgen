package ru.amatemeow.dbmg.service.DdlService;

import ru.amatemeow.dbmg.repository.model.entity.ModelEntity;

public interface DdlService {

  String buildDdl(ModelEntity model);
}
