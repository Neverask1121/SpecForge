def validate_business_rules(ir, business_rules):
    errors = []
    entity_names = {entity.name.lower() for entity in ir.entities}

    if "user" in entity_names and not any("authenticated" in rule.lower() for rule in business_rules):
        errors.append("User entity requires an authentication business rule")

    if "contact" in entity_names and not any("unique" in rule.lower() for rule in business_rules):
        errors.append("Contact entity requires a uniqueness business rule")

    if "subscription" in entity_names and not any("subscription" in rule.lower() for rule in business_rules):
        errors.append("Subscription entity requires a premium access rule")

    return errors
