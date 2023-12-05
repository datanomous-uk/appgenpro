from pydantic import Field
from aipreneuros.actions.document_schema import Document

from pathlib import Path
from aipreneuros.utils.mermaid import mermaid_to_file
from aipreneuros.utils import logger, json_to_markdown
import json

class SDDWebSchema(Document):

    Title: str = "Software Design Document"
    HighLevelSystemDesign: str = Field(
        title="High-Level System Design",
        description="""
        Create a blueprint for the system to be developed and should cover all technical aspects of the project. 
        Here are the key sections you MUST include in your Solution Design Document without FAIL:
        1. Introduction: Overview of the project, including its purpose and objectives.
        2. Scope of the Solution: Outline the boundaries of the solution, including what is in and out of scope. Identify the primary users and other stakeholders of the system.
        3. Architecture Overview: High-level architecture diagram showing the main components of the application. Description of the architectural style (e.g., microservices, monolithic) and rationale for the chosen approach.
        4. Technology Stack: List and justify the selection of technologies for the frontend, backend, database, and any other significant components. Include frameworks, programming languages, database systems, and any other relevant technologies.
        5. Detailed System Design: Break down the system into smaller components or modules. Provide detailed diagrams and descriptions for each component, including their interactions and data flow.
        6. API Design: Define the RESTful API endpoints, request/response structures, and HTTP methods. Include any third-party APIs that the application will integrate with.
        7. Non functionals: 
        a. Security Design: Outline the security measures and protocols to protect the system and data. Include authentication, authorization, data encryption, and compliance with security standards.
        b. Performance Considerations: Describe how the system will handle load and performance requirements. Include strategies for scaling, caching, and optimizing performance.
        c. Other non0functionals as addressed in the requirements document.
        8. Deployment Strategy: Detail the deployment process, including continuous integration and continuous deployment (CI/CD) pipelines.
        9. Testing Strategy: Outline the approach for quality assurance, including types of tests (unit, integration, system) and testing tools. Include test cases, test data, and criteria for test success.
        10. Risk Management: Identify potential risks in the implementation of the solution and mitigation strategies.
        """,
        default_factory=str
    )
    UIMocks: str = Field(
        title="UI Mockups",
        description="""
            Use mermaid to create mockups or wireframes of key screens/pages of the application.
            Detail the user and data flows and interaction with the application.
            """,
        default_factory=str
    )
    ArchitectureDiagram: str = Field(
        title="Architecture",
        description="""
            Use mermaid to draw the architecture of the application.
            """,
        default_factory=str
    )
    ClassDiagrams: str = Field(
        title="Class diagrams",
        description="""
            Use mermaid to create Class diagram with classDiagram code syntax, including classes (INCLUDING __init__ method) and functions (with type annotations),
            CLEARLY MARK the RELATIONSHIPS between classes, and comply with PEP8 standards.
            The data structures SHOULD BE VERY DETAILED and the API should be comprehensive with a complete design.
            MAKE SURE you include all the necessary functions for each class.
            """,
        default_factory=str
    )
    SequenceFlow: str = Field(
        title="Sequence Flow",
        description="""
            Use mermaid sequenceDiagram code syntax, COMPLETE and VERY DETAILED,
            using CLASSES AND API DEFINED ABOVE accurately, covering the CRUD AND INIT of each
            object, SYNTAX MUST BE CORRECT.""",
        default_factory=str
    )
    DataDiagram: str = Field(
        title="ERD",
        description="""
            Use mermaid code syntax, COMPLETE and VERY DETAILED, to crreate an Entity-Relationship Diagram (ERD) with detailed database schema.
            """,
        default_factory=str
    )
    OutOfScope: str = Field(
        title="OutofScope",
        description="""
            List all the out of scope items.
            """,
        default_factory=str
    )
    

    async def parse(self, resources_path:Path=Path("resources")):

        architecture_diagrams = self.ArchitectureDiagram
        class_diagrams = self.ClassDiagrams
        sequence_flow = self.SequenceFlow
        data_diagram = self.DataDiagram
        ui_mocks = self.UIMocks
        
        await mermaid_to_file(architecture_diagrams, resources_path/"architecture_diagrams")
        await mermaid_to_file(class_diagrams, resources_path/"class_diagram")
        await mermaid_to_file(sequence_flow, resources_path/"sequence_flow")
        await mermaid_to_file(data_diagram, resources_path/"data_diagram")
        await mermaid_to_file(ui_mocks, resources_path/"ui_mocks")

        architecture_diagram_png = resources_path/"architecture_diagram_png.png"
        class_diagram_png = resources_path/"class_diagram.png"
        sequence_flow_png = resources_path/"sequence_flow.png"
        data_diagram_png = resources_path/"data_diagram.png"
        ui_mocks_png = resources_path/"ui_mocks.png"

        document = self.model_dump_json(exclude=["Architecture", "ClassDiagrams", "SequenceFlow", "DataDiagram", "UIMocks"])
        document = json_to_markdown(json.loads(document))
    
        if not class_diagram_png.exists() or not sequence_flow_png.exists() or not data_diagram_png.exists() or not ui_mocks_png.exists():
            logger.warning("Failed to generate diagrams")
            return {
                "document": document,
                "image_paths" : []
            }
        
        return {
            "document": document,
            "image_paths" : [
                ("Architecture Diagram", str(architecture_diagram_png)),
                ("Class Diagram", str(class_diagram_png)),
                ("Sequence Flow", str(sequence_flow_png)),
                ("Data Diagram", str(data_diagram_png)),
                ("UI Mocks", str(ui_mocks_png)),
            ]
        }
        

      

    @staticmethod
    def get_format_example(**kwargs):
        sdd = SDDWebSchema(
            Title="Software Design Document",
            HighLevelSystemDesign="Document the solution based on the architecture suggested as standards.",
            ArchitectureDiagram="""```mermaid
            graph LR
                A[Web Frontend] --> B{API Server}
                B --> C[Database]
                B --> D[Cache]
                E[External Service] --> B
            ```""",
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
             SequenceFlow="""```mermaid
                sequenceDiagram
                    participant Main as Main
                    participant ClassName as ClassNameAPI

                    Main->>ClassNameAPI: function_name()
                ```"""
        )
        return sdd.model_dump_json()