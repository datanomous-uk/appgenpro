from aipreneuros import Environment
from aipreneuros.utils.logs import logger

import pprint
import chainlit as cl

class Task:

    def __init__(self,
                 description: str = None,
                 assistant_role_name: str = None,
                 user_role_name: str = None,
                 max_consecutive_auto_reply: int = 5,
                 task_prompt: str = None,
                 placeholders: dict = {},):

        self.description = description
        self.assistant_role_name = assistant_role_name
        self.user_role_name = user_role_name
        self.max_consecutive_auto_reply = max_consecutive_auto_reply
        self.task_prompt = task_prompt
        self.placeholders = placeholders


    """
    Executes the conversation between the user and the assistant on the given task.

    Parameters:
        environment (Environment): The environment in which the conversation takes place.

    Returns:
        None
    """
    def execute(
            self, 
            environment: Environment, 
        ):

        user_agent = environment.get_role(self.user_role_name).get_user()
        assistant_agent = environment.get_role(self.assistant_role_name).get_user()

        prompt = self.initialize_prompt(environment)
        user_agent.human_input_mode = "ALWAYS"
        self.log()
        user_agent.initiate_chat(
            assistant_agent,
            message=prompt,
            clear_history=True
        )
        user_agent.human_input_mode = "NEVER"
        rsp = user_agent.last_message(agent=assistant_agent)['content']

        # ## Get the last message that is not a "TERMINATE" flag.
        # chat_history = [m for m in user_agent._oai_messages[assistant_agent] if not is_terminate_msg(m)]
        # rsp = chat_history[-1]['content']

        # Update the env variables with the returned details (shared knowledge)
        self.update_environment(environment, rsp)
        environment.log(msg=f"{self.description}")

    
    async def a_execute(
        self, 
        environment: Environment
    ):
        user_agent = environment.get_role(self.user_role_name).get_user()
        assistant_agent = environment.get_role(self.assistant_role_name).get_user()

        task = await environment._display_task(self.description)

        cl.run_sync(cl.Message(
            content=f"**The *{self.assistant_role_name}* is starting on the task: *{self.description}*.**",
        ).send())
        prompt = self.initialize_prompt(environment)
        user_agent.human_input_mode = "ALWAYS"  
        self.log()
        await cl.make_async(user_agent.initiate_chat)(
            assistant_agent,
            message=prompt,
            clear_history=True
        )
        user_agent.human_input_mode = "NEVER"
        rsp = user_agent.last_message(agent=assistant_agent)['content']

        # Update the env variables with the returned details (shared knowledge)
        self.update_environment(environment, rsp)

        await environment._finish_task(task)
        environment.log(msg=f"{self.description}")




    """
    Override this function to customize how the environment
    gets updated.

    Args:
        environment (str): The current environment.
        rsp (str): The response message to update the environment with.

    Returns:
        None
    """
    def update_environment(self, environment, rsp):

        # Customize this function.
        pass



    """
    Override this function to customize how the prompt gets initialized
    with the environment fields.

    Parameters:
        environment (dict): A dictionary containing the environment variables.

    Returns:
        str: The initialized task prompt.

    Raises:
        Exception: If there is an error initializing the prompt.
    """
    
    def initialize_prompt(self, environment):

        try:
            self.placeholders = {**self.placeholders, **environment.dict()}
            return self.task_prompt.format(**self.placeholders)
        except:
            logger.error(f"Failed to initialize the prompt '{self.task_prompt}'. Please check if the placeholders are correct '{self.placeholders}'. Then try again!")
    


    def log(self):
        logger.debug(f"**Executing a new task**\n\nThe task configurations:\n\n--\n\n{self.__str__()}\n\n--\n\n")
    

    def dict(self):
        return {
            "description": self.description,
            "assistant_role_name": self.assistant_role_name,
            "user_role_name": self.user_role_name,
            "max_consecutive_auto_reply": self.max_consecutive_auto_reply,
            "task_prompt": self.task_prompt
        }
    

    def __repr__(self) -> str:
        return self.__str__()
    
    def __str__(self):
        return f"Description: {pprint.pformat(self.description)}\nAssistant Role Name: {self.assistant_role_name}\nUser Role Name: {self.user_role_name}\nMax Consecutive Auto Reply: {self.max_consecutive_auto_reply}\nTask Prompt: {pprint.pformat(self.task_prompt)}\nPlaceholders: {pprint.pformat(self.placeholders)}"
    