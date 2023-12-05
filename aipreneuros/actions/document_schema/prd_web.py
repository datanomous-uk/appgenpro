from pydantic import Field
from aipreneuros.actions.document_schema import Document


class PRDWebSchema(Document):

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
    UserStories: list = Field(
        title="User Stories",
        description="Provide a list of user stories to be fulfilled by this application. Specify the purpose of each user story. You can use the example user stories provided in the context as reference.",
        default_factory=list
    )
    OutOfScope: str = Field(
        title="OutofScope",
        description="""
            List all the out of scope items.
            """,
        default_factory=str
    )
    AnythingUnclear: str = Field(
        title="Anything Unclear",
        description="List any unclear aspects, questions, or additional details required to capture data requirements effectively in plain text as details for the Product Owner to consult with the client. Explain any assumptions or interpretations made when documenting requirements. If everything is clear, you must say that nothing is unclear.",
        default_factory=str
    )

    @staticmethod
    def get_format_example(**kwargs):
        prd = PRDWebSchema(
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
                "The Architecture will be modular and ...",
                "The Performance (how fast the application responds to user inputs) will be ...",
                "The Scalability (how to handle increased loads) will be ...",
                "The Reliability (how to recover from failures) will be ...",
                "The Availability (proportion of time the system is operational and accessible to the users) will be ...",
                "The Usability (UX, accessibility) will be ...",
                "The Security (Protection of the system from malicious attacks and unauthorized access, including data encryption, secure communication, and adherence to legal and compliance requirements) will be ...",
                "The Maintainability (code readability, documentation, and adherence to coding standards) will be ...",
                "The Compatibility (operate with different browsers, devices, operating systems) will be ...",
                "The Portability (moving the application to different environments) will be ...",
                "The Internationalization (adapt the application to different languages) will be ...",
                "The Responsiveness (adapt to different screen sizes and orientations) will be ...",
                "The Interoperability (integrate with other systems, APIs) will be ...",
                "The Versioning (manage different versions of the API to ensure backward compatibility) will be ...",
                "The Error Handling (robust and clear error handling mechanisms with meaningful error messages ...",
                "..."
            ],
            UserStories=[
                "As a [role], I want to [...] so that [state the reason or goal]",
                " .... "
            ],
            AnythingUnclear="Everything is clear."
        )
        return prd.model_dump_json()
