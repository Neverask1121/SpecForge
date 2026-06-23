from models.ir_schema import IR


def generate_auth_schema(ir: IR):

    auth = {}

    for role in ir.roles:

        auth[role] = []

    for permission in ir.permissions:

        if permission.permission == "allow":

            auth[permission.role].append(
                permission.feature
            )

    return {
        "roles": auth
    }