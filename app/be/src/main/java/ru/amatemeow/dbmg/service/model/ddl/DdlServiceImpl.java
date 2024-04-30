package ru.amatemeow.dbmg.service.model.ddl;

import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.util.CollectionUtils;
import ru.amatemeow.dbmg.common.constants.DdlClausePatterns;
import ru.amatemeow.dbmg.common.enumeration.PostgresDataType;
import ru.amatemeow.dbmg.common.util.EnumUtils;
import ru.amatemeow.dbmg.repository.model.entity.ModelEntity;
import ru.amatemeow.dbmg.repository.model.entity.info.LogicalAttributeInfoAttribute;
import ru.amatemeow.dbmg.repository.model.entity.info.LogicalEntityInfoAttribute;

import java.text.MessageFormat;
import java.util.List;

@Slf4j
@Service
public class DdlServiceImpl implements DdlService {

  @Override
  public String buildDdl(ModelEntity model) {
    List<String> builtTables = buildTables(model.getModelInfo().getEntities());
    return String.join("\n\n", builtTables);
  }

  private List<String> buildTables(List<LogicalEntityInfoAttribute> entities) {
    return entities.stream().map(ent -> {
      String tableClause = MessageFormat.format(DdlClausePatterns.TABLE_PATTERN, ent.getName());
      String attributesClausesUnited = buildAttributes(ent.getAttributes());
      return MessageFormat.format(
          DdlClausePatterns.CREATE_TABLE_CLAUSE_PATTERN,
          tableClause,
          attributesClausesUnited);
    }).toList();
  }

  private String buildAttributes(List<LogicalAttributeInfoAttribute> attributes) {
    List<String> attributeStrings = attributes.stream()
        .map(attr -> MessageFormat.format(
            DdlClausePatterns.COLUMN_PATTERN,
            attr.getName(),
            EnumUtils.searchEnum(
                PostgresDataType.class,
                attr.getType(),
                PostgresDataType.STRING).getValue()))
        .toList();
    CollectionUtils.lastElement(attributeStrings).replaceFirst(",$", "");
    return String.join(",", attributeStrings);
  }
}
