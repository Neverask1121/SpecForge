# AI Application Compiler - Viva Notes

## Project Overview

The AI Application Compiler converts natural language product requirements into a structured, executable application specification.

Instead of generating everything in one step, it follows a staged compiler architecture with validation, repair, consistency checking, and execution simulation.

---

# System Pipeline

Requirement
→ IR Generator
→ Validator
→ Repair Engine
→ Database Generator
→ API Generator
→ UI Generator
→ Auth Generator
→ Business Rules Generator
→ Consistency Validator
→ Runtime Simulator
→ Final JSON Output

---

# Core Components

## 1. IR Generator

Purpose:

Converts natural language requirements into a structured Intermediate Representation (IR).

Example:

Input:

Build a CRM with login, contacts, dashboard and premium plans.

Output:

* Entities
* Roles
* Permissions
* Relationships
* Workflows

Why?

The IR acts as the central representation used by all later stages.

---

## 2. Validator

Purpose:

Detect invalid structures before generation continues.

Checks:

* Invalid relationships
* Missing references
* Incorrect schema formats
* Broken entity references

Example:

many_to_one

Detected as invalid.

---

## 3. Repair Engine

Purpose:

Fix only the broken section instead of regenerating everything.

Example:

Issue:

many_to_one

Repair:

one_to_many

Why?

Partial repair is faster, cheaper, and more deterministic than full regeneration.

---

## 4. Repair Log

Purpose:

Maintain a record of every repair performed.

Example:

{
"issue": "Invalid relation type: many_to_one",
"fix": "Converted to one_to_many"
}

---

## 5. Database Generator

Purpose:

Convert IR entities into SQL database schema.

Example:

User entity

↓

CREATE TABLE User (...)

---

## 6. API Generator

Purpose:

Generate REST API endpoints.

Example:

GET /user

POST /user

PUT /user/{id}

DELETE /user/{id}

---

## 7. UI Generator

Purpose:

Generate application page structure.

Example:

UserList

UserDetail

UserCreate

Routes:

/users

/users/:id

/users/create

---

## 8. Auth Generator

Purpose:

Generate role-based access control (RBAC).

Example:

Admin

* dashboard
* contacts
* plans

User

* dashboard
* contacts

---

## 9. Business Rules Generator

Purpose:

Generate application business constraints.

Examples:

* User must be authenticated before accessing protected resources.
* Contact email must be unique.
* Subscription must exist before premium access.
* Plan price must be greater than zero.

---

## 10. Consistency Validator

Purpose:

Verify generated schemas are consistent.

Checks:

* UI ↔ API consistency
* API ↔ Database consistency
* Role ↔ Permission consistency
* Reference consistency

Example:

If a UI page exists for Contacts but no Contact API exists, validation fails.

---

## 11. Runtime Simulator

Purpose:

Simulate execution before accepting the generated architecture.

Checks:

Entity Exists
↓
API Exists
↓
Permission Exists
↓
Executable

Example Output:

Result: True

Message: Request executable

---

## 12. Metrics Tracker

Purpose:

Measure system reliability.

Tracks:

* Success Rate
* Validation Failures
* Repairs Applied
* Average Latency

Example:

{
"total_runs": 20,
"success_rate": 95,
"validation_failures": 4,
"repairs": 4
}

---

## 13. Benchmark Runner

Purpose:

Evaluate the compiler on multiple prompts.

Includes:

* Normal prompts
* Edge-case prompts

Examples:

Normal:

* CRM
* E-commerce
* LMS
* Hospital System

Edge Cases:

* Empty requirement
* Circular relationships
* Missing entities
* Conflicting requirements

---

# Final Output Format

```json
{
  "app": {},
  "assumptions": {},
  "ui": {},
  "api": {},
  "database": {},
  "auth": {},
  "business_logic": {},
  "validation": {},
  "repairs": {}
}
```

---

# Frequently Asked Viva Questions

## Q1. Why not use a single prompt?

Answer:

Single-pass generation is unreliable.

A staged compiler architecture allows validation, repair, consistency checking, and execution simulation before producing the final output.

---

## Q2. What is IR?

Answer:

IR stands for Intermediate Representation.

It is the structured application model generated from natural language requirements.

All later stages consume the IR.

---

## Q3. Why use validators?

Answer:

Validators detect:

* Invalid relationships
* Missing references
* Broken schemas
* Inconsistencies

before application generation continues.

---

## Q4. Why repair instead of regenerating?

Answer:

Repairing only the affected section:

* Reduces cost
* Reduces latency
* Improves determinism
* Preserves valid generated sections

---

## Q5. What does the Runtime Simulator do?

Answer:

The Runtime Simulator performs a dry run of the generated architecture.

It validates:

UI → API → Database → Authorization

before accepting the architecture.

---

## Q6. What is the biggest advantage of this architecture?

Answer:

Reliability.

The system does not trust the LLM output directly.

Every stage is validated, repaired if necessary, checked for consistency, and tested for executability.

---

## Q7. How is this different from a chatbot?

Answer:

A chatbot generates text.

This system generates structured application specifications through a compiler pipeline consisting of generation, validation, repair, consistency checking, and execution simulation.

---

## Project Status

Implemented:

✓ IR Generator

✓ Validator

✓ Repair Engine

✓ Repair Logs

✓ Database Generator

✓ API Generator

✓ UI Generator

✓ Auth Generator

✓ Business Rules Generator

✓ Consistency Validator

✓ Runtime Simulator

✓ Metrics Tracker

✓ Benchmark Runner

✓ Final JSON Output

Priority Achieved:

Reliability > Executability > Consistency > Cost > Speed
