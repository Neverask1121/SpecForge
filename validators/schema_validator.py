from models.ir_schema import IR


def validate_schema(ir: IR):
    errors = []

    if not ir.app_name or not ir.app_name.strip():
        errors.append("App name is required")

    if not ir.entities:
        errors.append("At least one entity is required")

    for entity in ir.entities:
        if not entity.name or not entity.name.strip():
            errors.append("Entity name is required")
        if not entity.fields:
            errors.append(f"Entity {entity.name} must include at least one field")

    if not ir.roles:
        errors.append("At least one role is required")

    return errors
