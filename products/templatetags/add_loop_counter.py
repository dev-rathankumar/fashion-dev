from django import template


register = template.Library()


@register.filter(name='add_loop_counter')
def add_loop_counter(field, value):
    return field.as_widget(
        attrs={
            "data-idnum": value
        }
    )
