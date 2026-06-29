from app.models.workflowRun import WorkflowRun
from app.models.workflowStep import WorkflowStep
from app.models.workflowStepRun import WorkflowStepRun
from server.app.schemas.RunStatus import RunStatus
from app.models.workflow import Workflow
from sqlalchemy.orm import Session
from app.services.step_executor import execute_step
from app.services.condition_evaluator import evaluate_conditions
from app.services.state_machine import transition_run


def execute_workflow(
        workflow: Workflow,
        db: Session
):
    '''Executing a workflow'''
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
        except Exception as e:
            if step_run:
                
                transition_run(
                    step_run,
                    RunStatus.FAILED
                )

                step_run.error_message = str(e)

            transition_run(
                run, RunStatus.FAILED
            )
            db.commit()

            raise
    
    transition_run(
        run, RunStatus.COMPLETED
    )

    db.commit()
    db.refresh(run)

    return run


