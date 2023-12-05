from pydantic import BaseModel, Field
from aipreneuros.actions.document_schema import Document

from pathlib import Path
from aipreneuros.utils.mermaid import mermaid_to_file
from aipreneuros.utils import logger, json_to_markdown
import json

class FieldDefinition(BaseModel):
    FieldName: str
    DataType: str
    IsPrimaryKey: bool = False
    IsForeignKey: bool = False

class TableDefinition(BaseModel):
    TableName: str
    Fields: list[FieldDefinition]
    Description: str

class KPIDefinition(BaseModel):
    KPIName: str
    Description: str
    Calculation: str

class DataModelSchema(Document):

    class Config:
        protected_namespaces = ()
        json_schema_extra = {}

    Title: str = "Data Model Design Document"
    Standards: str = Field(
        title="Enterprise Data Standards",
        description="""Explain how you ensured alignment with any industry standards in your designs, 
        if there are any mentioned standards. If there are no industry standards mentioned in this project, 
        mention this here and explain the pros and cons of this.""",
        default_factory=str
    )
    LogicalDataModel: str = Field(
        title="Logical Data Model Design",
        description="""Create a logical data model design with fact and dimension tables. 
        Do not go into detail about all the fields of the fact and dimension tables here 
        (only provide table names and description of what the table is for and its relation to the other tables in the design), 
        just mention the overall design of the logical data model and how you will support KPI calculations and BI report generations with your data models. 
        Give a brief rationale for why you chose this design for this project over any other possible solutions. 
        State the suitable framework/tool to be used to build and manage the data models. 
        If no specific tools are given in the requirements, you may pick the best tool here and explain the rationale
        behind why you picked it for this project among other tools. 
        You must make sure that the tool you pick will allow you to create the data models with python code and manage 
        the transformation and validation of data with the data models easily with python code. """,
        default_factory=str
    )
    FactTables: list[TableDefinition] = Field(
        title="Identified Fact Tables",
        description="Identify with great DETAIL, the necessary fact tables for the logical data model you designed.",
        default_factory=list
    )
    DimensionTables: list[TableDefinition] = Field(
        title="Identified Dimension Tables",
        description="Identify with great DETAIL, the necessary dimension tables for the logical data model you designed.",
        default_factory=list
    )
    ERDiagram: str = Field(
        title="ER Diagram of the Logical Data Model",
        description="""Use mermaid entity\-relationship model (or ER model) code syntax to describe
            the data models used in the system, it should be COMPLETE and VERY DETAILED.
            Include details such as data schema, data types, and relationships between tables. 
            ALWAYS MAKE SURE you create this model based on the fact and dimension tables you have already designed for the logical data model.
            Include attribute definitions on ER diagrams to aid comprehension of the purpose and meaning of entities.""",
        default_factory=str
    )

    async def parse(self, resources_path:Path=Path("resources")):
        er_diagram = self.ERDiagram

        await mermaid_to_file(er_diagram, resources_path/"er_diagram")
        
        er_diagram_png = resources_path/"er_diagram.png"
        document = self.model_dump_json(exclude=["ERDiagram", "FactTables", "DimensionTables"])
        document = json_to_markdown(json.loads(document))

        # check the png files exist
        if not er_diagram_png.exists():
            logger.warning("Failed to generate er_diagram.png")
            return {
                "document": document,
                "image_paths" : []
            }
        
        return {
            "document": document,
            "image_paths" : [
                ("ER Diagram", str(er_diagram_png))
            ]
        }


    @staticmethod
    def get_format_example(**kwargs):
        return DataModelSchema(
            Title="Data Model Design Document",
            Standards="...",
            LogicalDataModel="The logical data model to be used in the Data Transformation part of the ETL Pipeline is ...",
            FactTables=[
                TableDefinition(
                    TableName="FACT_TABLE_NAME",
                    Fields=[
                        FieldDefinition(
                            FieldName="...",
                            DataType="...",
                            IsPrimaryKey=True,
                            IsForeignKey=False
                        ),
                    ],
                    Description="...",
                )
            ],
            DimensionTables=[
                TableDefinition(
                    TableName="DIM_TABLE_NAME",
                    Fields=[
                        FieldDefinition(
                            FieldName="...",
                            DataType="...",
                            IsPrimaryKey=True,
                            IsForeignKey=False
                        ),
                    ],
                    Description="...",
                )
            ],
            ERDiagram= """
```mermaid
erDiagram
    CUSTOMER ||--o{ ORDER : places
    CUSTOMER {
        string name
        string custNumber
        string sector
    }
    ORDER ||--|{ LINE-ITEM : contains
    ORDER {
        int orderNumber
        string deliveryAddress
    }
    LINE-ITEM {
        string productCode
        int quantity
        float pricePerUnit
    }
```
            """
        ).model_dump_json()
    