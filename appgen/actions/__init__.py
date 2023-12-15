from __future__ import annotations
from .action import Action
from .write_document import (
    WriteDocument,
    WriteWebRequirementsDocument,
    WriteDataModelDocument,
    WriteWebTechnicalDesignDocument,
    WriteWebDevelopmentBacklogDocument,
    WriteDataRequirementsDocument,
    WriteDataTechnicalDesignDocument,
    WriteDataDevelopmentBacklogDocument
)
from .write_code import WriteCode
from .analyze_data import AnalyzeData

__all__ = [
    "WriteDocument",
    "WriteWebRequirementsDocument",
    "WriteDataModelDocument",
    "WriteWebTechnicalDesignDocument",
    "WriteWebDevelopmentBacklogDocument",
    "WriteDataRequirementsDocument",
    "WriteDataTechnicalDesignDocument",
    "WriteDataDevelopmentBacklogDocument",
    "WriteCode",
    "AnalyzeData",
]

actions = {
    "WriteDocument": WriteDocument,
    "WriteWebRequirementsDocument": WriteWebRequirementsDocument,
    "WriteDataModelDocument": WriteDataModelDocument,
    "WriteWebTechnicalDesignDocument": WriteWebTechnicalDesignDocument,
    "WriteWebDevelopmentBacklogDocument": WriteWebDevelopmentBacklogDocument,
    "WriteDataRequirementsDocument": WriteDataRequirementsDocument,
    "WriteDataTechnicalDesignDocument": WriteDataTechnicalDesignDocument,
    "WriteDataDevelopmentBacklogDocument": WriteDataDevelopmentBacklogDocument,
    "WriteCode": WriteCode,
    "AnalyzeData": AnalyzeData
}

def get_action(action_name: str) -> Action:
    if action_name not in actions:
        raise ValueError(f"Action {action_name} not found. Available actions: {', '.join(actions.keys())}")
    return actions[action_name]