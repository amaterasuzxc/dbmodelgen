package ru.amatemeow.dbmg.repository.model.entity;

import io.hypersistence.utils.hibernate.type.json.JsonType;
import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.Type;
import ru.amatemeow.dbmg.repository.model.entity.info.ModelInfoAttribute;
import ru.amatemeow.dbmg.repository.task.entity.TaskEntity;

import java.util.UUID;

@Getter
@Setter
@Builder
@AllArgsConstructor
@NoArgsConstructor
@Entity
@Table(name = "models")
public class ModelEntity {

  @Id
  @Column(name = "id")
  private UUID id;

  @Type(JsonType.class)
  @Column(name = "entities")
  @Builder.Default
  private ModelInfoAttribute modelInfo = new ModelInfoAttribute();

  @OneToOne(fetch = FetchType.LAZY, optional = false)
  @JoinColumn(name = "model_id")
  private TaskEntity task;
}
