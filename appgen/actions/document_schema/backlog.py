from pydantic import  Field
from appgen.actions.document_schema import Document

from pathlib import Path
from appgen.utils.mermaid import mermaid_to_file
from appgen.utils import logger, json_to_markdown
import json

def wrap_in_backticks(input_str):
    # Check if the input string is already wrapped in triple backticks
    if (input_str.startswith('```\n') or input_str.startswith('```python\n')) and (input_str.endswith('```') or input_str.endswith('```\n')):
        return input_str
    else:
        # Wrap the string in triple backticks
        return f'```python\n{input_str}\n```'


def pretty_list(input_list):
    pretty_list = []
    for item in input_list:
      if isinstance(item, (tuple, list)):
          pretty_list.append(f"**`{item[0]}`**: {item[1]}")

    return pretty_list
          

class BacklogSchema(Document):
  Title: str = "Development Backlog Document"
  PythonPackageName: str = Field(
    title="Python Package Name",
    description="Provide a package name for the project that is concise and clear. Characters must only use a combination of all lowercase and underscores.",
    default_factory=str
  )
  DependenciesandTools: list = Field(
    title="Dependencies and Tools",
    description="""List any python or non-python packages that will be necessary for implementation and briefly explain how and where these packages will be used.
    Do NOT suggest excessive or unecessary non-python tools.
    MAKE SURE to consider the tools that might be used in all aspects of the technical solution including:
      1. How the classes and functions in the class diagram will be implemented.
      2. Anything else mentioned in the design diagram that will be implemented with Python code.
    """,
    default_factory=list
  )
  RequiredPythonPackages: str = Field(
    title="Required Python Third-Party Packages and Tools",
    description="""List any third party python packages that will be necessary for implementation.
    Do NOT use deprecated versions of any packages. 
    MAKE SURE to list all the python packages mentioned in the Dependencies and Tools section.
    Provide this information in requirements.txt format.""",
    default_factory=str
  )
  TaskList: list = Field(
    title="Task List",
    description="""The list of ONLY REQUIRED files needed to write the program and the methods/functions that should be implemented in each file. 
    ALWAYS write a main.py or app.py here.
    If the program is split into components or microservices, make sure to ALWAYS split each into individual directories.  
    Only need relative paths, comply with PEP8 standards. 
  
    Use the class diagram and program flow diagrams in the design document to MAKE SURE ALL the specified classes and functions are included in each file CORRECTLY. 
    For each file, write a DETAILED explanation of how it will be implemented, consider:
      1. the classes and functions that should be implemented using the class diagram.
      2. the behavior of the classes and functions that should be implemented using the program flow diagram.
      3. any tools that will be used in the implementation of the classes and functions.
    """,
    default_factory=list
  )
  FullAPISpec: str = Field(
    title="Full API Specification",
    description="Provide in OpenAPI 3.0 format as a plain string, guarded by triple backticks like: ```<CONTENT>``` so you must fill in the <CONTENT> with the API specification. Describe all APIs that may be used by both the frontend and backend of the project. Use OpenAPI 3.0 format to document the API endpoints, request and response structures, and authentication mechanisms.",
    default_factory=str
  )


  async def parse(self, resources_path:Path=Path("resources")):
        
        self.PythonPackageName = wrap_in_backticks(self.PythonPackageName)
        self.FullAPISpec = wrap_in_backticks(self.FullAPISpec)
        self.DependenciesandTools = pretty_list(self.DependenciesandTools)
        self.TaskList = pretty_list(self.TaskList)
        
        document = self.model_dump_json(exclude=["RequiredPythonPackages"]) 
        document = json_to_markdown(json.loads(document))
       
        return {
            "document": document,
            "image_paths" : []
        }
        

  @staticmethod
  def get_format_example(**kwargs):
    backlog = BacklogSchema(
      Title="Development Backlog Document",
      PythonPackageName="""```python
package_name
```""",
      DependenciesandTools=[
      ],
      RequiredPythonPackages="""
    """,
      TaskList=[
           ("...", "...")],
      FullAPISpec=""" """
  )

    return backlog.model_dump_json()
