from models.ir_schema import IR


def repair_ir(ir: IR, repair_log=None):

    for rel in ir.relationships:

        if rel.relation_type == "many_to_one":

            if repair_log:
                repair_log.add(
                    "Invalid relation type: many_to_one",
                    "Converted to one_to_many"
                )

            rel.relation_type = "one_to_many"

    return ir