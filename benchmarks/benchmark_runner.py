from benchmarks.prompt_sets import NORMAL_PROMPTS, EDGE_CASE_PROMPTS

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
from runtime.simulator import simulate_request
from metrics.metrics_tracker import MetricsTracker


DEFAULT_MODE = "staged_validation_repair"
COMPARISON_MODES = [
    "single_pass",
    "staged",
    "staged_validation",
    "staged_validation_repair",
]


def _run_mode(prompt, mode, tracker):
    start = tracker.start_timer()
    tracker.record_run()

    try:
        ir = generate_ir(prompt)
        assumptions = generate_assumptions(ir)
        architecture = generate_architecture(ir)
        validation_errors = []

        if mode in {"staged_validation", "staged_validation_repair"}:
            validation_errors.extend(validate_ir(ir))
            validation_errors.extend(validate_schema(ir))

        if validation_errors and mode == "staged_validation_repair":
            tracker.record_validation_failure()
            tracker.record_retry()
            tracker.record_repair()
            ir = repair_ir(
                ir,
                issues=[
                    {
                        "section": "relationships",
                        "message": "Validation failed",
                        "fix": "Normalized relationship types",
                    }
                ]
            )
            validation_errors = []
            validation_errors.extend(validate_ir(ir))
            validation_errors.extend(validate_schema(ir))

        db_schema = generate_db_schema(ir)
        api_schema = generate_api_schema(ir)
        ui_schema = generate_ui_schema(ir)
        auth_schema = generate_auth_schema(ir)
        business_rules = generate_business_rules(ir)

        validation_errors.extend(validate_references(ir, api_schema, ui_schema, auth_schema))
        validation_errors.extend(validate_consistency(ir, api_schema, ui_schema))
        validation_errors.extend(validate_business_rules(ir, business_rules))

        if validation_errors:
            tracker.record_validation_failure()
            tracker.record_failure_type("validation_error")

        result, _ = simulate_request(
            entity_name=ir.entities[0].name.lower(),
            role=ir.roles[0],
            ir=ir,
            api_schema=api_schema,
            auth_schema=auth_schema,
        )

        if result:
            tracker.record_success()
        else:
            tracker.record_failure_type("runtime_simulation_failed")

        generate_final_output(
            ir=ir,
            architecture=architecture,
            assumptions=assumptions,
            db_schema=db_schema,
            api_schema=api_schema,
            ui_schema=ui_schema,
            auth_schema=auth_schema,
            business_rules=business_rules,
            validation_errors=validation_errors,
            repair_logs=[],
        )

    except Exception as e:
        tracker.record_failure_type(type(e).__name__)
        tracker.record_failure_type("runtime_error")

    tracker.stop_timer(start)


def run_benchmarks(mode=DEFAULT_MODE):
    tracker = MetricsTracker()
    prompts = NORMAL_PROMPTS + EDGE_CASE_PROMPTS

    for prompt in prompts:
        _run_mode(prompt, mode, tracker)

    summary = tracker.summary()
    summary["mode"] = mode
    summary["total_runs"] = len(prompts)
    return summary


def run_comparison_benchmarks():
    return {
        mode: run_benchmarks(mode)
        for mode in COMPARISON_MODES
    }
