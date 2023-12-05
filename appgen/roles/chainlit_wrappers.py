from autogen import Agent, AssistantAgent, UserProxyAgent
from typing import Dict, Optional, Union
import chainlit as cl

def make_pretty(msg):
    return msg.replace("TERMINATE","")

async def ask_helper(func, **kwargs):
    res = await func(**kwargs).send()
    while not res:
        res = await func(**kwargs).send()
    return res


def show_message(assistant, message, recipient):
    if isinstance(message, dict):
        parsed_doc = message.get("parsed_doc", None)
        
        elements = []
        if parsed_doc:
            doc = parsed_doc.get("document", "")
            image_paths = parsed_doc.get("image_paths", [])

            elements = [
                cl.Image(name=img[0], display="inline", path=img[1], size="large")
                for img in image_paths
            ]

        if parsed_doc is None:
            doc = message.get("content", None)
            doc = make_pretty(doc)
            
        if not doc.startswith("The Client makes the following request:"):
            cl.run_sync(cl.Message(
                content=doc,
                author=assistant.name,
                elements=elements
            ).send()
            )


            cl.run_sync(
                cl.Message(
                    content=f'**The {assistant.name} wants you to review their work above before handing off.**',
                ).send()
            )
    
    elif recipient.human_input_mode != "NEVER" and "The Client makes the following request: " not in message:
        cl.run_sync(
            cl.Message(
                content=f'{make_pretty(message)}',
                author=assistant.name
            ).send()
        )
        cl.run_sync(
            cl.Message(
                content=f'**The {assistant.name} wants you to review their work above before handing off.**',
            ).send()
        )
    elif assistant.name == "CodingAssistant" or recipient.name == "CodingAssistant":
        language = "bash" if message.startswith("exitcode:") else None
        if message.startswith("user said:") or "TERMINATE" in message: return
        cl.run_sync(
            cl.Message(
                content=f'{make_pretty(message)}',
                author=assistant.name,
                language=language
            ).send()
        )
class ChainlitAssistantAgent(AssistantAgent):


    def send(
        self,
        message: Union[Dict, str],
        recipient: Agent,
        request_reply: Optional[bool] = None,
        silent: Optional[bool] = False,
    ) -> bool:
        show_message(self, message, recipient)
   
        super(ChainlitAssistantAgent, self).send(
            message=message,
            recipient=recipient,
            request_reply=request_reply,
            silent=silent,
        )


class ChainlitUserProxyAgent(UserProxyAgent):
    def get_human_input(self, prompt: str) -> str:
        if prompt.startswith(
            ("Provide feedback to", "Please give feedback to")
        ):
            res = cl.run_sync(
                ask_helper(
                    cl.AskActionMessage,
                    content="**Please make a selection from the options below:**\n**Continue Without Feedback or Provide Feedback?**",
                    actions=[
                        cl.Action(
                            name="continue", 
                            value="continue", 
                            label="✅ Continue"
                        ),
                        cl.Action(
                            name="feedback",
                            value="feedback",
                            label="💬 Provide feedback",
                        ),  
                    ],
                    timeout=2000
                )
            )
            if res.get("value") == "continue":
                return "exit"
            # if res.get("value") == "exit":
            #     return "exit"

        reply = cl.run_sync(ask_helper(cl.AskUserMessage, content="", timeout=2000))
        return reply["content"].strip()
    

    def send(
        self,
        message: Union[Dict, str],
        recipient: Agent,
        request_reply: Optional[bool] = None,
        silent: Optional[bool] = False,
    ):
        show_message(self, message, recipient)

        super(ChainlitUserProxyAgent, self).send(
            message=message,
            recipient=recipient,
            request_reply=request_reply,
            silent=silent,
        )

