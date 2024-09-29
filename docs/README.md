# Planner Agent with Meta Agent: Structured Task Execution Workflow

## Description

The **Planner Agent with Meta Agent** project automates complex problem-solving by transforming a given problem statement into a structured plan and executing it step-by-step. The **Planner Agent** serves as the top-most agent, converting the initial problem into a well-crafted plan, which is then passed to the **Meta Agent**. The Meta Agent takes over by executing each task from the plan one at a time, updating the plan as needed until all tasks are successfully completed. The final result is provided after all sub-tasks have been resolved, ensuring an efficient and organized solution process.

This system simplifies problem-solving by breaking down the complexity into manageable steps, delegating tasks to specialized agents as necessary, and iterating until the full problem is solved.

## Architecture Overview

![Image of the Workflow](diagram.svg)

### Agents:

- **Planner Agent:** Receives the problem statement and transforms it into a structured plan. Each step in the plan is designed for sequential execution by the Meta Agent.
- **Meta Agent:** Executes each task from the plan, managing step-by-step task resolution. After completing each task, it updates the plan and proceeds with the next one until no tasks are left.
- **Supporting Agents (ReAct, CoT, Tool):** The Meta Agent delegates specific tasks to these agents as needed:
  - **ReAct Agent**: Executes tasks using external tools, and if tools are missing or outdated, it interacts with the **Tool Agent** to create, update, or delete tools as required.
  - **Chain of Thought (CoT) Agent**: Handles tasks that rely on iterative reasoning without tools.
  - **Tool Agent**: Manages the lifecycle of tools by creating, updating, or even deleting tools based on the task's needs or user requests.

## Key Features

- **Structured Planning**: The Planner Agent breaks down complex queries into manageable steps, ensuring organized task execution.
- **Dynamic Task Execution**: The Meta Agent executes tasks iteratively and updates the plan after each task, ensuring real-time adjustments based on results.
- **Flexible Tool Management**: The **Tool Agent** can create, update, or delete tools dynamically during task execution based on requests from the **ReAct Agent**.
- **Iterative Reasoning**: Tasks that do not require external tools are handled by the **CoT Agent** through step-by-step logical processing.

## Workflow

1. **Problem Statement:** The user provides a problem statement to the **Planner Agent**.
2. **Plan Creation:** The **Planner Agent** converts the problem statement into a well-defined plan with multiple steps.
3. **Task Execution:** The **Meta Agent** executes each step in the plan sequentially, updating the plan as tasks are completed.
4. **Tool Interaction (if needed):** If a task requires a tool, the **ReAct Agent** handles it by invoking the **Tool Agent** for tool creation, updates, or deletion.
5. **Iterative Processing:** The process repeats until all tasks are resolved, and the final answer is produced based on the results.

## Installation

Ensure Python 3.x is installed, then run the following to install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

To start the application:

```bash
python app.py
```

## Usage

1. Provide a problem statement to the **Planner Agent**.
2. The **Planner Agent** creates a plan, which the **Meta Agent** uses to execute tasks.
3. The Meta Agent will:
   - Delegate tool-based tasks to the **ReAct Agent**, which may involve the **Tool Agent**.
   - Use the **CoT Agent** for reasoning tasks without tools.
4. The process continues until all tasks are complete, and the final result is provided.

### Example Queries

#### Example 1: Time right now

```plaintext
Enter a query: what is the time now
Entering Plan Agent
Plan:
1. Check the current time on a device or clock.
Pending Tasks:
1. Check the current time on a device or clock.
Completed Tasks:

Entering Meta Agent
Agent Name: Time Checker Agent
Description: This agent is responsible for checking the current time on a device or clock.
Tasks: ["Check the device's clock or a nearby clock for the current time."]
Tool: {'Tool Name': 'Device Clock Tool', 'Tool Description': "A tool that allows the agent to access the device's clock to retrieve the current time."}
Entering Time Checker Agent
Thought: Since the task is to check the current time, I need to use a tool that can interact with the user to ask for the current time or retrieve it from the system. However, I don't have a tool that can directly retrieve the current time from the system. I will request a new tool to be created that can retrieve the current time.
Entering Tool Agent
Query: Please create a new tool called 'Time Checker Tool' that can retrieve the current time from the system. This tool should be able to get the current time in hours and minutes.
Time Checker Tool has been saved to experimental.py successfully.
Tool Name: Time Checker Tool
Tool Input: {'properties': {'timezone': {'description': 'The timezone to get the current time from.', 'example': ['UTC'], 'title': 'Timezone', 'type': 'string'}}, 'required': ['timezone'], 'type': 'object'}
 Tool has been generated successfully. Now the tool is available in the tool box and ready for use.
Thought: Now that the Time Checker Tool is available in the tool box, I can use it to retrieve the current time. Since the user is using Windows, I will use the 'UTC' timezone as the input to get the current time in a standard format.
Action Name: Time Checker Tool
Action Input: {
  "timezone": "UTC"
}
Observation: Current time in UTC: 17:26
Thought: Now that I have the current time in UTC, I can provide the final answer to the user. Since the user asked for the current time, I will present the time in a clear and readable format.
Answer: The current time is **17:26** (UTC).
Final Answer: The current time is **17:26** (UTC).
Current Task:
Check the current time on a device or clock.
Task Response:
Final Answer: The current time is **17:26** (UTC).
Pending Tasks:

Completed Tasks:
1. Check the current time on a device or clock.
The current time is **17:26** (UTC).
```

## Contact

For any questions, feel free to reach out:

- **Email**: jeogeoalukka@gmail.com