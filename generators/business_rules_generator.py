from models.ir_schema import IR


def generate_business_rules(ir: IR):

    rules = []

    entity_names = {
        entity.name.lower()
        for entity in ir.entities
    }

    if "user" in entity_names:
        rules.append(
            "User must be authenticated before accessing protected resources"
        )

    if "contact" in entity_names:
        rules.append(
            "Contact email must be unique"
        )

    if "subscription" in entity_names:
        rules.append(
            "Subscription must exist before premium access"
        )

    if "plan" in entity_names:
        rules.append(
            "Plan price must be greater than zero"
        )

    return rules