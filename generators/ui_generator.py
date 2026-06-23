from models.ir_schema import IR


def generate_ui_schema(ir: IR):

    pages = []

    for entity in ir.entities:

        name = entity.name

        pages.append({
            "name": f"{name}List",
            "route": f"/{name.lower()}s"
        })

        pages.append({
            "name": f"{name}Detail",
            "route": f"/{name.lower()}s/:id"
        })

        pages.append({
            "name": f"{name}Create",
            "route": f"/{name.lower()}s/create"
        })

    return {
        "pages": pages
    }