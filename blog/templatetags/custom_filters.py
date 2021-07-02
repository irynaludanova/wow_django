from django import template

register = template.Library()


CENSOR = [
    'бля', 'пизд', 'еба','хуй', 'хуе',
]

@register.filter(name='censor')
def censor(text: str):
    text_list = text.split()
    for i in range(len(text_list)):
        for c in CENSOR:
            if text_list[i].lower().find(c) >= 0:
                text_list[i] = '***'
    return ' '.join(text_list)
