package ru.amatemeow.dbmg.service.task.queue;

import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;
import ru.amatemeow.dbmg.repository.model.entity.ModelEntity;
import ru.amatemeow.dbmg.repository.task.entity.TaskEntity;

import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

@Slf4j
@Component
public class TextProcessingTask { // TODO

  private static final Lock LOCK = new ReentrantLock(true);

  private static final int POLL_STATUS_TIMEOUT_MILLIS = 10000;

  ModelEntity runTask(TaskEntity task) {
    return null;
  }
}
