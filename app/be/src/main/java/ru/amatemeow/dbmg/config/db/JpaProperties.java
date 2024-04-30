package ru.amatemeow.dbmg.config.db;

import lombok.Getter;
import lombok.Setter;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.Configuration;

import java.util.Map;
import java.util.Properties;

@Getter
@Setter
@ConfigurationProperties("spring.jpa")
@Configuration
public class JpaProperties {

  Map<String, String> properties;

  public Properties toProperties() {
    Properties properties = new Properties();
    this.properties.forEach(properties::setProperty);
    return properties;
  }
}
