import re
from jinja2 import Template
from .naming_conventions import camel_to_snake

PYTHON_TEMPLATE = """from dataclasses import dataclass, field
from typing import Optional, List, Union
from decimal import Decimal
from datetime import date

class MissingType:
    pass
{% for type_name, type_spec in types.items() %}
@dataclass
class {{ type_name }}:
    {% for field in type_spec['properties'] -%}
    {{ field['name'] }}: {% if field['extant'] == 'missing' -%}
    Union[{{ field['mapped_type'] }}, MissingType]{% elif field['optional'] -%}
    Optional[{{ field['mapped_type'] }}]{% else -%}
    {{ field['mapped_type'] }}{% endif -%}
    {%- if field['default'] is not none -%} = {{ field['default'] }}
    {%- elif field['extant'] == 'missing' -%} = MissingType()
    {%- elif field['optional'] -%} = None
    {%- elif field['mapped_type'] == 'List[str]' -%} = field(default_factory=list)
    {%- endif %}
    {% endfor %}
{%- endfor %}"""

def map_type_to_python(yaml_type: str) -> str:
    """
    Maps YAML types to Python types.

    :param yaml_type: The type from the YAML specification.
    :return: Corresponding Python type as a string.
    """
    type_mapping = {
        "String": "str",
        "Integer": "int",
        "Decimal": "Decimal",
        "Date": "date",
        "Boolean": "bool",
        "Null": "None",
    }

    # Process lists
    list_match = re.match(r"List<(.+)>", yaml_type)
    if list_match:
        inner_type = list_match.group(1)
        mapped_inner_type = map_type_to_python(inner_type)
        return f"List[{mapped_inner_type}]"

    # Default mapping
    return type_mapping.get(yaml_type, yaml_type)

def preprocess_yaml_for_python(parsed_yaml: dict) -> dict:
    """
    Preprocesses the parsed YAML to map types, apply naming conventions,
    and handle optional fields. Sorts properties such that fields with defaults
    are placed after fields without defaults.
    """
    preprocessed = {}
    for type_name, type_spec in parsed_yaml.items():
        properties = []
        for field_name, field_spec in type_spec.get("properties", {}).items():
            clean_field_name = field_name.rstrip("?")
            properties.append({
                "name": camel_to_snake(clean_field_name),
                "mapped_type": map_type_to_python(field_spec["type"]),
                "optional": field_name.endswith("?"),
                "default": field_spec.get("default"),
                "extant": field_spec.get("extant", "required"),
            })
        # Sort properties: without defaults first, then with defaults
        sorted_properties = sorted(properties, key=lambda p: p["default"] is not None or p["extant"] == "missing")
        preprocessed[type_name] = {"properties": sorted_properties}
    return preprocessed

def generate_python_types(parsed_yaml: dict) -> str:
    preprocessed_yaml = preprocess_yaml_for_python(parsed_yaml)
    template = Template(PYTHON_TEMPLATE)
    return template.render(types=preprocessed_yaml)
