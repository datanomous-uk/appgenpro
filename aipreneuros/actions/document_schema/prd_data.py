from pydantic import Field
from aipreneuros.actions.document_schema import Document


class PRDDataSchema(Document):

    Title: str = "Requirements Document"
    Purpose: str = Field(
        title="Purpose and Scope",
        description="Provide a brief overview of the purpose and scope of the application. If the original requirements are vague, make assumptions and explain your rationale.",
        default_factory=str
    )
    Assumptions: list = Field(
        title="Assumptions",
        description="Provide a list of the assumptions. If the original requirements are vague, make assumptions and explain your rationale.",
        default_factory=list
    )
    FunctionalRequirements: list = Field(
        title="Functional Requirements",
        description="Provide a list of the functional requirements. If the original requirements are vague, make assumptions and explain your rationale.",
        default_factory=list
    )
    NonFunctionalRequirements: list = Field(
        title="Non-Functional Requirements",
        description="Provide a list of the non-functional requirements. If the original requirements are vague, make assumptions and explain your rationale.",
        default_factory=list
    )
    DataSources: list = Field(
        title="Data Sources and Ingestion",
        description="If this is a data and analytics application, provide a list of the data sources to be ingested by this application. If there are no data sources mentioned in the original requirements, then make assumptions based on the given information and make a clear note of why you made these assumptions.", 
        default_factory=list
    )
    DataCuration: list = Field(
        title="Data Curation",
        description="If this is a data and analytics application, provide as a list of the data cleaning and preprocessing needs. Specify data transformation or enrichment requirements. If the original requirements lack details, make assumptions and clarify your reasoning.",
        default_factory=list
    )
    DataTransformation: list = Field(
        title="Data Transformation",
        description="If this is a data and analytics application, provide a list of data metrics to be calculated. Define how each metric should be computed in plain text. If the original requirements are vague, make assumptions and explain your rationale.",
        default_factory=list
    )
    DataScience: list = Field(
        title="Data Science",
        description="If this is a data and analytics application, provide list of predictive analytics requirements for forecasting (time series, behavioural analysis), anomaly detection, root-cause analysis, recommendations. If the original requirements lack specifics, make assumptions and provide reasoning.",
        default_factory=list
    )
    DataVisualization: list = Field(
        title="Data Visualization",
        description="If this is a data and analytics application, provide the list of data visualizations or charts needed for data analysis. Describe the content and format of each visualization. Explain how each visualization should be presented to answer each requirementIf the original requirements lack specifics, make assumptions and provide reasoning.",
        default_factory=list
    )
    DataSecurityAndPrivacy: list = Field(
        title="Data Security and Privacy",
        description="If this is a data and analytics application, outline data security and privacy requirements related to data handling and access in plain text. Specify any encryption or access control measures. If the original requirements lack specifics, make assumptions and provide your reasoning.",
        default_factory=list
    )
    Orchestration: list = Field(
        title="Orchestration",
        description="If this is a data and analytics application, provide a clear description of the application's data orchestration requirements. If the original requirements are vague, make assumptions and provide reasoning.",
        default_factory=list
    )
    UIRequirements: list = Field(
        title="User Interface Requirements",
        description="Provide a clear description of the application's user interface requirements. If the original requirements are vague, make assumptions and provide reasoning.",
        default_factory=list
    )
    API: list = Field(
        title="APIs",
        description="Provide a list of APIs to be fulfilled by this application. Specify the purpose of each API.",
        default_factory=list
    )
    UserStories: list = Field(
        title="User Stories",
        description="Provide a list of user stories to be fulfilled by this application. Specify the purpose of each user story. You can use the example user stories provided in the context as reference.",
        default_factory=list
    )
    AnythingUnclear: str = Field(
        title="Anything Unclear",
        description="List any unclear aspects, questions, or additional details required to capture data requirements effectively in plain text as details for the Product Owner to consult with the client. Explain any assumptions or interpretations made when documenting requirements. If everything is clear, you must say that nothing is unclear.",
        default_factory=str
    )

    @staticmethod
    def get_format_example(**kwargs):
        prd = PRDDataSchema(
            Title="Requirements Document",
            Purpose="""The purpose of this document is to outline the requirements for a ... """,
            Assumptions=[
                "The application should be able to ...",
                "..."
            ],
            FunctionalRequirements=[
                "The application should be able to ...",
                "..."
            ],
            NonFunctionalRequirements=[
                "An ETL architecture will be used for the data pipeline. ...",
                "The data will be ...",
                "The data will be modelled using ...",
                "..."
            ],
            DataSources=[
                "... Database ... accessed from ...", 
                "... API ... accessed from ...", 
                "... Cloud Storage Services ... accessed from ...",
                " ..... "
                ],
            DataCuration=[
                "Missing values will be handled by ... ",
                "Data normalization techniques including ... will be applied where necessary.",
                " ..... "
            ],
            DataTransformation=[
                "The following KPIs will be defined: ... will be defined and calculated using specific business logic.",
                " .... "
            ],
            DataScience=[
                "The following predictive models will be defined: ...",
                " .... "
            ],
            DataVisualization=[
                "The following visualizations will be created: ...",
                " .... "
            ],
            DataSecurityAndPrivacy=[
                "All sensitive data will be handled in compliance with GDPR, HIPAA, ... or other relevant regulations.",
                "All data will be stored securely in encrypted form. ...",
                " ..... "
            ],
            Orchestration=[
                "The application will be orchestrated using ....",
                " ... "
            ],
            API=[
                "The application will use the following APIs ....",
                " ... "
            ],
            UIRequirements=[
                "The application will be accessed by ....",
                "The UI will have the following functionalities ...",
                " .... "
            ],
            UserStories=[
                "As a [role], I want to [capture specific data] so that [state the reason or goal]",
                "As a [role], I want to [perform a specific data analysis] to [achieve a particular outcome].",
                " .... "
            ],
            AnythingUnclear="Everything is clear."
        )
        return prd.model_dump_json()
