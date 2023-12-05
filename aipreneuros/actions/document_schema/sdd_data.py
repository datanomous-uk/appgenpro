from pydantic import Field
from aipreneuros.actions.document_schema import Document

from pathlib import Path
from aipreneuros.utils.mermaid import mermaid_to_file
from aipreneuros.utils import logger, json_to_markdown
import json

class SDDDataSchema(Document):

    

    Title: str = "Software Design Document"
    HighLevelSystemDesign: str = Field(
        title="High-Level System Design",
        description="""Provide an overview of how the functionality and responsibilities of the system were partitioned and then
        assigned to subsystems or components. Don't go into too much detail about the
        individual components themselves in this section. The main purpose here is to
        gain a general understanding of how and why the system was decomposed, and how
        the individual parts work together to provide the desired functionality. 
        Describe how the higher-level components collaborate with each other in order 
        to achieve the required results. Provide some sort of rationale for choosing this
        particular decomposition of the system (perhaps discussing other proposed 
        decompositions and why they were rejected).""",
        default_factory=str
    )
    DataIngestion: str = Field(
        title="Data Ingestion Implementation Details",
        description="""If this is a data and analytics application, explain how data from the specified data sources will be ingested into the system. 
        Include details about data connectors, data flow, and ingestion methods. 
        ALWAYS write step-by-step DETAILED instructions for how to implement the data ingestion process.
        """,
        default_factory=str
    )
    DataCuration: str = Field(
        title="Data Curation Implementation Details",
        description="""If this is a data and analytics application, describe the process of cleaning, enriching, and structuring raw data to ensure its quality and compatibility with the system.
        Include steps such as duplicate removal, null value handling, and data validation.
        ALWAYS write step-by-step DETAILED instructions for how to implement the data curation process.""",
        default_factory=str
    )
    DataTransformation: str = Field(
        title="Data Transformation Implementation Details",
        description="""If this is a data and analytics application, explain how curated data will be transformed into a suitable format for analysis, reporting, or storage. 
        Discuss data modeling, schema changes, and any additional metrics generation.
        ALWAYS write step-by-step instructions for how to implement the data transformation process
        ALWAYS include DETAILED instructions on how the data models designed in this document will be implemented and used in the step by step transformation process.
        """,
        default_factory=str
    )
    DataScience: str = Field(
        title="Data Science Implementation Details",
        description="""If this is a data and analytics application, detail how data will be used for feature engineering and predictive model building, including the choice of data science libraries and methods. 
        ALWAYS write step-by-step DETAILED instructions for implementing the visual representations of the transformed data that meet the user requirements.
        """,
        default_factory=str
    )
    DataVisualization: str = Field(
        title="Data Visualization Implementation Details",
        description="""If this is a data and analytics application, detail how data will be visualized, including the choice of visualization tools and methods. 
        ALWAYS write step-by-step DETAILED instructions for implementing the visual representations of the transformed data that meet the user requirements.
        """,
        default_factory=str
    )
    Orchestration: str = Field(
        title="Orchestration Implementation Details",
        description="""If this is a data and analytics application, outline how various components of the system will be coordinated and managed to ensure seamless data processing and workflow execution.
        ALWAYS write step-by-step DETAILED instructions for implementing the orchestration process.
        """,
        default_factory=str
    )
    API: str = Field(
        title="API Details",
        description="""Outline the APIs to be created.
        ALWAYS write step-by-step DETAILED instructions for implementing them.
        """,
        default_factory=str
    )
    ClassDiagrams: str = Field(
        title="Data structures and/or Interface Definitions To Be Implemented",
        description="""Use mermaid classDiagram code syntax,
            including classes (INCLUDING __init__ method) and functions (with type annotations),
            CLEARLY MARK the RELATIONSHIPS between classes, and comply with PEP8 standards.
            The data structures SHOULD BE VERY DETAILED and the API should be comprehensive with
            a complete design.
            
            ALWAYS MAKE SURE you create these class diagrams based on the design of the microservices above and how they will be implemented.
            MAKE SURE you include all the necessary functions for each microservice class to behave as you designed and explained above.
            Given the data model design document, you must include the data model class here with all the necessary functions and marks of how the data model class relates to the microservice classes.
            """,
        default_factory=str
    )
    ProgramFlow: str = Field(
        title="Program Flow To Be Implemented",
        description="""Use mermaid sequenceDiagram code syntax, COMPLETE and VERY DETAILED,
            using CLASSES AND API DEFINED ABOVE accurately, covering the CRUD AND INIT of each
            object, SYNTAX MUST BE CORRECT.""",
        default_factory=str
    )

  
    async def parse(self, resources_path:Path=Path("resources")):
        class_diagrams = self.ClassDiagrams
        program_flow = self.ProgramFlow

        await mermaid_to_file(class_diagrams, resources_path/"class_diagram")
        await mermaid_to_file(program_flow, resources_path/"program_flow")

        class_diagram_png = resources_path/"class_diagram.png"
        program_flow_png = resources_path/"program_flow.png"

        document = self.model_dump_json(exclude=["ClassDiagrams", "ProgramFlow"])
        document = json_to_markdown(json.loads(document))
    
        if not class_diagram_png.exists() or not program_flow_png.exists():
            logger.warning("Failed to generate class_diagram.png or program_flow.png")
            return {
                "document": document,
                "image_paths" : []
            }
        
        return {
            "document": document,
            "image_paths" : [
                ("Class Diagram", str(class_diagram_png)),
                ("Program Flow", str(program_flow_png)),
            ]
        }
        

    @staticmethod
    def get_format_example(**kwargs):
        sdd = SDDDataSchema(
            Title="Software Design Document",
            HighLevelSystemDesign="Document the solution based on the architecture suggested.",
            ClassDiagrams="""```mermaid
                classDiagram
                    class ClassName{
                        +function_name() -> Any
                    }
                    class OtherClassName{
                        +other_function_name(param: str) -> Any
                    }    
                    ClassName "1" -- "1" OtherClassName: uses
                ```""",
                            ProgramFlow="""```mermaid
                sequenceDiagram
                    participant Main as Main
                    participant ClassName as ClassNameAPI

                    Main->>ClassNameAPI: function_name()
                ```"""
        )
        return sdd.model_dump_json()