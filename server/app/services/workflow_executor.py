from app.models.workflowRun import WorkflowRun
from app.models.workflowStep import WorkflowStep
from app.models.workflowStepRun import WorkflowStepRun
from app.schemas.StepRunStatus import StepRunStatus
from app.models.workflow import Workflow
from sqlalchemy.orm import Session
from datetime import datetime, UTC
from app.services.step_executor import execute_step
from app.services.condition_evaluator import evaluate_conditions


def execute_workflow(
        workflow: Workflow,
        db: Session
):
    '''Executing a workflow'''
    run = WorkflowRun(
        workflow_id = workflow.id,
        status="running"
    )

    db.add(run)
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

    context= {}

    for step in steps:

        if step.condition:
            if not evaluate_conditions(step.condition, context):
                step_run = WorkflowStepRun(
                    workflow_run_id = run.id,
                    workflow_step_id = step.id,
                    status= StepRunStatus.SKIPPED,
                    completed_at = datetime.now(UTC),
                    started_at=datetime.now(UTC),
                    error_message = "Condition evaluated to false" 
                )
                db.add(step_run)
                db.commit()
                continue
        
        step_run = None
        try:
            step_run = WorkflowStepRun(
                workflow_run_id = run.id,
                workflow_step_id = step.id,
                status= StepRunStatus.RUNNING,
                started_at = datetime.now(UTC)
            )

            db.add(step_run)
            db.commit()
            db.refresh(step_run)

            # Placeholder execution
            output = execute_step(step, step_run, context)

            context[step.name] = output

            step_run.output = output
            step_run.status = StepRunStatus.COMPLETED
            step_run.completed_at = datetime.now(UTC)

            db.commit()
        except Exception as e:
            if step_run:
                step_run.status= StepRunStatus.FAILED
                step_run.error_message = str(e)
                step_run.completed_at = datetime.now(UTC)

            run.status = "failed"
            db.commit()

            raise
    
    run.status = "completed"

    db.commit()
    db.refresh(run)

    return run


