from pydantic import BaseModel
from typing import Dict, List, Optional, Union, Any

from aipreneuros.config import CONFIG
from aipreneuros.utils.logs import logger
from aipreneuros.utils.cost import estimate_cost_of_completion
from aipreneuros.actions import get_action
from aipreneuros.roles.chainlit_wrappers import (
    ChainlitUserProxyAgent, 
    ChainlitAssistantAgent
)
from autogen.agentchat import (
    Agent,
    GroupChat, 
    UserProxyAgent, 
    AssistantAgent
)

import chainlit as cl

PREFIX_TEMPLATE = """You are a {role}, your goal is to {goal}, and the constraints are {constraints}."""

STATE_TEMPLATE = """Conversation records:
===
{history}
===

Based on your conversation records so far, reflect and decide which stage you should enter or stay in based on these records.
Remember that the last message in the conversation records is the most recent message sent to you.
You must return a reply like the format below:
STATE: <INFO>
RESPONSE: <RESPONSE>

<INFO> is a number between 0-{n_states} to choose the most suitable next state to follow according to the understanding
of the conversation.
You may choose from the following states: 
{states}

If you think you have completed your goal and don't need to go to any of these states, then <INFO> should be -1.

<RESPONSE> is your well thought out response as a {recipient_name} to the sender, {sender_name}, explaining 
how you will handle the request with your expertise. Just explain your plan in a conversational manner here and 
explain your rationale for choosing a particular state to follow here.
"""

DEFAULT_SYSTEM_MESSAGE = """You are a helpful AI assistant.
Solve tasks using your coding and language skills.
In the following cases, suggest python code (in a python coding block) or shell script (in a sh coding block) for the user to execute.
    1. When you need to collect info, use the code to output the info you need, for example, browse or search the web, download/read a file, print the content of a webpage or a file, get the current date/time, check the operating system. After sufficient info is printed and the task is ready to be solved based on your language skill, you can solve the task by yourself.
    2. When you need to perform some task with code, use the code to perform the task and output the result. Finish the task smartly.
Solve the task step by step if you need to. If a plan is not provided, explain your plan first. Be clear which step uses code, and which step uses your language skill.
When using code, you must indicate the script type in the code block. The user cannot provide any other feedback or perform any other action beyond executing the code you suggest. The user can't modify your code. So do not suggest incomplete code which requires users to modify. Don't use a code block if it's not intended to be executed by the user.
If you want the user to save the code in a file before executing it, put # filename: <filename> inside the code block as the first line. Don't include multiple code blocks in one response. Do not ask users to copy and paste the result. Instead, use 'print' function for the output when relevant. Check the execution result returned by the user.
If the result indicates there is an error, fix the error and output the code again. Suggest the full code instead of partial code or code changes. If the error can't be fixed or if the task is not solved even after the code is executed successfully, analyze the problem, revisit your assumption, collect additional info you need, and think of a different approach to try.
When you find an answer, verify the answer carefully. Include verifiable evidence in your response if possible.
"""



class RoleSetting(BaseModel):
    """Role Settings"""
    role: str
    goal: str
    constraints: str

    def __str__(self):
        return f"{self.role}"

    def __repr__(self):
        return self.__str__()
    


'''
       Facilitating complex interactions in an AI-driven environment. 
       It involves the use of roles, agents, and actions, presumably to execute tasks or respond to user inputs in a chat or task management system. 
'''

class Role:
    """Role/Agent"""

    def __init__(self, role="", goal="", constraints="", **kwargs):
        self._setting = RoleSetting(role=role, goal=goal, constraints=constraints)
        self._role_id = str(self._setting)
        self.llm_config = CONFIG.llm_config.copy()
        self._user = None
        self.actions = []
        self.watch_list = []

    @classmethod
    def from_dict(cls, data):
        role_class = cls(**data)
        role_class.init_react_agent(**data)
        if actions:=data.get("actions"):
            actions = [get_action(action_name)(role=role_class) for action_name in actions]
            role_class.add_actions(actions)
        if watch_list:=data.get("watch_list"):
            role_class.watch(watch_list)
        return role_class

    @property
    def role(self):
        return self._role_id
    
    def get_user(self):
        return self._user

    def _get_prefix(self):
        return PREFIX_TEMPLATE.format(**self._setting.model_dump())

    def add_actions(self, actions:list):
        self.actions.extend(actions)
        
    def watch(self, watch_list:list):
        self._user.register_reply(
            watch_list,
            self._react
        )


    """
    Initializes the React agent.

    Args:
        max_consecutive_auto_reply (int, optional): The maximum number of consecutive auto replies. Defaults to 10.
        human_input_mode (str, optional): The mode for human input. Defaults to "NEVER".
        react_assistant_instructions (str, optional): The instructions for the React assistant. Defaults to "".
        num_of_react_loops (int, optional): The number of loops for the React agent. Defaults to 1.
        **kwargs: Additional keyword arguments.

    Returns:
        None
    """
    def init_react_agent(
            self, 
            max_consecutive_auto_reply=10, 
            human_input_mode="NEVER",
            react_assistant_instructions: Optional[str]="",
            num_of_react_loops: Optional[int]=1,
            **kwargs
    ):

        self.num_of_react_loops = num_of_react_loops

        user_agent_params = dict(  
            name=self.role,
            system_message = self._get_prefix() + "reply with TERMINATE if everything looks good.",
            is_termination_msg=lambda x: x.get("content", "") and (x.get("content", "").rstrip().endswith("TERMINATE") or x.get("content", "").strip() == ""),
            human_input_mode=human_input_mode,
            code_execution_config={
                    "work_dir": "coding",
                    "use_docker": False,  # set to True or image name like "python:3" to use docker
                },
            max_consecutive_auto_reply=max_consecutive_auto_reply,
            llm_config=self.llm_config
        )

        if CONFIG.use_chainlit:
            self._user = ChainlitUserProxyAgent(**user_agent_params)
        else:
            self._user = UserProxyAgent(**user_agent_params)

        react_agent_params = dict(
            name="CodingAssistant",
            is_termination_msg=lambda x: x.get("content", "") and (x.get("content", "").rstrip().endswith("TERMINATE") or x.get("content", "").rstrip() == ""),
            human_input_mode="NEVER",
            llm_config=self.llm_config,
            system_message=f"{DEFAULT_SYSTEM_MESSAGE}\n{react_assistant_instructions}\nReply 'TERMINATE' in the end when everything is done.",
            max_consecutive_auto_reply=max_consecutive_auto_reply,
        )

        if CONFIG.use_chainlit:
            self._react_assistant = ChainlitAssistantAgent(**react_agent_params)
        else:
            self._react_assistant = AssistantAgent(**react_agent_params)



    """
    React to incoming messages from a recipient.

    The recipient first thinks, then the action is executed.

    Args:
        recipient (Optional[Agent]): The recipient of the messages. Defaults to None.
        messages (Optional[List[Dict]]): The list of messages to react to. Defaults to None.
        sender (Optional[Agent]): The sender of the messages. Defaults to None.
        config (Optional[GroupChat]): The configuration for the group chat. Defaults to None.

    Returns:
        Union[str, Dict, None]: The reaction response, or None if there was no reaction.
    """
        
    def _react(self,
            recipient: Optional[Agent] = None,
            messages: Optional[List[Dict]] = None,
            sender: Optional[Agent] = None,
            config: Optional[GroupChat] = None
        ) -> Union[str, Dict, None]:

    
        client = recipient.client if config is None else config
        if messages is None:
            messages = recipient._oai_messages[sender]

        for _ in range(self.num_of_react_loops):
            rsp, state = self._think(messages, recipient, sender, client)
        
            if rsp == "" and state == -1:
                return True, "TERMINATE" 
            
            if rsp != "":
                if state == -1:
                    return True, rsp
                logger.info(f"{recipient.name}: {rsp}")
                if CONFIG.use_chainlit:
                    cl.run_sync(cl.Message(
                        content=rsp,
                        author=recipient.name
                    ).send())
                messages.append({
                    "role": "assistant",
                    "content": rsp
                })
            if state != -1:
                msg = f"**{recipient.name} is performing the following action: {self.actions[state].name}.**"
                logger.info(msg)
                if CONFIG.use_chainlit:
                    cl.run_sync(cl.Message(
                        content=msg
                    ).send())
                rsp = self.actions[state]._run(client=client, messages=messages, system_message=recipient._oai_system_message)
                return True, rsp
            
            return False, "TERMINATE"    



    """
    Executes the thinking process for the agent by deciding on what
    action to perform next.

    Args:
        messages (List[Dict]): The list of messages received by the agent.
        recipient (Optional[Agent]): The recipient agent for the response.
        sender (Optional[Agent]): The sender agent for the response.
        client (Optional[Any]): The client used for communication.

    Returns:
        None: This function does not return anything.

    Raises:
        None: This function does not raise any exceptions.
    """
    def _think(
            self, 
            messages: List[Dict], 
            recipient: Optional[Agent] = None, 
            sender: Optional[Agent] = None, 
            client: Optional[Any] = None
        ) -> None:

        # if len(self.tools) == 1:
        #     return "", 0
        is_empty_msg = messages[-1].get("content", "").lower() == ""
        is_terminate_msg = messages[-1].get("content", "").lower() in ["terminate", "exit"]

        if is_empty_msg or is_terminate_msg:
            return "", -1

        info_msg = f"**{recipient.name} is thinking...**"
        logger.info(info_msg)
        if CONFIG.use_chainlit:
                cl.run_sync(cl.Message(
                    content=info_msg
                ).send()
            )

        prompt = STATE_TEMPLATE.format(
            history=messages,
            recipient_name=recipient.name,
            sender_name=sender.name,
            n_states=len(self.actions),
            states=[f"{idx}: {action.name} --> {action.description}" for idx, action in enumerate(self.actions)],
        )
        msg = [{
            "role": "user",
            "content": prompt
        }]

        response = client.create(
            context=messages[-1].pop("context", None), messages=recipient._oai_system_message + msg
        )
        estimate_cost_of_completion(response)
        rsp = client.extract_text_or_function_call(response)[0]
        rsp, state = extract_state_info(rsp)

        if state != -1 and state >= len(self.actions):
            logger.error(f"Invalid state index provided: {state}")
        return rsp, state


def extract_state_info(input_string):
    response = input_string.split("RESPONSE: ")
    rsp = response[1]
    state = response[0]
    state = state.split("STATE: ")[1].strip()
    return rsp, int(state)
   