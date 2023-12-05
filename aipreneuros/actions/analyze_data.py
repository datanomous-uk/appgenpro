from typing import Union, Dict, Any
from aipreneuros.actions import Action


class AnalyzeData(Action):

    def __init__(
            self,
            role,
            name: str = "analyze_data",
            description:str = "Analyze the given Data sources to understand what the data shows and how you can possibly use it to fulfill the client's requests.",
            **kwargs):

        super().__init__(name, description)

        self._user = role._user
        self._react_assistant = role._react_assistant


    def _run(self, **context) -> Union[str, Dict, Any]:
        messages = context["messages"]
        msg = "\n".join([f"{msg['role']} said: {msg['content']}" for msg in messages])

        self._user._code_execution_config={
            "work_dir": "coding",
            "use_docker": False,  # set to True or image name like "python:3" to use docker
        }
        self._user.initiate_chat(
            self._react_assistant,
            message=msg
        )
        rsp = self._user.last_message(agent=self._react_assistant)['content']
        return rsp

