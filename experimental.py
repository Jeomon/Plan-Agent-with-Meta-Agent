from src.tool import tool
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os
load_dotenv()

class SystemProperties(BaseModel):
    os_name:str=Field(...,description="The name of the operating system.",example=['Windows', 'Linux', 'Darwin'])
    user_name:str=Field(...,description="The name of the user.",example=['John Doe'])
    cwd_path:str=Field(...,description="The path of the current working directory.",example=['/home/user/'])

@tool("System Properties Tool",args_schema=SystemProperties)
def system_properties_tool(os_name:str,user_name:str,cwd_path:str)->str:
    '''
    Retrieves information about the machine's system properties or settings, including the operating system, user, and current working directory.
    '''
    import platform
    import getpass
    import os
    try:
        system_properties={}
        system_properties['Operating System']=platform.system()
        system_properties['User']=getpass.getuser()
        system_properties['Current Working Directory']=os.getcwd()
        return str(system_properties)
    except Exception as err:
        return f"Error: {err}"

class SystemInfo(BaseModel):
    pass

@tool("System Information Tool",args_schema=SystemInfo)
def system_info_tool()->str:
    '''
    Retrieves the operating system name and version from the system properties.
    '''
    import platform
    try:
        os_name = platform.system()
        os_version = platform.release()
        os_info = f"Operating System: {os_name}\nVersion: {os_version}"
        return os_info
    except Exception as err:
        return f"Error: {err}"

