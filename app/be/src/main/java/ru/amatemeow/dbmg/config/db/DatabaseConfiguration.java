package ru.amatemeow.dbmg.config.db;

import jakarta.persistence.EntityManagerFactory;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.boot.jdbc.DataSourceBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;
import org.springframework.orm.jpa.JpaTransactionManager;
import org.springframework.orm.jpa.LocalContainerEntityManagerFactoryBean;
import org.springframework.orm.jpa.vendor.HibernateJpaVendorAdapter;
import org.springframework.transaction.PlatformTransactionManager;
import org.springframework.transaction.annotation.EnableTransactionManagement;

import javax.sql.DataSource;

@EnableTransactionManagement
@EnableJpaRepositories(basePackages = "ru.amatemeow.dbmg")
@Configuration
public class DatabaseConfiguration {

  @Bean
  @ConfigurationProperties("spring.datasource")
  public DataSource dataSource() {
    return DataSourceBuilder.create().build();
  }

  @Bean
  public EntityManagerFactory entityManagerFactory(DataSource dataSource, JpaProperties jpaProperties) {
    LocalContainerEntityManagerFactoryBean entityManagerFactoryBean = new LocalContainerEntityManagerFactoryBean();
    entityManagerFactoryBean.setDataSource(dataSource);
    entityManagerFactoryBean.setPackagesToScan("ru.amatemeow.dbmg");
    entityManagerFactoryBean.setJpaVendorAdapter(new HibernateJpaVendorAdapter());
    entityManagerFactoryBean.setJpaProperties(jpaProperties.toProperties());
    entityManagerFactoryBean.afterPropertiesSet();
    return entityManagerFactoryBean.getObject();
  }

  @Bean
  public PlatformTransactionManager transactionManager(EntityManagerFactory entityManagerFactory) {
    JpaTransactionManager transactionManager = new JpaTransactionManager();
    transactionManager.setEntityManagerFactory(entityManagerFactory);
    return transactionManager;
  }
}
