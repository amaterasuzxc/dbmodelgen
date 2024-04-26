package ru.amatemeow.dbmg.repository.task;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;
import ru.amatemeow.dbmg.repository.task.entity.TaskEntity;

import java.util.UUID;

@Repository
public interface TaskRepository extends JpaRepository<TaskEntity, UUID> {

  @Query(
      """
      select
        t.id
      from TaskEntity t
      where t.status in ('PENDING', 'RUNNING', 'FAILED')
  """)
  Iterable<UUID> findAllUnfinishedTaskIds();
}
