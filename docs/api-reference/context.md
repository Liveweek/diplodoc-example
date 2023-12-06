# Context

Модуль датаклассов контекста, на основе которых формируются артефакты потоков


## *FieldContext*
*Класс контекста поля*

**Атрибуты класса**

- `name`: `str`

- `datatype`: `str`

- `is_nullable`: `bool`



## *HubFieldContext*
*Класс контекста поля, заполняемого через Hub*

**Атрибуты класса**

- `name`: `str`

- `bk_schema_name`: `str`

- `hub_name`: `str`

- `on_full_null`: `str`

- `hub_field`: `str`



## *FieldMapContext*
*Класс контекста заполнения поля*

**Атрибуты класса**

- `src_field`: `str`

- `tgt_field`: `str`

- `tgt_datatype`: `str`

- `sql_expression`: `str`



## *TableContext*
*Класс контекста таблицы*

**Атрибуты класса**

- `name`: `str`

- `src_cd`: `str`

- `field_context`: `list`

- `schema`: `str`

- `field_ctx_list`: `list[FieldContext]`



## *SourceContext*
*Класс контекста таблицы источника*

**Атрибуты класса**

- `data_capture_mode`: `str`



## *DAPPSourceContext*
*Класс контекста таблицы источника DAPP*





## *DRPSourceContext*
*Класс контекста таблицы источника DRP*





## *TargetContext*
*Класс контекста целевой таблицы загрузки*

**Атрибуты класса**

- `hub_context`: `list`

- `hash_src_fields`: `list[str]`

- `hub_pool`: `set[str]`

- `hub_ctx_list`: `list[HubFieldContext]`



## *MappingContext*
*Класс контекста алгоритма заполнения полей*

**Атрибуты класса**

- `field_map_context`: `list`

- `src_cd`: `str`

- `src_name`: `str`

- `src_schema`: `str`

- `tgt_name`: `str`

- `algo`: `str`

- `algo_sub`: `str`

- `data_capture_mode`: `str`

- `source_system`: `str`

- `hub_pool`: `set[str]`

- `hub_ctx_list`: `list[HubFieldContext]`

- `field_map_ctx_list`: `list[FieldMapContext]`

