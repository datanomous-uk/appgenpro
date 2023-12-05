from aipreneuros.tasks import Task
from aipreneuros.config import CONFIG

from typing import Optional, List, Dict, Any, Tuple

from aipreneuros.utils import logger
from aipreneuros.utils.cost import estimate_cost_of_completion

from autogen.agentchat import Agent, ConversableAgent
from autogen.code_utils import (
    UNKNOWN,
    extract_code,
    infer_lang,
    execute_code
)

from pathlib import Path

DEFAULT_SYSTEM_MESSAGE="""Solve tasks using your coding and language skills. In the following cases, suggest python code (in a python coding block) or shell script (in a sh coding block) for the user to execute. 1. When you need to collect info, use the code to output the info you need, for example, browse or search the web, download/read a file, print the content of a webpage or a file, get the current date/time, check the operating system. After sufficient info is printed and the task is ready to be solved based on your language skill, you can solve the task by yourself. 2. When you need to perform some task with code, use the code to perform the task and output the result. Finish the task smartly. Solve the task step by step if you need to. If a plan is not provided, explain your plan first. Be clear which step uses code, and which step uses your language skill. When using code, you must indicate the script type in the code block. The user cannot provide any other feedback or perform any other action beyond executing the code you suggest. The user can't modify your code. So do not suggest incomplete code which requires users to modify. Don't use a code block if it's not intended to be executed by the user. If you want the user to save the code in a file before executing it, put # filename: <filename> inside the code block as the first line. Don't include multiple code blocks in one response. Do not ask users to copy and paste the result. Instead, use 'print' function for the output when relevant. Check the execution result returned by the user. If the result indicates there is an error, fix the error and output the code again. Suggest the full code instead of partial code or code changes. If the error can't be fixed or if the task is not solved even after the code is executed successfully, analyze the problem, revisit your assumption, collect additional info you need, and think of a different approach to try. When you find an answer, verify the answer carefully. Include verifiable evidence in your response if possible."""

class Implementation(Task):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def update_environment(self, environment, rsp):
        environment.codebase.update(CONFIG.artifacts["code"])


    def execute(
            self, 
            environment, 
        ):

        user_agent = environment.get_role(self.user_role_name).get_user()
        assistant_agent = environment.get_role(self.assistant_role_name).get_user()

        # Simulate pair programming
        user_agent.register_reply(
            assistant_agent.name,
            self._write_code
        )

        assistant_agent.register_reply(
            user_agent.name,
            self._write_code
        )

        # user_agent._oai_system_message[0]["content"] = f"{DEFAULT_SYSTEM_MESSAGE}\n{user_agent._oai_system_message["content"]}"
        # assistant_agent._oai_system_message[0]["content"] = f"{DEFAULT_SYSTEM_MESSAGE}\n{assistant_agent._oai_system_message['content']}"

        # register the termination functions to avoid infinite loops
        user_agent.register_reply(assistant_agent.name, ConversableAgent.check_termination_and_human_reply)
        assistant_agent.register_reply(user_agent.name, ConversableAgent.check_termination_and_human_reply)
    
        # Disabled code execution so that the user agent will provide feedback on the 
        # written code rather than blindly executing it.
        user_agent._code_execution_config = False

        prompt = self.initialize_prompt(environment)
        # user_agent.human_input_mode = "NEVER"
        self.log()
        user_agent.initiate_chat(
            assistant_agent,
            message=prompt,
            clear_history=True
        )
        # user_agent.human_input_mode = "NEVER"
        rsp = user_agent.last_message(agent=assistant_agent)['content']

        # ## Get the last message that is not a "TERMINATE" flag.
        # chat_history = [m for m in user_agent._oai_messages[assistant_agent] if not is_terminate_msg(m)]
        # rsp = chat_history[-1]['content']

        # Update the env variables with the returned details (shared knowledge)
        self.update_environment(environment, rsp)
        environment.log(msg=f"{self.description}")


    
    def _write_code(
            self,
            recipient: Optional[Agent] = None,
            messages: Optional[List[Dict]] = None,
            sender: Optional[Agent] = None,
            config: Optional[Any] = None,
        ):
            "return oai reply and save previous code blocks."
            client = recipient.client if config is None else config
            if client is None:
                return False, None
            if messages is None:
                messages = self._oai_messages[sender]

            # save code from previous messages to artifacts
            code_blocks = self._parse_code_blocks(messages, last_n_messages=1)

            # execute the code if python and add this to the messages
            for code_block in code_blocks:
                lang, filename, code = code_block
                if lang == "python":
                    if filename.startswith("test_"):
                        # filepath=Path("/Users/selinkayay/datanomous/aipreneuros/coding")/filename
                        # pytest_command = f"pytest {filepath}"
                        exec_results = execute_code(filename=filename, work_dir=Path("/Users/selinkayay/datanomous/aipreneuros/coding"))
                        logger.info(f"Executed test case file {filename} with results: {exec_results}")
                        messages.append({
                            "role": "user",
                            "content": f"Executed file {filename} with results: {exec_results}"
                        })
                elif lang == "sh":
                    exec_results = execute_code(code, lang=lang)
                    logger.info(f"Executed shell script with results: {exec_results}")
                    messages.append({
                        "role": "user",
                        "content": f"Executed the shell script with results: {exec_results}"
                    })
                else:
                    logger.warning(f"Unknown language: {lang}. Code block {code_block} not executed.")
    
            response = client.create(
                context=messages[-1].pop("context", None), messages=recipient._oai_system_message + messages
            )
            estimate_cost_of_completion(response)
            rsp = client.extract_text_or_function_call(response)[0]

            return True, rsp

    
    def _parse_code_blocks(self, messages, last_n_messages=1) -> List[Tuple[str, str, str]]:
        codes = []
        for i in range(min(len(messages), last_n_messages)):
            message = messages[-(i + 1)]
            if not message["content"]:
                continue
            code_blocks = extract_code(message["content"])
            logger.debug(code_blocks)
            if len(code_blocks) == 1 and code_blocks[0][0] == UNKNOWN:
                continue

            # found code blocks, save to artifacts
            code = self._save_code_blocks(code_blocks)
            codes.extend(code)
        return codes

    def _save_code_blocks(self, code_blocks) -> List[Tuple[str, str, str]]:
        codes = []
        """Save the code blocks to artifacts."""
        for code_block in code_blocks:
            lang, code = code_block
            if code.startswith("# filename: "):
                filename = code[11 : code.find("\n")].strip()
            else:
                filename = None
            logger.debug(f"Saving code for {filename}")
            # TODO: get rid of this config and update the environment at each step instead.
            codes.append((lang, filename, code))
            code_files = CONFIG.artifacts["code"]
            code_files[filename] = code
            # save code to some directory
            from aipreneuros.utils.write_utils import save_code
            save_code(code, filename, Path("/Users/selinkayay/datanomous/aipreneuros/coding"))
        return codes
