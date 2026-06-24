from models.ir_schema import IR


VALID_RELATIONS = {
    "one_to_one",
    "one_to_many",
    "many_to_many"
}


def validate_ir(ir: IR):

    errors = []

    entity_names = {
        entity.name
        for entity in ir.entities
    }

    for rel in ir.relationships:

        if rel.source not in entity_names:
            errors.append(
                f"Unknown source entity: {rel.source}"
            )

        if rel.target not in entity_names:
            errors.append(
                f"Unknown target entity: {rel.target}"
            )

        if rel.relation_type not in VALID_RELATIONS:
            errors.append(
                f"Invalid relation type: {rel.relation_type}"
            )

    if not ir.app_name or not ir.app_name.strip():
        errors.append("App name is required")

    if not ir.entities:
        errors.append("At least one entity is required")

    if not ir.roles:
        errors.append("At least one role is required")

    return errors
