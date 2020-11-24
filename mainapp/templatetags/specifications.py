from django import template
from django.utils.safestring import mark_safe


register = template.Library()


TABLE_START = '''
<table class="table">
    <tbody>
'''
TABLE_ITEM = '''
        <tr>
            <td>
                {name}
            </td>
            <td>
                {value}
            </td>
        </tr>
'''
TABLE_END = '''
    </tbody>
</table>
'''
SPEC = {
    'notebook': {
        'Диагональ': 'diagonal',
        'Матрица': 'display_type',
        'Процессор': 'processor',
        'Общий объём памяти': 'processor_frequency',
        'Оперативная память': 'ram',
        'Видеокарта': 'video',
        'Время работы аккумулятора': 'time_without_charge',
    },
    'smartphone': {
        'Диагональ': 'diagonal',
        'Матрица': 'display_type',
        'Разрешение экрана': 'resolution',
        'Ёмкость аккумулятора': 'accumulator_volume',
        'Объём встроенной памяти': 'sd_volume_max',
        'SD карта': 'sd',
        'Основная камера': 'main_camera_mp',
        'Фронтальная камера': 'frontal_camera_mp',
    }
}


def get_product_specification_table_items(product, model_name):
    table_items = ''
    for name, value in SPEC[model_name].items():
        table_items += TABLE_ITEM.format(name=name, value=getattr(product, value))
    return table_items


@register.filter
def generate_product_specification_table(product):
    model_name = product.__class__._meta.model_name
    return mark_safe(TABLE_START + get_product_specification_table_items(product, model_name) + TABLE_END)
