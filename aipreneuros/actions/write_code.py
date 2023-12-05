from typing import Optional, List, Dict, Any, Union, Tuple

from aipreneuros.actions import Action
from aipreneuros.utils import logger
from aipreneuros.config import CONFIG
from aipreneuros.utils.cost import estimate_cost_of_completion

from autogen.agentchat import Agent, ConversableAgent
from autogen.code_utils import (
    UNKNOWN,
    extract_code,
    infer_lang,
    execute_code
)

from pathlib import Path

class WriteCode(Action):

    def __init__(
            self,
            role,
            name: str = "WriteCode",
            description: str = "Write Code",
            **kwargs
    ):
        
        super().__init__(name, description)

        self._user = role._user
        self._react_assistant = role._react_assistant

        # Simulate pair programming
        self._user.register_reply(
            self._react_assistant.name,
            self._write_code
        )

        self._react_assistant.register_reply(
            self._user.name,
            self._write_code
        )

        # register the termination functions to avoid infinite loops
        self._user.register_reply(self._react_assistant.name, ConversableAgent.check_termination_and_human_reply)
        self._react_assistant.register_reply(self._user.name, ConversableAgent.check_termination_and_human_reply)
    
        # Disabled code execution so that the user agent will provide feedback on the 
        # written code rather than blindly executing it.
        self._user._code_execution_config = False


    def _run(self, **context) -> Union[str, Dict, Any]:
        
        logger.info("Writing code!")
        msg = context["messages"][0]

        self._user.initiate_chat(
            self._react_assistant,
            message=msg
        )

        rsp = self._user.last_message(agent=self._react_assistant)['content']
        return rsp

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
        code_blocks = self._parse_code_blocks(messages)

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
            elif lang == "sh" or lang == "bash":
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