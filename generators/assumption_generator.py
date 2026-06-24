from models.ir_schema import IR


def generate_assumptions(ir: IR):
    assumptions = [
        "Generated automatically from the provided requirement",
        "Entities map to CRUD-style APIs and list/detail/create UI pages",
    ]

    if any(entity.name.lower() == "user" for entity in ir.entities):
        assumptions.append("Users are authenticated through role-based access control")

    return assumptions
