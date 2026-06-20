from pydantic import BaseModel, HttpUrl

class EchoStepConfig(BaseModel):
    message: str

class HttpStepConfig(BaseModel):
    url: HttpUrl