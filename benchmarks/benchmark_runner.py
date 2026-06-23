from benchmarks.prompt_sets import (
    NORMAL_PROMPTS,
    EDGE_CASE_PROMPTS
)

from generators.ir_generator import generate_ir
from generators.api_generator import generate_api_schema
from generators.ui_generator import generate_ui_schema
from generators.auth_generator import generate_auth_schema

from validators.ir_validator import validate_ir
from validators.consistency_validator import validate_consistency

from repair.repair_engine import repair_ir

from runtime.simulator import simulate_request

from metrics.metrics_tracker import MetricsTracker


def run_benchmarks():

    tracker = MetricsTracker()

    prompts = NORMAL_PROMPTS + EDGE_CASE_PROMPTS

    failure_types = {}

    for prompt in prompts:

        start = tracker.start_timer()

        try:

            ir = generate_ir(prompt)

            errors = validate_ir(ir)

            if errors:

                tracker.record_validation_failure()

                tracker.record_repair()

                ir = repair_ir(ir)

            api_schema = generate_api_schema(ir)

            ui_schema = generate_ui_schema(ir)

            auth_schema = generate_auth_schema(ir)

            consistency_errors = validate_consistency(
                ir,
                api_schema,
                ui_schema
            )

            if consistency_errors:

                failure_types["consistency_error"] = (
                    failure_types.get(
                        "consistency_error",
                        0
                    ) + 1
                )

            result, message = simulate_request(
                entity_name=ir.entities[0].name.lower(),
                role=ir.roles[0],
                ir=ir,
                api_schema=api_schema,
                auth_schema=auth_schema
            )

            if result:
                tracker.record_success()

        except Exception as e:

            error_name = type(e).__name__

            failure_types[error_name] = (
                failure_types.get(
                    error_name,
                    0
                ) + 1
            )

        tracker.stop_timer(start)

    return tracker.summary(), failure_types