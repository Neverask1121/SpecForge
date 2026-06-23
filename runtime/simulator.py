def simulate_request(
    entity_name,
    role,
    ir,
    api_schema,
    auth_schema
):

    entity_exists = False

    for entity in ir.entities:

        if entity.name.lower() == entity_name.lower():
            entity_exists = True
            break

    if not entity_exists:
        return False, "Entity not found"

    api_exists = False

    for endpoint in api_schema:

        if endpoint["path"] == f"/{entity_name.lower()}":
            api_exists = True
            break

    if not api_exists:
        return False, "API endpoint missing"

    role_permissions = auth_schema["roles"].get(
        role,
        []
    )

    permission_match = False

    for permission in role_permissions:

        if permission.lower().rstrip("s") == entity_name.lower().rstrip("s"):
            permission_match = True
            break

    if not permission_match:
        return False, "Permission denied"

    return True, "Request executable"