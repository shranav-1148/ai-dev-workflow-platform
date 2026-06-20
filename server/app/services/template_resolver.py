import re

def resolve_templates(value, context):
    if not isinstance(value, str):
        return value
    
    matches = re.findall(r"\{\{(.*?)\}\}", value)

    for match in matches:
        parts = match.strip().split(".")

        current = context

        for part in parts:
            current = current.get(part)

            if current is None:
                raise Exception(
                    f"Unable to resolve template: {match}"
                )
            
            value = value.replace(
                f"{{{{{match}}}}}",
                str(current)
            )

    return value