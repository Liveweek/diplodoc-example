# Exporters
Классы для реализации экспорта конкретного набора артефактов в соответствии с определённым контекстом

## *SourceObjectExporter*
*Класс-экспортёр артефактов, описывающих таблицы системы источника (1 yaml-файл)*

**Атрибуты класса**

- `src_ctx`: `SourceContext`

- `env`: `Environment`

- `template_name`: `str`

**Публичные методы класса**

***##SourceObjectExporter.export(self, path)##***

Метод реализует экспорт контекста таблицы источника в YAML-файл в соответствии с форматом в ЦЕХ

Аргументы:
- `self`
- `path`

## *TargetObjectExporter*
*Класс-экспортёр артефактов, описывающих целевые таблицы загрузки (yaml-файл, ddl-скрипт и json-шаблон для ресурса)*

**Атрибуты класса**

- `tgt_ctx`: `TargetContext`

- `env`: `Environment`

- `template_name_yaml`: `str`

- `template_name_sql`: `str`

- `template_name_json`: `str`

**Публичные методы класса**

***##TargetObjectExporter.export_yaml(self, path)##***

Экспортирует YAML-файл целевого объекта в заданный путь на основе контекста

Аргументы:
- `self`
- `path`

***##TargetObjectExporter.export_sql(self, path)##***

Экспортирует DDL-скрипт на SQL в заданный путь на основе контекста

Аргументы:
- `self`
- `path`

***##TargetObjectExporter.export_ceh_resource(self, path)##***

Экспортирует JSON-файл ресурса в заданный путь на основе контекста

Аргументы:
- `self`
- `path`

## *MappingObjectExporter*
*Класс-экспортёр артефактов файлов потока (WF, CF и python-файл для сборки WF)*

**Атрибуты класса**

- `map_ctx`: `MappingContext`

- `env`: `Environment`

- `wf_file`: `str`

- `cf_file`: `str`

- `author_name`: `str`

- `template_wf_name`: `str`

- `template_cf_name`: `str`

- `template_py_name`: `str`

**Публичные методы класса**

***##MappingObjectExporter.export_wf(self, path)##***

Экспортирует YAML-файл рабочего потока в соответствии с заданным контекстом в указанный путь

Аргументы:
- `self`
- `path`

***##MappingObjectExporter.export_cf(self, path)##***

Экспортирует YAML-файл управляющего потока в соответствии с заданным контекстом в указанный путь

Аргументы:
- `self`
- `path`

***##MappingObjectExporter.export_py(self, path)##***

Экспортирует python-файл рабочего потока в указанный путь

Аргументы:
- `self`
- `path`

## *MartPackExporter*
*Класс-фасад для выгрузки полного набора артефактов потока: источника, целевого объекта и правила заполнения полей*

**Атрибуты класса**

- `exp_obj`: `MartMapping`

- `path`: `str`

- `_src_exporter`: `SourceObjectExporter`

- `_tgt_exporter`: `TargetObjectExporter`

- `_mapping_exporter`: `MappingObjectExporter`

**Публичные методы класса**

***##MartPackExporter.load(self)##***

Инициализирует процесс экспорта всех артекфактов

Аргументы:
- `self`