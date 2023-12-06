"""
Модуль датаклассов контекста, на основе которых формируются артефакты потоков
"""
from dataclasses import dataclass, KW_ONLY, field


@dataclass
class FieldContext:
    """Класс контекста поля"""
    name:        str
    datatype:    str
    is_nullable: bool = True


    def __post_init__(self):
        if self.datatype.upper().strip() == "CHAR(32)":
            self.datatype = "TEXT"

@dataclass
class HubFieldContext:
    """Класс контекста поля, заполняемого через Hub"""
    name:           str
    bk_schema_name: str
    hub_name:       str
    on_full_null:   str
    _: KW_ONLY
    hub_field:      str = ''

    def __post_init__(self):
        self.hub_field = f'{self.hub_name[4:]}_id'


@dataclass
class FieldMapContext:
    """Класс контекста заполнения поля"""
    src_field:      str
    tgt_field:      str
    tgt_datatype:   str
    sql_expression: str = "~"


@dataclass
class TableContext:
    """Класс контекста таблицы"""
    name:          str
    src_cd:        str
    field_context: list
    _: KW_ONLY
    schema:        str = '~'
    field_ctx_list: list[FieldContext] = field(default_factory=list)

    def __post_init__(self):
        match self.name.split('.'):
            case [table_name]:
                self.name = table_name
            case [schema_name, table_name]:
                self.schema = schema_name
                self.name = table_name

        print(f"Создан контекст для таблицы: схема ({self.schema}) таблица ({self.name})")

        for row in self.field_context:
            match row:
                case [name, datatype]:
                    field = FieldContext(name=name, datatype=datatype)
                    self.field_ctx_list.append(field)
                case [name, datatype, nullable]:
                    field = FieldContext(
                        name=name,
                        datatype=datatype,
                        is_nullable=nullable.lower() != 'not null',
                    )
                    self.field_ctx_list.append(field)



@dataclass
class SourceContext(TableContext):
    """Класс контекста таблицы источника"""
    data_capture_mode: str


@dataclass
class DAPPSourceContext(SourceContext):
    """Класс контекста таблицы источника DAPP"""
    def __post_init__(self):
        super().__post_init__()
        self.field_ctx_list.append(FieldContext('hdp_processed_dttm', 'timestamp'))

        if self.data_capture_mode == 'increment':
            self.field_ctx_list.append(FieldContext('changetype', 'text'))


@dataclass
class DRPSourceContext(SourceContext):
    """Класс контекста таблицы источника DRP"""
    def __post_init__(self):
        super().__post_init__()

        self.field_ctx_list.append(FieldContext('processed_dt', 'timestamp'))
        self.field_ctx_list.append(FieldContext('dte', 'text'))

        if self.data_capture_mode == 'increment':
            self.field_ctx_list.append(FieldContext('op_type', 'text'))


@dataclass
class TargetContext(TableContext):
    """Класс контекста целевой таблицы загрузки"""
    hub_context:     list

    hash_src_fields: list[str] = field(default_factory=list)
    hub_pool:        set[str] = field(default_factory=set)
    hub_ctx_list:    list[HubFieldContext] = field(default_factory=list)

    def __post_init__(self):
        super().__post_init__()

        for row in self.hub_context:
            hub_field = HubFieldContext(*row)
            self.hub_ctx_list.append(hub_field)
            self.hub_pool.add(hub_field.hub_name)

        hub_fields = {hub_f.name for hub_f in self.hub_ctx_list}
        fields = {field.name for field in self.field_ctx_list}

        self.hash_src_fields = list(fields - hub_fields)


@dataclass
class MappingContext:
    """Класс контекста алгоритма заполнения полей"""
    field_map_context:  list
    src_cd:             str
    src_name:           str
    src_schema:         str
    tgt_name:           str
    algo:               str
    algo_sub:           str
    data_capture_mode:  str
    source_system:      str
    hub_pool:           set[str]
    hub_ctx_list:       list[HubFieldContext] = field(default_factory=list)
    field_map_ctx_list: list[FieldMapContext] = field(default_factory=list)

    def __post_init__(self):
        for row in self.field_map_context:
            field_map = FieldMapContext(*row)
            self.field_map_ctx_list.append(field_map)

        if self.data_capture_mode == 'increment':

            __deleted_flg_sql_expr = {
                "DAPP": "upper(changetype) = 'DELETE'",
                "DRP": "upper(op_type) = 'DELETE'"
            }

            deleted_flg_map = FieldMapContext(
                src_field='',
                tgt_field='deleted_flg',
                tgt_datatype='boolean',
                sql_expression=__deleted_flg_sql_expr[self.source_system],
            )
            self.field_map_ctx_list.append(deleted_flg_map)
