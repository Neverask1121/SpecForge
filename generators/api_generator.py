from models.ir_schema import IR


def generate_api_schema(ir: IR):

    api = []

    for entity in ir.entities:

        name = entity.name.lower()

        api.extend([
            {
                "method": "GET",
                "path": f"/{name}"
            },
            {
                "method": "GET",
                "path": f"/{name}/{{id}}"
            },
            {
                "method": "POST",
                "path": f"/{name}"
            },
            {
                "method": "PUT",
                "path": f"/{name}/{{id}}"
            },
            {
                "method": "DELETE",
                "path": f"/{name}/{{id}}"
            }
        ])

    return api