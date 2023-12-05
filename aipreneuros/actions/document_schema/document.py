from pydantic import BaseModel
from pathlib import Path
import json

from aipreneuros.utils import json_to_markdown

class Document(BaseModel):
    """
    The base Document class to define a document schema.
    A document schema allows you to enforce agents to output
    structured outputs and improves the predictability/reusability of
    your agents across different app types.

    You should extend this class to define your document schema.

    To define the contents of the document, define each subsection
    as an attribute of this class using a Field object to describe
    the subsection.
    """

    class Config:
        protected_namespaces = ()
        json_schema_extra = {}
    @staticmethod
    def get_format_example(**kwargs):
        """
        Return a format example of the document class by providing an example
        of each field without context.

        Parameters:
            **kwargs: Additional keyword arguments.

        Raises:
            NotImplementedError: If the method is not implemented.

        Returns:
            None
        """
        
        raise NotImplementedError()
    
    async def parse(self, resources_path:Path=Path("resources")):
        """
        Parses the resources and returns a dictionary containing the document content in markdown
        format and an empty list of image paths.
        The document and image paths are returned are to be displayed on the chat UI.

        Override this function to parse and save images for any of the fields where you expect 
        images/diagrams to be generated.

        :param resources_path: The path to the resources directory. Defaults to "resources".
        :type resources_path: Path

        :return: A dictionary containing the parsed document and a list of image paths.
        :rtype: dict
        """
        document = self.model_dump_json()
        document = json_to_markdown(json.loads(document))
        return {
                "document": document,
                "image_paths" : []
            }
