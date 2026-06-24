from models.ir_schema import IR


def generate_architecture(ir: IR):
    return {
        "entities": [
            {
                "name": entity.name,
                "fields": [field.model_dump() for field in entity.fields],
            }
            for entity in ir.entities
        ],
        "roles": ir.roles,
        "relationships": [relationship.model_dump() for relationship in ir.relationships],
        "workflows": [workflow.model_dump() for workflow in ir.workflows],
    }
