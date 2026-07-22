from app.models.workflowRun import WorkflowRun
from app.models.workflowStep import WorkflowStep
from app.models.workflowStepRun import WorkflowStepRun
from server.app.schemas.RunStatus import RunStatus
from app.models.workflow import Workflow
from sqlalchemy.orm import Session
from app.services.step_executor import execute_step
from app.services.condition_evaluator import evaluate_conditions
from app.services.state_machine import transition_run

def dependencies_satisfied(step, completed_steps):
    """
        Determines whether all dependencies for a step
        have successfully completed.
    """
    if not step.depends_on:
        return True

    return all(
        dep_id in completed_steps
        for dep_id in step.depends_on
    )

def has_failed_dependency(step, failed_steps):
    """
        Determines whether any dependency for a step has failed.
    """
    if not step.depends_on:
        return False
    
    return any(
        dep_id in failed_steps
        for dep_id in step.depends_on
    )


def validate_workflow_dependencies(steps):
    """
        Validates that all dependency references point to existing workflow steps
    """

    valid_step_ids = {
        step.id
        for step in steps
    }

    for step in steps:
        if not step.depends_on:
            continue

        for dep_id in step.depends_on:
            if dep_id not in valid_step_ids:
                raise Exception(
                    f"Step {step.id} depends on non-existent step {dep_id}"
                )
            
def create_step_run(
        db,
        run, step
):
    """
        Creates a new workflow step run in PENDING state
    """
    step_run = WorkflowStepRun(
            workflow_run_id=run.id, 
            workflow_step_id=step.id, 
            status=RunStatus.PENDING 
        ) 
    db.add(step_run) 
    db.commit() 
    db.refresh(step_run) 
    
    return step_run

def execute_workflow(
        workflow: Workflow,
        db: Session
):
    
    """
        Workflow DAG execution engine.
    """


    # Create workflow run
    run = WorkflowRun(
        workflow_id = workflow.id,
        status=RunStatus.PENDING
    )

    db.add(run)
    db.commit()
    db.refresh(run)

    transition_run(
        run,
        RunStatus.RUNNING
    )

    db.commit()


    # Load workflow steps

    steps = (
        db.query(WorkflowStep)
        .filter(
            WorkflowStep.workflow_id == workflow.id
        )
        .order_by(WorkflowStep.order)
        .all()
    )

    # Validate DAG: all the steps have dependencies on steps that exist

    try:
        validate_workflow_dependencies(steps)

    except Exception:
        transition_run(
            run,
            RunStatus.FAILED
        )

        db.commit()
        raise

    # Execution state: Executing the workflow

    context = {}

    completed_steps = set()
    failed_steps = set()

    pending_steps = {
        step.id: step
        for step in steps
    }

    # DAG scheduler loop: looping over all pending steps 
    while pending_steps:
        runnable_steps = []

        # Handle failed dependencies: skip a step that depends on a failed dependency

        for step in list(pending_steps.values()):
            if not has_failed_dependency(
                step,
                failed_steps
            ):
                continue

            step_run = create_step_run(
                db,
                run,
                step
            )

            transition_run(
                step_run,
                RunStatus.SKIPPED
            )

            step_run.error_message = (
                "Skipped due to failed dependency"
            )

            db.commit()

            completed_steps.add(step.id)
            pending_steps.pop(step.id, None)
        
        # Find Runnable steps: Find all runnable steps on the current state

        for step in pending_steps.values():

            if dependencies_satisfied(
                step,
                completed_steps
            ):
                runnable_steps.append(step)

        
        # Deadlock detection: If a step is not runnable it is a deadlock at this point

        if not runnable_steps:
            transition_run(
                run,
                RunStatus.FAILED
            )

            db.commit()

            raise Exception(
                "Deadlock DAG detected"
            )
        
        # Execute runnable steps: After checking all dependencies run remaining steps

        for step in runnable_steps:

            # Condition evaluation: Evaluate that condition is met

            if step.condition:
                condition_passed = evaluate_conditions(
                    step.condition,
                    context
                )

                if not condition_passed:
                    step_run = create_step_run(
                        db,
                        run,
                        step
                    )

                    transition_run(
                        step_run,
                        RunStatus.SKIPPED
                    )

                    step_run.error_message = (
                        "Condition evaluated to false"
                    )

                    db.commit()

                    completed_steps.add(step.id)
                    pending_steps.pop(step.id, None)

                    continue

            # Step Execution: Execution of step

            step_run = create_step_run(
                db,
                run,
                step
            )

            while True:
                try: 
                    transition_run(
                        step_run,
                        RunStatus.RUNNING
                    )
                    
                    db.commit()
                    
                    output = execute_step(
                        step,
                        step_run,
                        context
                    )
                    
                    context[step.name] = output
                    
                    step_run.output = output
                    transition_run(
                        step_run,
                        RunStatus.COMPLETED
                    )
                    
                    db.commit()
                    
                    completed_steps.add(step.id)
                    
                    pending_steps.pop(step.id, None)
                                
                
                except Exception as e:
                    step_run.attempt_count += 1
                    
                    if step_run.attempt_count > step.retry_policy.max_attempts:
                        if step_run:
                            transition_run(
                                step_run,
                                RunStatus.FAILED
                            )
                        
                            step_run.error_message = str(e)
                        
                            db.commit()
                        
                        failed_steps.add(step.id)
                        pending_steps.pop(step.id, None)
                        
                        transition_run(
                            run,
                            RunStatus.FAILED
                        )
                        
                        db.commit()
                        raise
    
    # Complete workflow: Finish workflow

    if run.status != RunStatus.FAILED:

        transition_run(
            run,
            RunStatus.COMPLETED
        )

        db.commit()
    
    db.refresh(run)

    return run
