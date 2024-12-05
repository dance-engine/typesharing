import yaml
import re

class ValidationError(Exception):
    """Exception for YAML validation errors."""

def validate_yaml(parsed_yaml: dict):
    """
    Validates the structure and content of the parsed YAML.
    Ensures it meets the requirements for type generation.
    """
    valid_types = {"String", "Integer", "Boolean", "Decimal", "Date"}
    list_pattern = re.compile(r"List<(.+)>")

    if not isinstance(parsed_yaml, dict):
        raise ValidationError("YAML must be a dictionary at the top level.")

    for object_name, object_spec in parsed_yaml.items():
        # Validate top-level object type and properties
        if "type" not in object_spec or object_spec["type"] != "Object":
            raise ValidationError(f"{object_name} must have a type of 'Object'.")
        if "properties" not in object_spec:
            raise ValidationError(f"{object_name} must define 'properties'.")
        if not isinstance(object_spec["properties"], dict) or not object_spec["properties"]:
            raise ValidationError(f"{object_name} must have at least one property.")

        # Validate each property
        for prop_name, prop_spec in object_spec["properties"].items():
            if "type" not in prop_spec:
                raise ValidationError(
                    f"Property '{prop_name}' in {object_name} must have a 'type' defined."
                )

            prop_type = prop_spec["type"]
            # Check if type is valid
            if prop_type not in valid_types and not list_pattern.match(prop_type):
                if prop_type not in parsed_yaml:
                    raise ValidationError(
                        f"Property '{prop_name}' in {object_name} has an invalid type: '{prop_type}'. "
                        "Valid types are String, Integer, Boolean, Decimal, Date, or objects defined in the YAML."
                    )

            # Validate List types
            if list_pattern.match(prop_type):
                inner_type = list_pattern.match(prop_type).group(1)
                if inner_type not in valid_types and inner_type not in parsed_yaml:
                    raise ValidationError(
                        f"List property '{prop_name}' in {object_name} must define a valid inner type: '{inner_type}'."
                    )

            # Validate extant value
            if "extant" in prop_spec and prop_spec["extant"] != "missing":
                raise ValidationError(
                    f"Property '{prop_name}' in {object_name} has an invalid 'extant' value: '{prop_spec['extant']}'. "
                    "The only allowed value is 'missing'."
                )

def parse_yaml(file_path: str) -> dict:
    """
    Parses a YAML file into a dictionary and validates its structure.
    """
    with open(file_path, "r") as file:
        parsed_yaml = yaml.safe_load(file)

    validate_yaml(parsed_yaml)
    return parsed_yaml
