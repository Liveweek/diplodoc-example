"""Базовые исключения, используемые в рамках работы генератора"""


class IncorrectMappingReadException(Exception):
    """Исключение, вызываемое в случае некорректного входного формата маппинга для обработки"""
    def __str__(self):
        return 'Некорректно сформирован excel-файл маппинга'


class IncorrectSetupException(Exception):
    """Исключение, вызываемое в случае некорректного указания параметров генератора маппинга"""
    def __str__(self):
        return 'Заполните все файлы программы для генерации маппинга'