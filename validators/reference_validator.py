def validate_references(ir, api_schema, ui_schema, auth_schema):
    errors = []

    entity_names = {entity.name.lower() for entity in ir.entities}
    api_paths = {endpoint["path"].split("/")[1].split("{")[0] for endpoint in api_schema if endpoint.get("path")}
    ui_routes = {page["route"].split("/")[1].rstrip("s") for page in ui_schema.get("pages", []) if page.get("route")}
    auth_roles = set(auth_schema.get("roles", {}).keys())

    for entity in entity_names:
        if entity not in api_paths:
            errors.append(f"Missing API reference for entity: {entity}")
        if entity not in ui_routes and f"{entity}s" not in ui_routes:
            errors.append(f"Missing UI reference for entity: {entity}")

    for role in ir.roles:
        if role not in auth_roles:
            errors.append(f"Missing auth reference for role: {role}")

    return errors
