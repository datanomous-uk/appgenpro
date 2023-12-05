from typing import Union, Dict, Any

class Action(object):
    def __init__(self, name: str, description: str, **kwargs):
        """
        Initializes an instance of the action class.

        Args:
            name (str): The name of the action.
            description (str): The description of the action.
            **kwargs: Additional keyword arguments.

        Returns:
            None
        """
        self.name = name
        self.description = description

    def _run(self, **context) -> Union[str, Dict, Any]:
        """
        Runs the action and returns either a message dictionary or the message content
        as a string.

        Args:
            context (dict): A dictionary containing the context for the function.

        Returns:
            Union[str, Dict, Any]: Either a string, dictionary, or any other type.
        """
        raise NotImplementedError()