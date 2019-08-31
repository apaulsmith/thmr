def format_datetime(value):
    if not value:
        return ''

    try:
        return value.strftime("%b %d %Y %H:%M:%S")
    except AttributeError:
        return str(value)
