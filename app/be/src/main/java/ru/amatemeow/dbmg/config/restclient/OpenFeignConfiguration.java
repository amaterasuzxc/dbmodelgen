package ru.amatemeow.dbmg.config.restclient;

import org.springframework.cloud.openfeign.EnableFeignClients;
import org.springframework.context.annotation.Configuration;

@EnableFeignClients(basePackages = "ru.amatemeow.dbmg.common.restclient")
@Configuration
public class OpenFeignConfiguration {
}
