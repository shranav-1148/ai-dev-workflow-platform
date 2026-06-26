from app.schemas.StepRunStatus import StepRunStatus

STEP_RUN_TRANSITIONS = {
    StepRunStatus.QUEUED: [
        StepRunStatus.RUNNING,
        StepRunStatus.SKIPPED
    ],

    StepRunStatus.RUNNING: [
        StepRunStatus.COMPLETED,
        StepRunStatus.FAILED
    ],

    StepRunStatus.COMPLETED: [],

    StepRunStatus.FAILED: [],

    StepRunStatus.SKIPPED: []
}

def transition_step_run(step_run, new_status):
    current_status = step_run.status

    allowed_transitions = STEP_RUN_TRANSITIONS.get(
        current_status, []
    )

    if new_status not in allowed_transitions:
        raise Exception(
            f"Invalid transiftion from {current_status} to {new_status}"
        )
    
    step_run.status = new_status