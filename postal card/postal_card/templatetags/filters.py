from django import template

register = template.Library()

def convertNum(value):
    if value == '0':
        return '۰'
    elif value == '1':
        return '۱'
    elif value == '2':
        return '۲'
    elif value == '3':
        return '۳'
    elif value == '4':
        return '۴'
    elif value == '5':
        return '۵'
    elif value == '6':
        return '۶'
    elif value == '7':
        return '۷'
    elif value == '8':
        return '۸'
    elif value == '9':
        return '۹'
    return value

@register.filter(name= 'convertText')
def convertText(value):
    newValue = ""
    for ch in value:
        newValue += convertNum(ch)
    return newValue   