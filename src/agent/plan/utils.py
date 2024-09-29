import re

def plan_to_list(plan: str) -> list:
    # Use regex to find each numbered task (starting with digits followed by a period)
    tasks = re.findall(r'\d+\.\s(.*?)(?=\n\d+\.|\Z)', plan, re.DOTALL)
    # Strip any extra spaces from each task and return the list
    return [task.strip() for task in tasks]

def extract_llm_response(xml_response: str) -> dict:
    # Initialize the result dictionary
    result = {
        'Current Plan': None,
        'Pending': None,
        'Completed': None,
        'Final Answer': None,
        'Route': None
    }
    
    # Define regex patterns to match each part of the response
    current_plan_regex = re.compile(r'<current-plan>\s*(.*?)\s*</current-plan>', re.DOTALL)
    pending_regex = re.compile(r'<pending>\s*(.*?)\s*</pending>', re.DOTALL)
    completed_regex = re.compile(r'<completed>\s*(.*?)\s*</completed>', re.DOTALL)
    final_answer_regex = re.compile(r'<final-answer>\s*(.*?)\s*</final-answer>', re.DOTALL)
    route_regex = re.compile(r'<route>\s*(.*?)\s*</route>', re.DOTALL)

    # Helper function to clean up task lists by removing bullet points, dashes, and extra characters
    def clean_task_list(task_string: str) -> list:
        # Remove the bullet markers like '- [ ]', '- [x]', and any extra dashes or spaces
        cleaned_tasks = re.sub(r'[-–]\s*\[\s*\]|\[\s*x\s*\]|[-–]\s*', '', task_string)
        # Split the cleaned tasks into a list and strip unnecessary spaces
        return [task.strip() for task in cleaned_tasks.split('\n') if task.strip()]

    # Extract Current Plan
    current_plan_match = current_plan_regex.search(xml_response)
    if current_plan_match:
        current_plan_content = current_plan_match.group(1).strip()
        # Remove numeric prefixes like "1.", "2.", etc.
        result['Current Plan'] = [re.sub(r'^\d+\.\s*', '', task).strip() for task in current_plan_content.split('\n') if task.strip()]

    # Extract Pending tasks
    pending_match = pending_regex.search(xml_response)
    if pending_match:
        pending_content = pending_match.group(1).strip()
        result['Pending'] = clean_task_list(pending_content)

    # Extract Completed tasks
    completed_match = completed_regex.search(xml_response)
    if completed_match:
        completed_content = completed_match.group(1).strip()
        result['Completed'] = clean_task_list(completed_content)

    # Extract Final Answer
    final_answer_match = final_answer_regex.search(xml_response)
    if final_answer_match:
        result['Final Answer'] = final_answer_match.group(1).strip()

    # Extract Route
    route_match = route_regex.search(xml_response)
    if route_match:
        result['Route'] = route_match.group(1).strip()

    return result

def read_markdown_file(file_path: str) -> str:
    with open(file_path, 'r',encoding='utf-8') as f:
        markdown_content = f.read()
    return markdown_content

def extract_task(text: str) -> str:
    # Regular expression to match a single task starting with a number followed by a dot and the task description
    task_regex = re.compile(r'\d+\.\s*(.*)', re.DOTALL)
    
    # Extract the first match
    task_match = task_regex.search(text)
    
    # If a match is found, return the task statement
    if task_match:
        return task_match.group(1).strip()
    return None