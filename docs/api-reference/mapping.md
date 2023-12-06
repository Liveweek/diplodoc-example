# Mapping
Классы обработки документа-маппинга полей

## *MappingMeta*
*Класс трансформации данных из excel-файла в метаданные маппинга данных*

**Атрибуты класса**

- `mapping_df`: `pd.DataFrame`

- `src_cd`: `str`

**Публичные методы класса**

***##MappingMeta.get_tgt_tables_list(self)##***

Получить список целевых таблиц загрузки

Аргументы:
- `self`

***##MappingMeta.get_mapping_by_table(self, table_name)##***

Получить набор метаданных заполнения полей для заданной целевой таблицы

Аргументы:
- `self`
- `table_name`

## *MartMapping*
*Класс преобразования мета-данных заполнения полей в модели контекста для последующего экспорта в выходной формат*

**Атрибуты класса**

- `mart_name`: `str`

- `mart_mapping`: `pd.DataFrame`

- `src_cd`: `str`

- `data_capture_mode`: `str`

- `source_system`: `str`

- `src_ctx`: `SourceContext`

- `tgt_ctx`: `TargetContext`

- `mapping_ctx`: `MappingContext`

