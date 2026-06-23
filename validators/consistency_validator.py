def validate_consistency(ir, api_schema, ui_schema):

    errors = []

    entity_names = {
        entity.name.lower()
        for entity in ir.entities
    }

    api_paths = {
        endpoint["path"].split("/")[1].split("{")[0]
        for endpoint in api_schema
        if len(endpoint["path"].split("/")) > 1
    }

    for entity in entity_names:

        if entity not in api_paths:
            errors.append(
                f"Missing API for entity: {entity}"
            )

    return errors