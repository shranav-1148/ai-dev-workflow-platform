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
    '''
        This is the workflow execution engine.
        Responsible for orchestrating the exectuion lifecycle of an entire workflow.
        - Create workflow run
        - load workflow steps
        - evaluate step conditions
        - execute step handlers
        - stores outputs in execution context
        - creates step execution records
        - handles failures
        - updates lifeyce states
    '''
    run = WorkflowRun(
        workflow_id = workflow.id,
        status=RunStatus.PENDING
    )

    db.add(run)
    db.commit()
    transition_run(
        run,
        RunStatus.RUNNING
    )

    db.commit()
    db.refresh(run)

    steps = (
        db.query(WorkflowStep)
        .filter(
            WorkflowStep.workflow_id == workflow.id
        )
        .order_by(WorkflowStep.order)
        .all()
    )

    valid_step_ids = {
        step.id
        for step in steps
    }
    for step in steps:
        if not step.depends_on:
            continue

        for dep_id in step.depends_on:
            if dep_id not in valid_step_ids:

                transition_run(
                    run, RunStatus.FAILED
                )
                db.commit()

                raise Exception(
                    f"Step {step.id} depends on non-existent step {dep_id}"
                )



    context= {}

    completed_steps = set()

    failed_steps = set()
    
    pending_steps = {
        step.id: step
        for step in steps
    }
    
    while pending_steps:
        runnable_steps = []


        for step in list(pending_steps.values()):
            # Dependency check to decide if tasks can be runnable
            if has_failed_dependency(step, failed_steps):

                step_run = WorkflowStepRun(
                    workflow_run_id=run.id,
                    workflow_step_id=step.id,
                    status=RunStatus.PENDING
                )

                db.add(step_run)
                db.commit()
                db.refresh(step_run)

                transition_run(
                    step_run,
                    RunStatus.SKIPPED
                )

                step_run.error_message = "Dependency failed"

                db.commit()
                pending_steps.pop(step.id, None)
                completed_steps.add(step.id)
                continue
            if dependencies_satisfied(step, completed_steps):
                runnable_steps.append(step)


        # Runnable check
        if not runnable_steps:
            transition_run(run, RunStatus.FAILED)
            db.commit()
            raise Exception("Deadlocked DAG detected")

        for step in runnable_steps:

            if step.condition:
                '''If there is a condition set and the condition is not met
                Create a step Run with Pending status but change it immediately
                to skipped'''
                if not evaluate_conditions(step.condition, context):
                    step_run = WorkflowStepRun(
                    workflow_run_id = run.id,
                    workflow_step_id = step.id,
                    status= RunStatus.PENDING
                    )

                    db.add(step_run)
                    db.commit()
                    db.refresh(step_run)

                    transition_run(
                        step_run,
                        RunStatus.SKIPPED
                    )
                    step_run.error_message = "Condition evaluated to false"
                    db.commit() 
                    completed_steps.add(step.id)
                    pending_steps.pop(step.id, None)

                    continue
        
            step_run = None
            try:
                step_run = WorkflowStepRun(
                    workflow_run_id = run.id,
                    workflow_step_id = step.id,
                    status= RunStatus.PENDING
                )

                db.add(step_run)
                db.commit()
                db.refresh(step_run)

                transition_run(
                    step_run,
                    RunStatus.RUNNING
                )
            
                db.commit()

                # Placeholder execution
                output = execute_step(step, step_run, context)

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
                if step_run:
                
                    transition_run(
                        step_run,
                        RunStatus.FAILED
                    )
                    step_run.error_message = str(e)
                    db.commit()
                    pending_steps.pop(step.id, None)
                    failed_steps.add(step.id)

                transition_run(
                    run, RunStatus.FAILED
                )
                db.commit()
                raise
    
    if run.status != RunStatus.FAILED:
        transition_run(
        run, RunStatus.COMPLETED
        )

    db.commit()
    db.refresh(run)

    return run


