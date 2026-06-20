from app.models.workflowRun import WorkflowRun
from app.models.workflowStep import WorkflowStep
from app.models.workflowStepRun import WorkflowStepRun
from app.models.workflow import Workflow
from sqlalchemy.orm import Session
from app.services.step_executor import execute_step


def execute_workflow(
        workflow: Workflow,
        db: Session
):
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
        try:
            step_run = WorkflowStepRun(
                workflow_run_id = run.id,
                workflow_step_id = step.id,
                status="running"
            )

            db.add(step_run)
            db.commit()
            db.refresh(step_run)

            # Placeholder execution
            output = execute_step(step, step_run, context)

            context[step.name] = output

            step_run.output = output
            step_run.status = "completed"

            db.commit()
        except Exception as e:
            step_run.status="failed"
            step_run.error_message = str(e)

            run.status = "failed"
            db.commit()

            raise
    
    run.status = "completed"

    db.commit()
    db.refresh(run)

    return run


