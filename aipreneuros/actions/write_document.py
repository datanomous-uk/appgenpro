import json

from typing import Type, Union, Dict, Any
from pydantic import BaseModel
import asyncio

from aipreneuros.actions import Action
from aipreneuros.actions.document_schema import (
    PRDDataSchema,
    BacklogDataSchema,
    SDDDataSchema,
    DataModelSchema,
    PRDWebSchema,
    BacklogWebSchema,
    SDDWebSchema
)
from aipreneuros.utils import logger, json_to_markdown
from aipreneuros.utils.cost import estimate_cost_of_completion
from aipreneuros.config import CONFIG

DOCUMENT_PROMPT_TEMPLATE = """
# Format example:
{format_example}
-----
AIM: Based on your conversation records so far, fill in ALL the fields of the format example and return it in full.

If the previous document is provided, YOU MUST build on top of this document. 
This means that you will edit this document and add on the feedback provided in the requirements. Make sure you only change the necessary parts of the document to follow the given feedback, DO NOT make any other changes.

YOU MUST note that the format example is just an example and should be used as a guide only.
DO NOT just copy the format example word by word. 
YOU MUST consider the context and the requirements and adapt it accordingly to the given format.

If the requirements are unclear, ensure minimum viability and avoid excessive design. 
Output a JSON STRING and do NOT wrap the JSON string in quotes or backticks. 
"""

class WriteDocument(Action):
    """
    Write a Structured Documentation and return the result.

    Args:
        name (str): The name of the tool.
        description (str): The description of the tool. 
        document_schema (Type[BaseModel]): The schema of the document. Example: PRDSchema
        document_name (str): The name of the document. Example: prd
        document_prompt_template (str): The prompt template to generate the document.
    """

    def __init__(
        self,
        name:str, 
        description:str,  
        document_schema:Type[BaseModel],
        document_name:str,
        document_prompt_template:str = DOCUMENT_PROMPT_TEMPLATE,
        **kwargs
    ):
        super().__init__(name, description)

        self.document_schema = document_schema
        self.document_name = document_name
        self.document_prompt_template = document_prompt_template
        
    
    def _run(self, client, messages=[], system_message=[], **context) -> Union[str, Dict, Any]:
        # Initialize the prompt template with the document schema details.
        prompt = self.document_prompt_template.format(
            format_example=self.document_schema.get_format_example()
        )
        msg = [{
            "role": "assistant",
            "content": prompt
        }]

        # Initialize the LLM config and request chat completion using oai.
        config_list = CONFIG.config_list
        logger.debug(config_list)

        rsp = client.create(
            context=messages[-1].pop("context", None), messages=system_message+messages+msg
        )
        estimate_cost_of_completion(rsp)
        rsp = client.extract_text_or_function_call(rsp)[0]

        # Parse the response using the document schema and save it to the docs artifacts.
        content = self.document_schema.model_validate_json(rsp)
        
        docs = CONFIG.artifacts["docs"]
        docs[self.document_name] = content

        # TODO: keep environment memory with own message definitions
        # also define actionmessage to store the document classes in memory
        # and retrieve them later OR use memgpt!
        if CONFIG.use_chainlit:
            content = content.model_copy()
            parsed_doc = asyncio.run(content.parse())
            return {
                "content": json_to_markdown(json.loads(content.model_dump_json())),
                "parsed_doc": parsed_doc
            }
        return json_to_markdown(json.loads(content.model_dump_json()))



class WriteDataRequirementsDocument(WriteDocument):

    def __init__(
        self,
        name:str = "write_requirements_document", 
        description:str = "Write a Requirements Document and return the result.",  
        document_schema:Type[BaseModel] = PRDDataSchema,
        document_name:str = "prd",
        document_prompt_template:str = DOCUMENT_PROMPT_TEMPLATE,
        **kwargs
    ):
        super().__init__(name, description, document_schema, document_name, document_prompt_template)


class WriteDataModelDocument(WriteDocument):

    def __init__(
        self,
        name:str = "write_data_model_document", 
        description:str = "Write a data model documentation and return the result.",  
        document_schema:Type[BaseModel] = DataModelSchema,
        document_name:str = "data_model",
        document_prompt_template:str = DOCUMENT_PROMPT_TEMPLATE,
        **kwargs
    ):
        super().__init__(name, description, document_schema, document_name, document_prompt_template)


class WriteDataTechnicalDesignDocument(WriteDocument):

    def __init__(
        self,
        name = "write_design_document",
        description = "Write a design document and return the result.",
        document_schema = SDDDataSchema,
        document_name = "sdd",
        document_prompt_template:str = DOCUMENT_PROMPT_TEMPLATE,
        **kwargs
    ):
        super().__init__(name, description, document_schema, document_name, document_prompt_template)


class WriteDataDevelopmentBacklogDocument(WriteDocument):

    def __init__(
        self,
        name = "write_backlog_document",
        description = "Write a backlog document and return the result.",
        document_schema = BacklogDataSchema,
        document_name = "backlog",
        document_prompt_template:str = DOCUMENT_PROMPT_TEMPLATE,
        **kwargs
    ):
        super().__init__(name, description, document_schema, document_name, document_prompt_template)



class WriteWebRequirementsDocument(WriteDocument):

    def __init__(
        self,
        name:str = "write_requirements_document", 
        description:str = "Write a Requirements Document and return the result.",  
        document_schema:Type[BaseModel] = PRDWebSchema,
        document_name:str = "prd",
        document_prompt_template:str = DOCUMENT_PROMPT_TEMPLATE,
        **kwargs
    ):
        super().__init__(name, description, document_schema, document_name, document_prompt_template)



class WriteWebTechnicalDesignDocument(WriteDocument):

    def __init__(
        self,
        name = "write_design_document",
        description = "Write a design document and return the result.",
        document_schema = SDDWebSchema,
        document_name = "sdd",
        document_prompt_template:str = DOCUMENT_PROMPT_TEMPLATE,
        **kwargs
    ):
        super().__init__(name, description, document_schema, document_name, document_prompt_template)


class WriteWebDevelopmentBacklogDocument(WriteDocument):

    def __init__(
        self,
        name = "write_backlog_document",
        description = "Write a backlog document and return the result.",
        document_schema = BacklogWebSchema,
        document_name = "backlog",
        document_prompt_template:str = DOCUMENT_PROMPT_TEMPLATE,
        **kwargs
    ):
        super().__init__(name, description, document_schema, document_name, document_prompt_template)