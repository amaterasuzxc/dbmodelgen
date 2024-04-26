package ru.amatemeow.dbmg.repository.task.entity;

import jakarta.persistence.*;
import lombok.*;
import ru.amatemeow.dbmg.common.enumeration.TaskStatus;
import ru.amatemeow.dbmg.repository.model.entity.ModelEntity;

import java.util.UUID;

@Getter
@Setter
@Builder
@AllArgsConstructor
@NoArgsConstructor
@Entity
@Table(name = "tasks")
public class TaskEntity {

  @Id
  @Column(name = "id")
  private UUID id;

  @Column(name = "title")
  private String title;

  @Column(name = "text")
  private String text;

  @Enumerated(EnumType.STRING)
  @Column(name = "status")
  private TaskStatus status;

  @OneToOne(mappedBy = "task", fetch = FetchType.LAZY, optional = false, cascade = CascadeType.ALL)
  private ModelEntity model;
}
