from app.models.workflowRun import WorkflowRun
from app.models.workflowStep import WorkflowStep
from app.models.workflowStepRun import WorkflowStepRun
from app.schemas.StepRunStatus import StepRunStatus
from app.models.workflow import Workflow
from sqlalchemy.orm import Session
from app.services.step_executor import execute_step
from app.services.condition_evaluator import evaluate_conditions
from app.services.state_machine import transition_step_run


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
            '''If there is a condition set and the condition is not met
                Create a step Run with Pending status but change it immediately
                to skipped'''
            if not evaluate_conditions(step.condition, context):
                step_run = WorkflowStepRun(
                    workflow_run_id = run.id,
                    workflow_step_id = step.id,
                    status= StepRunStatus.PENDING
                )

                db.add(step_run)
                db.commit()
                db.refresh(step_run)

                transition_step_run(
                    step_run,
                    StepRunStatus.SKIPPED
                )
                step_run.error_message = "Condition evaluated to false"                
                continue
        
        step_run = None
        try:
            step_run = WorkflowStepRun(
                workflow_run_id = run.id,
                workflow_step_id = step.id,
                status= StepRunStatus.PENDING
            )

            db.add(step_run)
            db.commit()
            db.refresh(step_run)

            transition_step_run(
                step_run,
                StepRunStatus.RUNNING
            )
            
            db.commit()

            # Placeholder execution
            output = execute_step(step, step_run, context)

            context[step.name] = output

            step_run.output = output
            
            transition_step_run(
                step_run,
                StepRunStatus.COMPLETED
            )

            db.commit()
        except Exception as e:
            if step_run:
                
                transition_step_run(
                    step_run,
                    StepRunStatus.FAILED
                )

                step_run.error_message = str(e)

            run.status = "failed"
            db.commit()

            raise
    
    run.status = "completed"

    db.commit()
    db.refresh(run)

    return run


