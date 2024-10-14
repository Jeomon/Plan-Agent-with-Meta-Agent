from typing import TypedDict,Annotated
from src.message import BaseMessage
from operator import add

def subtract(l1: list[str], l2: list[str]) -> list[str]:
    return list(set(l1) - set(l2))

class PlanState(TypedDict):
    input: str
    plan_type: str
    plan_status: str
    plan: list[str]
    output: str

class UpdateState(TypedDict):
    plan:str
    current:str
    responses:Annotated[list[str],add]
    pending: list[str]
    completed: list[str]
    output:str
    messages: Annotated[list[BaseMessage],add]