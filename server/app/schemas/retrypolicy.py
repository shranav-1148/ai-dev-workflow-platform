from pydantic import BaseModel
from enum import Enum


class BackoffStrategy(str, Enum):
    NONE= "none"
    LINEAR = "linear"
    EXPONENTIAL = 'exponential'

class RetryPolicy(BaseModel):
    max_attempts: int = 1
    delay_seconds: int = 0
    backoff: BackoffStrategy = BackoffStrategy.NONE