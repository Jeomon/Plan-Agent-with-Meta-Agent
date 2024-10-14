from src.agent.plan.utils import extract_plan,read_markdown_file,extract_llm_response
from src.message import AIMessage,HumanMessage,SystemMessage
from langchain_core.runnables.graph import MermaidDrawMethod
from src.agent.plan.state import PlanState,UpdateState
from langgraph.graph import StateGraph,END,START
from IPython.display import display,Image
from src.inference import BaseInference
from src.agent.meta import MetaAgent
from src.router import LLMRouter
from src.agent import BaseAgent
from termcolor import colored

class PlanAgent(BaseAgent):
    def __init__(self,max_iteration=10,llm:BaseInference=None,verbose=False):
        self.name='Plan Agent'
        self.max_iteration=max_iteration
        self.graph=self.create_graph()
        self.verbose=verbose
        self.iteration=0
        self.llm=llm
    
    def router(self,state:PlanState):
        routes=[
            {
                'route': 'simple',
                'description': 'This route handles straightforward tasks with no user interaction. It generates a plan in one step, making it ideal for clear, uncomplicated problems that can be quickly solved.'
            },
            {
                'route': 'advanced',
                'description': 'This route is tailored for more complex, involved or ambiguous tasks that require additional information or user preferences. It involves multiple interactions to refine the plan based on specific needs, ensuring a more comprehensive and customized solution. This route is ideal for tasks that need deeper understanding or nuanced decision-making.'
            }
        ]
        query=state.get('input')
        router=LLMRouter(routes=routes,llm=self.llm,verbose=False)
        plan_type=router.invoke(query)
        return {**state,'plan_type':plan_type}

    def simple_plan(self,state:PlanState):
        system_prompt=read_markdown_file('./src/agent/plan/prompt/simple_plan.md')
        llm_response=self.llm.invoke([SystemMessage(system_prompt),HumanMessage(state.get('input'))])
        plan_data=extract_plan(llm_response.content)
        plan=plan_data.get('Plan')
        if self.verbose:
            print(colored(f'Plan:\n{'\n'.join([f'{index+1}. {task}' for index,task in enumerate(plan)])}',color='green',attrs=['bold']))
        return {**state,'plan':plan}
    
    def advance_plan(self,state:PlanState):
        system_prompt=read_markdown_file('./src/agent/plan/prompt/advanced_plan.md')
        messages=[SystemMessage(system_prompt),HumanMessage(state.get('input'))]
        llm_response=self.llm.invoke(messages)
        plan_data=extract_plan(llm_response.content)
        route=plan_data.get('Route')
        while route!='Plan':
            question=plan_data.get('Question')
            messages.pop(-1)
            answer=input(f'{question}\nUser: ')
            user_prompt=f'<option>\n<question>{question}</question>\n<answer>{answer}</answer>\n<route>{route}</route>\n</option>'
            messages.append(HumanMessage(user_prompt))
            llm_response=self.llm.invoke(messages)
            messages.append(AIMessage(llm_response.content))
            plan_data=extract_plan(llm_response.content)
            route=plan_data.get('Route')
        plan=plan_data.get('Plan')
        if self.verbose:
            print(colored(f'Plan:\n{'\n'.join([f'{index+1}. {task}' for index,task in enumerate(plan)])}',color='green',attrs=['bold']))
        return {**state,'plan':plan}


    def initialize(self,state:UpdateState):
        system_prompt=read_markdown_file('./src/agent/plan/prompt/update.md')
        current=state.get('plan')[0]
        pending=state.get('plan')
        completed=[]
        if self.verbose:
            print(colored(f'Pending Tasks:\n{'\n'.join([f'{index+1}. {task}' for index,task in enumerate(pending)])}',color='yellow',attrs=['bold']))
            print(colored(f'Completed Tasks:\n{'\n'.join([f'{index+1}. {task}' for index,task in enumerate(completed)])}',color='blue',attrs=['bold']))
        messages=[SystemMessage(system_prompt)]
        return {**state,'messages':messages,'current':current,'pending':pending,'completed':completed,'output':''}
    
    def execute_task(self,state:UpdateState):
        plan=state.get('plan')
        current=state.get('current')
        responses=state.get('responses')
        agent=MetaAgent(llm=self.llm,verbose=self.verbose)
        task_response=agent.invoke(f'Information:\n{'\n'.join([f'{index+1}. {task}' for index,task in enumerate(responses)])}\nTask:\n{current}')
        if self.verbose:
            print(colored(f'Current Task:\n{current}',color='cyan',attrs=['bold']))
            print(colored(f'Task Response:\n{task_response}',color='cyan',attrs=['bold']))
        user_prompt=f'Plan:\n{plan}\nTask:\n{current}\nTask Response:\n{task_response}'
        messages=[HumanMessage(user_prompt)]
        return {**state,'messages':messages,'responses':[task_response]}

    def update_plan(self,state:UpdateState):
        llm_response=self.llm.invoke(state.get('messages'))
        plan_data=extract_llm_response(llm_response.content)
        plan=plan_data.get('Plan')
        pending=plan_data.get('Pending')
        completed=plan_data.get('Completed')
        if self.verbose:
            print(colored(f'Pending Tasks:\n{'\n'.join([f'{index+1}. {task}' for index,task in enumerate(pending)])}',color='yellow',attrs=['bold']))
            print(colored(f'Completed Tasks:\n{'\n'.join([f'{index+1}. {task}' for index,task in enumerate(completed)])}',color='blue',attrs=['bold']))
        if pending:
            current=pending[0]
        else:
            current=''
        completed=plan_data.get('Completed')
        return {**state,'plan':plan,'current':current,'pending':pending,'completed':completed}
    
    def final(self,state:UpdateState):
        user_prompt='All Tasks completed successfully. Now give the final answer.'
        llm_response=self.llm.invoke(state.get('messages')+[HumanMessage(user_prompt)])
        plan_data=extract_llm_response(llm_response.content)
        output=plan_data.get('Final Answer')
        return {**state,'output':output}

    def plan_controller(self,state:UpdateState):
        if state.get('pending'):
            return 'task'
        else:
            return 'final'

    def route_controller(self,state:PlanState):
        return state.get('plan_type')

    def create_graph(self):
        graph=StateGraph(PlanState)
        graph.add_node('route',self.router)
        graph.add_node('simple',self.simple_plan)
        graph.add_node('advanced',self.advance_plan)
        graph.add_node('execute',lambda _:self.update_graph())

        graph.add_edge(START,'route')
        graph.add_conditional_edges('route',self.route_controller)
        graph.add_edge('simple','execute')
        graph.add_edge('advanced','execute')
        graph.add_edge('execute',END)

        return graph.compile(debug=False)
    
    def update_graph(self):
        graph=StateGraph(UpdateState)
        graph.add_node('inital',self.initialize)
        graph.add_node('task',self.execute_task)
        graph.add_node('update',self.update_plan)
        graph.add_node('final',self.final)

        graph.add_edge(START,'inital')
        graph.add_edge('inital','task')
        graph.add_edge('task','update')
        graph.add_conditional_edges('update',self.plan_controller)
        graph.add_edge('final',END)

        return graph.compile(debug=False)

    def invoke(self,input:str):
        if self.verbose:
            print(f'Entering '+colored(self.name,'black','on_white'))
        state={
            'input': input,
            'plan_status':'',
            'route':'',
            'plan': [],
            'output': ''
        }
        agent_response=self.graph.invoke(state)
        return agent_response['output']


    def stream(self, input: str):
        pass