from models.ir_schema import IR


TYPE_MAPPING = {
    "string": "VARCHAR(255)",
    "integer": "INTEGER",
    "float": "FLOAT",
    "date": "DATE"
}


def generate_db_schema(ir: IR):

    sql = []

    for entity in ir.entities:

        table_lines = []

        for field in entity.fields:

            field_type = TYPE_MAPPING.get(
                field.type.lower(),
                "TEXT"
            )

            nullable = ""

            if field.required:
                nullable = " NOT NULL"

            table_lines.append(
                f"    {field.name} {field_type}{nullable}"
            )

        table_sql = (
            f"CREATE TABLE {entity.name} (\n"
            + ",\n".join(table_lines)
            + "\n);"
        )

        sql.append(table_sql)

    return "\n\n".join(sql)