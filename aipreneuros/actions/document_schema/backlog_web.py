from pydantic import  Field
from aipreneuros.actions.document_schema import Document

from pathlib import Path
from aipreneuros.utils.mermaid import mermaid_to_file
from aipreneuros.utils import logger, json_to_markdown
import json


class BacklogWebSchema(Document):

  Title: str = "Development Backlog Document"
  PackageName: str = Field(
    title="Package Name",
    description="Provide a package name for the project that is concise and clear. Characters must only use a combination of all lowercase and underscores.",
    default_factory=str
  )
  UX: list = Field(
    title="UX Requirements",
    description="""
    If the project involves a user interface, include guidelines or references to UI/UX design standards and assets (like wireframes, style guides).
    """,
    default_factory=list
  )
  TaskList: list = Field(
    title="Task List",
    description="""
    First group the requirements into domains and then come up with independent components based on the solution design document.
    And use the class diagram and program flow diagrams in the design document to MAKE SURE ALL IS DEFINED CORRECTLY. 
    For each component, write a DETAILED tasks to be implemented, consider:
      1. The components are independent from each other.
      2. Each component needs to implement related functional and non-functional requirements.
      3. Integrate user stories and acceptance criteria within the Task List to align development tasks with user needs and expectations.
      4. Think, evaluate, and valiate if all the tasks map to requirements and solution design.
    """,
    default_factory=list
  )
  ImplementationList: list = Field(
    title="Implementation List",
    description="""
    For each task in the Task List, define the classes and write pseudocode for each to implement the required functionality as functions. Assume, anticipate, suggest and define the required business logic to implement each function in the class thoroughly.
    Use the class diagram and program flow diagrams in the design document to MAKE SURE ALL the specified classes and functions are included in each file and are defined CORRECTLY. 
    For each class, write a DETAILED explanation of how it will be implemented, consider:
      1. Write pseudocode for each class to define the functions to be implemented.
      2. The classes and functions that should be implemented using the class diagram.
      2. the behavior of the classes and functions that should be implemented using the program flow diagram.
      3. any tools that will be used in the implementation of the classes and functions.
      4. Create the class under a folder representing the component defined in the Task List.
      5. Create APIs that may be used by both the frontend and backend of the project. Use OpenAPI 3.0 format (guarded by triple backticks like: ```<CONTENT>``` so you must fill in the <CONTENT> with the API specification) to document the API endpoints, request and response structures, and authentication mechanisms.
      6. Create the main.py to run all the components implemented from one place.
      7. Think, evaluate, and valiate if functions are defined correctly to map to requirements and solution design.
    """,
    default_factory=list
  )
  RequiredPackages: str = Field(
    title="Required Third-Party Packages and Tools",
    description="""List any third party packages that will be necessary for implementation.
    Do NOT use deprecated versions of any packages. 
    MAKE SURE to list all the packages mentioned in the Dependencies and Tools section.
    Provide this information in requirements.txt format.""",
    default_factory=str
  )
  DependenciesandTools: list = Field(
    title="Dependencies and Tools",
    description="""List any packages that will be necessary for implementation and briefly explain how and where these packages will be used.
    Do NOT suggest excessive or unecessary tools.
    MAKE SURE to consider the tools that might be used in all aspects of the technical solution including:
      1. How the classes and functions in the class diagram will be implemented.
      2. Anything else mentioned in the design diagram that will be implemented.
    """,
    default_factory=list
  )
  Security: list = Field(
    title="Security",
    description="""
    Outline the security best practices, covering aspects such as secure coding, data encryption, and vulnerability management.
      1. Mention compliance requirements if the application is subject to specific regulations (like GDPR, HIPAA).
    """,
    default_factory=list
  )
  TestCases: list = Field(
    title="Test Cases",
    description="""
    Outline the testing approach including unit tests, integration tests, system tests, and acceptance tests.
      1. Mention the frameworks and tools to be used for testing, and guidelines for writing test cases.
      2. Include steps for automated testing, building, and deployment processes.
      3. Mention Quality assurance (QA) practices, and coding standards to ensure code quality.
    """,
    default_factory=list
  )


  """
  Parses the specified resources path to generate a document and return it along with an empty list of image paths.

  :param resources_path: The path to the resources directory. Default is `Path("resources")`.
  :type resources_path: Path

  :return: A dictionary containing the generated document and an empty list of image paths.
  :rtype: dict
  """
  async def parse(self, resources_path:Path=Path("resources")):
        
        self.PackageName = pretty_list(self.PackageName)
        self.UX = wrap_in_backticks(self.UX)
        self.TaskList = pretty_list(self.TaskList)
        self.ImplementationList = pretty_list(self.ImplementationList)
        self.DependenciesandTools = pretty_list(self.DependenciesandTools)
        self.Security = pretty_list(self.Security)
        self.TestCases = pretty_list(self.TestCases)

        document = self.model_dump_json(exclude=["RequiredPackages"]) 
        document = json_to_markdown(json.loads(document))
       
        return {
            "document": document,
            "image_paths" : []
        }

       
  """
    Generate the function comment for the given function body in a markdown code block with the correct language syntax.

    Args:
        **kwargs: Additional keyword arguments.

    Returns:
        str: The function comment in markdown format.
  """   
  @staticmethod
  def get_format_example(**kwargs):
    backlog = BacklogWebSchema(
      Title="Development Backlog Document",
      PackageName="""```python
      package_name
      ```""",
            DependenciesandTools=[
              ("yaml", "To load the configuration file, config.yaml, into a singleton Config class for easy access."),
              ("flask", "To create the web application and API endpoints."),
              ("...", "...")
            ],
            RequiredPackages="""
            PyYAML
            flask
          """,
        TaskList=[
            ("main.py", "The starting point to run the application ....."),
            ("config/config.yaml", "Contains the configuration. The configurations include ... "),
            ("config/config.py", "Contains a singleton Config class that loads the config.yaml file for easy access throughout the framework.  This class will be used by ... to ... The following functions will need to be implemented ..."),
            ("...", "...")],

            FullAPISpec = """```python
            openapi: 3.0.0
            info:
              title: "Example API"
              version: "1.0.0"
            paths:
              /path/to/endpoint:
                post:
                  summary: "Example POST operation"
                  requestBody:
                    required: true
                    content:
                      application/json:
                        schema:
                          type: object
                          properties:
                            exampleField:
                              type: string
                  responses:
                    '200':
                      description: "Successful operation"
            ```"""
            )

    return backlog.model_dump_json()


    """
    Wrap the input string in triple backticks if it is not already wrapped.
    
    Args:
        input_str (str): The input string to be wrapped.
        
    Returns:
        str: The input string wrapped in triple backticks.
    """
def wrap_in_backticks(input_str):
    # Check if the input string is already wrapped in triple backticks
    if (input_str.startswith('```\n') or input_str.startswith('```python\n')) and (input_str.endswith('```') or input_str.endswith('```\n')):
        return input_str
    else:
        # Wrap the string in triple backticks
        return f'```python\n{input_str}\n```'

    """
    Generate a pretty list from an input list.
    
    Args:
        input_list (list): The input list to be processed.
    
    Returns:
        list: The generated pretty list.
    """
def pretty_list(input_list):
    pretty_list = []
    for item in input_list:
      if isinstance(item, (tuple, list)):
          pretty_list.append(f"**`{item[0]}`**: {item[1]}")

    return pretty_list
          
