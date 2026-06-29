from server.app.schemas.RunStatus import RunStatus
from datetime import datetime, UTC

def utc_now():
    return datetime.now(UTC)

RUN_TRANSITIONS = {
    RunStatus.PENDING: [
        RunStatus.RUNNING,
        RunStatus.SKIPPED
    ],

    RunStatus.RUNNING: [
        RunStatus.COMPLETED,
        RunStatus.FAILED
    ],

    RunStatus.COMPLETED: [],

    RunStatus.FAILED: [],

    RunStatus.SKIPPED: []
}

def transition_run(run_object, new_status):
    current_status = run_object.status

    allowed_transitions = RUN_TRANSITIONS.get(
        current_status, []
    )



    if new_status not in allowed_transitions:
        raise Exception(
            f"Invalid transiftion from {current_status} to {new_status}"
        )
    
    run_object.status = new_status
    
    if new_status == RunStatus.RUNNING:
        run_object.started_at = utc_now()

    if new_status in [
        RunStatus.COMPLETED,
        RunStatus.FAILED,
        RunStatus.SKIPPED
    ]:
        run_object.completed_at = utc_now()
    
    