package ru.amatemeow.dbmg.repository.model;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import ru.amatemeow.dbmg.repository.model.entity.ModelEntity;

import java.util.UUID;

@Repository
public interface ModelRepository extends JpaRepository<ModelEntity, UUID> {
}
