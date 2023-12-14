from __future__ import annotations
from .task import Task
from .data_analysis import DataAnalysis
from .requirements_gathering import RequirementsGathering
from .data_modelling import DataModelling
from .solution_design import SolutionDesign
from .technical_design import TechnicalDesign
from .implementation import Implementation

__all__ = [
    "Task",
    "RequirementsGathering",
    "DataModelling",
    "SolutionDesign",
    "TechnicalDesign",
    "Implementation",
    "DataAnalysis",
]

tasks = {
    "RequirementsGathering": RequirementsGathering,
    "DataModelling": DataModelling,
    "SolutionDesign": SolutionDesign,
    "TechnicalDesign": TechnicalDesign,
    "Implementation": Implementation,
    "DataAnalysis": DataAnalysis
}

def get_task(name):
    if name in tasks:
        return tasks[name]
    else:
        raise ValueError(f"Task '{name}' not found. Available tasks: {list(tasks.keys())}")
    
    