from __future__ import annotations
from .action import Action
from .write_document import (
    WriteDocument,
    WriteRequirementsDocument,
    WriteDataModelDocument,
    WriteTechnicalDesignDocument,
    WriteDevelopmentBacklogDocument
)
from .write_code import WriteCode
from .analyze_data import AnalyzeData

__all__ = [
    "WriteDocument",
    "WriteRequirementsDocument",
    "WriteDataModelDocument",
    "WriteTechnicalDesignDocument",
    "WriteDevelopmentBacklogDocument",
    "WriteCode",
    "AnalyzeData",
]

actions = {
    "WriteDocument": WriteDocument,
    "WriteRequirementsDocument": WriteRequirementsDocument,
    "WriteDataModelDocument": WriteDataModelDocument,
    "WriteTechnicalDesignDocument": WriteTechnicalDesignDocument,
    "WriteDevelopmentBacklogDocument": WriteDevelopmentBacklogDocument,
    "WriteCode": WriteCode,
    "AnalyzeData": AnalyzeData
}

def get_action(action_name: str) -> Action:
    if action_name not in actions:
        raise ValueError(f"Action {action_name} not found. Available actions: {', '.join(actions.keys())}")
    return actions[action_name]