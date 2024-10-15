from src.tool import tool
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os
load_dotenv()

class SystemTime(BaseModel):
    format:str=Field(...,description="The format of the time",example=['%Y-%m-%d %H:%M:%S'])

@tool("System Time Tool",args_schema=SystemTime)
def system_time_tool(format:str):
    '''
    Retrieves the current system time in a human-readable format.
    '''
    from datetime import datetime
    try:
        current_time = datetime.now().strftime(format)
    except Exception as err:
        return f"Error: {err}"
    return current_time

