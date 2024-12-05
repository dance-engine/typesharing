import re

from jinja2 import Template
from .naming_conventions import snake_to_camel

TS_TEMPLATE = """{%- for type_name, type_spec in types.items() -%}
interface {{ type_name }} {
    {% for field_name, field_spec in type_spec['properties'].items() -%}
    {{ field_name }}{{ '?' if field_spec['optional'] }}: {{ "null | undefined | " + field_spec['mapped_type'] if field_spec.get('extant') == 'missing' else "null | " + field_spec['mapped_type'] if field_spec['optional'] else field_spec['mapped_type'] }};
    {% endfor %}
}
{% endfor %}
"""

def map_type_to_ts(yaml_type: str) -> str:
    """
    Maps YAML types to TypeScript types.
    :param yaml_type: The type from the YAML specification.
    :return: Corresponding TypeScript type as a string.
    """
    type_mapping = {
        "String": "string",
        "Integer": "number",
        "Decimal": "string",
        "Date": "string",
        "Boolean": "boolean",
        "Null": "null",
    }

    # Check for generic List<T> types
    list_match = re.match(r"List<(.+)>", yaml_type)
    if list_match:
        inner_type = list_match.group(1)
        mapped_inner_type = map_type_to_ts(inner_type)
        return f"{mapped_inner_type}[]"

    # Default mapping
    return type_mapping.get(yaml_type, yaml_type)

def preprocess_yaml_for_ts(parsed_yaml: dict) -> dict:
    """
    Preprocesses the parsed YAML to map types for TypeScript and apply naming conventions.
    :param parsed_yaml: The parsed YAML as a dictionary.
    :return: Preprocessed YAML with mapped types and camelCase field names.
    """
    preprocessed = {}
    for type_name, type_spec in parsed_yaml.items():
        properties = {}
        for field_name, field_spec in type_spec.get("properties", {}).items():
            properties[snake_to_camel(field_name.rstrip("?"))] = {
                "mapped_type": map_type_to_ts(field_spec["type"]),
                "optional": field_name.endswith("?"),
                "extant": field_spec.get("extant", "required"),
            }
        preprocessed[type_name] = {"properties": properties}
    return preprocessed

def generate_ts_types(parsed_yaml: dict) -> str:
    preprocessed_yaml = preprocess_yaml_for_ts(parsed_yaml)
    template = Template(TS_TEMPLATE)
    return template.render(types=preprocessed_yaml)
