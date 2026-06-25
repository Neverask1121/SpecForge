import json
import os
from pathlib import Path


def _load_env_file():
    env_path = Path(__file__).with_name(".env")
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


_load_env_file()

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


def compile_requirement(requirement: str):
    repair_log = RepairLog()

    ir = generate_ir(requirement)
    assumptions = generate_assumptions(ir)
    architecture = generate_architecture(ir)

    validation_errors = []
    validation_errors.extend(validate_ir(ir))
    validation_errors.extend(validate_schema(ir))

    if validation_errors:
        ir = repair_ir(
            ir,
            repair_log,
            issues=[{"section": "relationships", "message": "IR validation failed", "fix": "Normalized invalid relationships"}]
        )

    validation_errors = []
    validation_errors.extend(validate_ir(ir))
    validation_errors.extend(validate_schema(ir))

    db_schema = generate_db_schema(ir)
    api_schema = generate_api_schema(ir)
    ui_schema = generate_ui_schema(ir)
    auth_schema = generate_auth_schema(ir)
    business_rules = generate_business_rules(ir)

    validation_errors.extend(validate_consistency(ir, api_schema, ui_schema))
    validation_errors.extend(validate_references(ir, api_schema, ui_schema, auth_schema))
    validation_errors.extend(validate_business_rules(ir, business_rules))

    runtime_result = simulate_request(
        entity_name=ir.entities[0].name.lower(),
        role="Admin" if "Admin" in ir.roles else ir.roles[0],
        ir=ir,
        api_schema=api_schema,
        auth_schema=auth_schema
    )

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

    return {
        "final_output": final_output,
        "runtime": {
            "result": runtime_result[0],
            "message": runtime_result[1]
        }
    }


def compile_requirement_json(requirement: str):
    return json.dumps(compile_requirement(requirement)["final_output"], indent=2)
