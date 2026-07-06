# AI Workflow Platform — Current Architecture Summary

## Overview

The platform currently implements the foundational architecture of a workflow orchestration engine.

Although the individual step handlers are still placeholders, the orchestration layer itself has already evolved into a legitimate DAG-based execution system.

The system currently consists of the following major architectural subsystems:

1. Workflow Definition Layer
2. Workflow Execution Engine
3. State Machine System
4. DAG Scheduler
5. Condition Evaluation System
6. Context Propagation System
7. Template Resolution System
8. Step Handler Runtime System
9. Typed Configuration Layer

---

# 1. Workflow Definition Layer

This layer defines the static structure of workflows.

Core models:

* `Workflow`
* `WorkflowStep`
* `WorkflowRun`
* `WorkflowStepRun`

The workflow definition layer is responsible for:

* defining workflow templates
* defining workflow steps
* defining dependency relationships
* storing step configurations
* tracking runtime execution state

---

## Workflow Model

The `Workflow` model represents the logical workflow template.

It acts as the blueprint for execution.

Conceptually:

```text
Workflow
 ├── Step A
 ├── Step B
 └── Step C
```

The workflow itself is not execution state.

It is only the reusable workflow definition.

---

## WorkflowStep Model

The `WorkflowStep` model represents a node within the workflow DAG.

Responsibilities:

* step type definition
* dependency definition
* execution ordering
* conditional execution
* runtime configuration storage

Current important fields:

```python
step_type
config
depends_on
condition
order
```

The step model effectively acts as the platform DSL (Domain Specific Language).

It defines:

* what executes
* when it executes
* what it depends on
* how it executes

---

## WorkflowRun Model

The `WorkflowRun` model represents a runtime execution instance of a workflow.

Example:

```text
Workflow Template
        ↓
WorkflowRun #1
WorkflowRun #2
WorkflowRun #3
```

This separation between template and runtime execution is foundational to orchestration systems.

It enables:

* execution history
* retries
* monitoring
* analytics
* auditing

---

## WorkflowStepRun Model

The `WorkflowStepRun` model represents execution state for a single step during a workflow run.

Responsibilities:

* tracking lifecycle state
* tracking timestamps
* storing outputs
* storing errors

Conceptually:

```text
WorkflowRun
 ├── StepRun A
 ├── StepRun B
 └── StepRun C
```

This becomes the runtime execution graph of the workflow.

---

# 2. Workflow Execution Engine

The execution engine is implemented through:

```python
execute_workflow()
```

This is the orchestration core of the platform.

Responsibilities:

* workflow lifecycle management
* DAG traversal
* dependency scheduling
* condition evaluation
* step execution
* failure handling
* state transitions
* execution context propagation

---

## Execution Lifecycle

Current execution flow:

```text
Create WorkflowRun
        ↓
Load WorkflowSteps
        ↓
Validate DAG
        ↓
Build Scheduler State
        ↓
Scheduler Loop
        ↓
Find Runnable Steps
        ↓
Execute Steps
        ↓
Update Runtime State
        ↓
Complete Workflow
```

---

# 3. State Machine System

The platform uses a centralized state machine system for lifecycle management.

Instead of mutating statuses directly, all lifecycle transitions are controlled through:

```python
transition_run()
```

This centralizes orchestration rules and prevents invalid state changes.

---

## Current Run Lifecycle

Current supported transitions:

```text
PENDING → RUNNING
RUNNING → COMPLETED
RUNNING → FAILED
PENDING → SKIPPED
```

Benefits:

* lifecycle integrity
* invalid transition prevention
* centralized transition rules
* automated timestamp management

---

## Timestamp Automation

The state machine automatically manages:

```python
started_at
completed_at
```

This is important because timestamps are lifecycle concerns and therefore belong inside the state machine layer.

---

# 4. DAG Scheduler Architecture

The workflow engine currently executes workflows as DAGs (Directed Acyclic Graphs).

The scheduler maintains runtime orchestration state through:

```python
pending_steps
completed_steps
failed_steps
```

These structures act as scheduler memory.

---

## Dependency Resolution

Dependency scheduling is implemented through:

```python
dependencies_satisfied()
```

This determines whether a step is eligible for execution.

Example:

```text
Step B depends on Step A
Step C depends on Step B
```

The scheduler dynamically determines:

* what can execute
* what must wait
* what becomes blocked

---

## Scheduler Loop

Current scheduler loop:

```python
while pending_steps:
```

Each iteration:

* evaluates workflow state
* finds runnable nodes
* schedules execution

This forms the orchestration core.

---

## Runnable Step Discovery

Runnable steps are dynamically discovered based on dependency state.

Conceptually:

```text
completed_steps
        ↓
dependency evaluation
        ↓
runnable_steps
```

---

## Deadlock Detection

Deadlock protection currently exists through:

```python
if not runnable_steps:
    raise Exception(...)
```

This prevents:

* cyclic dependencies
* permanently blocked workflows
* infinite scheduling loops

---

## Failure Propagation

The scheduler supports dependency failure propagation.

Example:

```text
Step A fails
        ↓
Dependent Step B becomes skipped
```

This prevents workflows from hanging indefinitely on impossible dependencies.

---

# 5. Condition Evaluation System

The platform supports conditional execution through:

```python
if step.condition:
```

Conditions are evaluated dynamically during execution.

Example:

```text
IF build succeeds
THEN deploy
```

This allows workflows to support dynamic branching behavior instead of static execution.

---

# 6. Context Propagation System

The workflow engine maintains runtime execution context through:

```python
context = {}
```

Step outputs are stored using:

```python
context[step.name] = output
```

This enables inter-step communication.

Example:

```text
Step A creates repository
        ↓
Step B uses repository URL
        ↓
Step C deploys repository
```

Without context propagation, workflows cannot compose behavior across steps.

---

# 7. Template Resolution System

The platform includes runtime template resolution.

Example:

```text
{{step_name.output}}
```

This allows workflow configurations to dynamically reference outputs from previous steps.

The template system effectively acts as the workflow expression system.

---

# 8. Step Handler Runtime System

Step execution is delegated through a registry architecture.

Current registry:

```python
STEP_REGISTRY = {
    "echo": execute_echo_step,
    "http": execute_http_step,
    "github_repo": execute_github_step
}
```

This forms the runtime plugin architecture.

---

## Runtime Execution Pipeline

Current execution flow:

```text
Workflow Engine
    ↓
Step Registry
    ↓
Step Handler
    ↓
External System/API
```

Responsibilities are separated cleanly:

### Orchestrator

Responsible for:

* scheduling
* lifecycle management
* dependency handling

### Step Handlers

Responsible for:

* performing work
* interacting with external systems
* returning execution outputs

---

# 9. Typed Configuration Layer

The platform uses typed configuration models:

```python
HttpStepConfig
EchoStepConfig
```

This replaces arbitrary configuration blobs with validated execution contracts.

Benefits:

* validation
* type safety
* predictable execution
* cleaner handler implementations
