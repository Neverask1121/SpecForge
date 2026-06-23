def generate_final_output(
    ir,
    db_schema,
    api_schema,
    ui_schema,
    auth_schema,
    business_rules,
    validation_errors,
    repair_logs
):

    return {

        "app": {
            "name": ir.app_name
        },

        "assumptions": [
            "Generated automatically from requirement"
        ],

        "ui": ui_schema,

        "api": api_schema,

        "database": db_schema,

        "auth": auth_schema,

        "business_logic": business_rules,

        "validation": {
            "errors": validation_errors,
            "passed": len(validation_errors) == 0
        },

        "repairs": repair_logs
    }