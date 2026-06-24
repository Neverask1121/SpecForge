from models.ir_schema import IR


def repair_ir(ir: IR, repair_log=None, issues=None):
    issues = issues or []

    for issue in issues:
        section = issue.get("section", "ir")
        message = issue.get("message", "Unknown issue")
        fix = issue.get("fix", "Applied safe normalization")

        if repair_log:
            repair_log.add(message, fix, section)

        if section == "relationships":
            for rel in ir.relationships:
                if rel.relation_type == "many_to_one":
                    rel.relation_type = "one_to_many"

        if section == "roles":
            ir.roles = [role.strip() for role in ir.roles if role.strip()]

    return ir
