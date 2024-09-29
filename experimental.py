from src.tool import tool
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os
load_dotenv()

class TimeChecker(BaseModel):
    timezone:str=Field(...,description="The timezone to get the current time from.",example=['UTC'])

@tool("Time Checker Tool",args_schema=TimeChecker)
def time_checker_tool(timezone:str):
    '''
    Retrieves the current time from the system in hours and minutes.
    '''
    from datetime import datetime
    import pytz
    try:
        tz=pytz.timezone(timezone)
        current_time=datetime.now(tz)
        return f"Current time in {timezone}: {current_time.strftime('%H:%M')}"
    except Exception as err:
        return f"Error: {err}"

