import json

from compiler import compile_requirement


if __name__ == "__main__":
    requirement = """
    Build a CRM with login, contacts, dashboard,
    role-based access and premium plans.
    """

    result = compile_requirement(requirement)

    print("\n=== RUNTIME SIMULATION ===")
    print("Result:", result["runtime"]["result"])
    print("Message:", result["runtime"]["message"])

    print("\n=== FINAL COMPILER OUTPUT ===\n")
    print(json.dumps(result["final_output"], indent=2))
