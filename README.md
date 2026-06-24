# AI Application Compiler

AI Application Compiler turns a natural-language product requirement into a staged application specification.

## Architecture

The repository now follows the required pipeline:

Requirement
-> IR
-> Architecture
-> UI/API/DB/Auth
-> Business Rules
-> Validation
-> Repair
-> Runtime Simulation
-> Final JSON

### Core stages

- `generators/ir_generator.py` creates the structured IR.
- `generators/assumption_generator.py` derives explicit assumptions.
- `generators/architecture_generator.py` summarizes entities, roles, relationships, and workflows.
- `generators/db_generator.py`, `generators/api_generator.py`, `generators/ui_generator.py`, and `generators/auth_generator.py` build the domain schemas.
- `generators/business_rules_generator.py` produces business rules.
- `validators/` contains IR, schema, reference, consistency, and business-rule validation.
- `repair/repair_engine.py` applies section-scoped repairs and logs every repair.
- `runtime/simulator.py` checks the UI -> API -> DB -> Auth -> Business Rules chain.
- `metrics/metrics_tracker.py` records success rate, validation pass rate, retries, latency, and failure types.

## Pipeline

1. Generate IR from the requirement.
2. Generate assumptions and architecture.
3. Generate UI, API, DB, Auth, and business rules.
4. Validate JSON structure, schema, references, consistency, and business rules.
5. Repair only the affected section when validation fails.
6. Revalidate after repair.
7. Simulate runtime execution.
8. Emit the final JSON payload.

## Usage

Run the main compiler flow:

```bash
python main.py
```

Run benchmarks:

```bash
python -m benchmarks.benchmark_runner
```

Benchmark defaults to 20 total runs across `10 normal + 10 edge` prompts.

Comparison modes are available through `run_comparison_benchmarks()`:

- `single_pass`
- `staged`
- `staged_validation`
- `staged_validation_repair`

## Example Output

```json
{
  "app": {
    "name": "CRM"
  },
  "assumptions": [
    "Generated automatically from the provided requirement"
  ],
  "architecture": {
    "entities": [],
    "roles": [],
    "relationships": [],
    "workflows": []
  },
  "ui": {},
  "api": [],
  "database": "",
  "auth": {
    "roles": {}
  },
  "business_logic": [],
  "validation": {
    "errors": [],
    "passed": true
  },
  "repairs": []
}
```

## Benchmark Results

The benchmark runner reports:

- `success_rate`
- `validation_pass_rate`
- `retries`
- `latency`
- `failure_types`

The exact values depend on the generated IR and runtime simulation results for the current prompt set.

## Limitations

- The compiler still depends on an upstream LLM for IR generation.
- Runtime simulation is intentionally lightweight and checks structural compatibility rather than executing a full backend.
- Benchmark quality depends on prompt quality and the consistency of the generated IR.
- The final JSON is structured for downstream consumption, not direct deployment.
