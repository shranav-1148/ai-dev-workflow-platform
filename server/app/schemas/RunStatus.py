from enum import Enum
'''Enumerator object for WorkflowRun and WorkflowStepRun'''
class RunStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"