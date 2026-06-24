import json

from generators.ir_generator import generate_ir
from generators.assumption_generator import generate_assumptions
from generators.architecture_generator import generate_architecture
from generators.db_generator import generate_db_schema
from generators.api_generator import generate_api_schema
from generators.ui_generator import generate_ui_schema
from generators.auth_generator import generate_auth_schema
from generators.business_rules_generator import generate_business_rules
from generators.final_output_generator import generate_final_output

from validators.ir_validator import validate_ir
from validators.schema_validator import validate_schema
from validators.reference_validator import validate_references
from validators.consistency_validator import validate_consistency
from validators.business_rule_validator import validate_business_rules

from repair.repair_engine import repair_ir
from repair.repair_log import RepairLog

from runtime.simulator import simulate_request


requirement = """
Build a CRM with login, contacts, dashboard,
role-based access and premium plans.
"""

repair_log = RepairLog()

# Generate IR

ir = generate_ir(requirement)
assumptions = generate_assumptions(ir)
architecture = generate_architecture(ir)

# Initial validation

validation_errors = []
validation_errors.extend(validate_ir(ir))
validation_errors.extend(validate_schema(ir))

# Repair if needed

if validation_errors:

    ir = repair_ir(
        ir,
        repair_log,
        issues=[{"section": "relationships", "message": "IR validation failed", "fix": "Normalized invalid relationships"}]
    )

# Revalidate after repair

validation_errors = []
validation_errors.extend(validate_ir(ir))
validation_errors.extend(validate_schema(ir))

# Generate schemas

db_schema = generate_db_schema(ir)

api_schema = generate_api_schema(ir)

ui_schema = generate_ui_schema(ir)

auth_schema = generate_auth_schema(ir)

business_rules = generate_business_rules(ir)

# Consistency validation

consistency_errors = validate_consistency(
    ir,
    api_schema,
    ui_schema
)

validation_errors.extend(
    consistency_errors
)

validation_errors.extend(
    validate_references(
        ir,
        api_schema,
        ui_schema,
        auth_schema
    )
)

validation_errors.extend(
    validate_business_rules(
        ir,
        business_rules
    )
)

# Runtime simulation

result, message = simulate_request(
    entity_name="contact",
    role="Admin",
    ir=ir,
    api_schema=api_schema,
    auth_schema=auth_schema
)

print("\n=== RUNTIME SIMULATION ===")
print("Result:", result)
print("Message:", message)

# Final output

final_output = generate_final_output(
    ir=ir,
    architecture=architecture,
    assumptions=assumptions,
    db_schema=db_schema,
    api_schema=api_schema,
    ui_schema=ui_schema,
    auth_schema=auth_schema,
    business_rules=business_rules,
    validation_errors=validation_errors,
    repair_logs=repair_log.get_repairs()
)

print("\n=== FINAL COMPILER OUTPUT ===\n")

print(
    json.dumps(
        final_output,
        indent=2
    )
)
