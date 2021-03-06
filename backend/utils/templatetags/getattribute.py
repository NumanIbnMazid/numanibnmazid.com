from django import template

numeric_test = r"^\d+$"
register = template.Library()


def getattribute(value, arg):
    """Gets an attribute of an object dynamically from a string name"""
    try:
        if hasattr(value, str(arg)):
            if hasattr(getattr(value, str(arg), None), 'url'):
                return getattr(value, str(arg)).url
            return getattr(value, str(arg))
        elif hasattr(value, 'has_key') and value in arg:
            return value[arg]
        elif numeric_test.match(str(arg)) and len(value) > int(arg):
            return value[int(arg)]
        else:
            return None
    except Exception:
        return None


register.filter('getattribute', getattribute)
