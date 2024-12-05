import re

def snake_to_camel(snake_str: str) -> str:
    components = snake_str.split('_')
    return components[0] + ''.join(x.capitalize() for x in components[1:])

def camel_to_snake(camel_str: str) -> str:
    return re.sub(r'(?<!^)(?=[A-Z])', '_', camel_str).lower()
