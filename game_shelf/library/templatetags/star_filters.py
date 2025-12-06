from django import template

register = template.Library()

@register.filter
def stars(rating):
    """
    Convert a decimal rating (0–5, in 0.25 increments) into a list
    of 5 elements: 'full', 'three_quarter', 'half', 'quarter', 'empty'
    """
    stars_list = []
    r = float(rating)
    for i in range(1, 6):
        diff = r - i + 1
        if diff >= 1:
            stars_list.append('full')
        elif diff >= 0.75:
            stars_list.append('three_quarter')
        elif diff >= 0.5:
            stars_list.append('half')
        elif diff >= 0.25:
            stars_list.append('quarter')
        else:
            stars_list.append('empty')
    return stars_list
