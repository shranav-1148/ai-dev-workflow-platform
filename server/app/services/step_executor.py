from app.models.workflowStep import WorkflowStep
from app.schemas.step_configs import HttpStepConfig, EchoStepConfig
from app.services.template_resolver import resolve_templates
import requests

def execute_echo_step(step:WorkflowStep, step_run, context):
    raw_config = EchoStepConfig(**step.config)
    message = resolve_templates(raw_config.message, context)
    return {
        "type": "echo",
        "message": message,
    }

def execute_http_step(step: WorkflowStep, step_run, context):
    
    raw_config = HttpStepConfig(**step.config)
    url = resolve_templates(raw_config.url, context)

    response = requests.get(url)

    data = None

    try:
        data = response.json()
    except Exception:
        data= response.text

    return {
        "type" : "http",
        "status_code" : response.status_code,
        "data" : data
    }

def execute_github_step(step: WorkflowStep, step_run, context):
    raw_config = step.config

    repo_id = resolve_templates(raw_config.get("repo_id"), context)
    return {
        "type": "github_repo",
        "message": "github step executed",
        "config": step.config
    }


STEP_REGISTRY = {
    "echo": execute_echo_step,
    "http": execute_http_step,
    "github_repo": execute_github_step
}

def execute_step(step: WorkflowStep, step_run, context):
    handler = STEP_REGISTRY.get(step.step_type)

    if not handler:   
        raise Exception(f"Unknown step type: {step.step_type}")
    
    return handler(step, step_run, context)

