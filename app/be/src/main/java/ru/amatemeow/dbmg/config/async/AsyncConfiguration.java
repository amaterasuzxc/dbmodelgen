package ru.amatemeow.dbmg.config.async;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.task.TaskExecutor;
import org.springframework.scheduling.annotation.EnableAsync;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;
import ru.amatemeow.dbmg.common.constants.TaskExecutorNames;

@EnableAsync
@Configuration
public class AsyncConfiguration {

  @Bean(name = TaskExecutorNames.AI_TASK_EXECUTOR)
  public TaskExecutor aiTaskExecutor(
      @Value("${dbmg.task.max-parallel-tasks:10}") int corePoolSize,
      @Value("${dbmg.task.max-queue-size:20}") int queueCapacity
  ) {
    ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
    executor.setCorePoolSize(corePoolSize);
    executor.setMaxPoolSize(corePoolSize);
    executor.setQueueCapacity(queueCapacity);
    executor.setThreadNamePrefix("ai-task-executor-");
    executor.afterPropertiesSet();
    return executor;
  }
}
