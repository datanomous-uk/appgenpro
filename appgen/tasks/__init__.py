from __future__ import annotations
from .task import Task
from .analyze_data import AnalyzeData
from .gather_requirements import GatherRequirements
from .data_modelling import DataModelling
from .design_solution import DesignSolution
from .plan_development import PlanDevelopment
from .implement_solution import ImplementSolution

__all__ = [
    "Task",
    "GatherRequirements",
    "DataModelling",
    "DesignSolution",
    "PlanDevelopment",
    "ImplementSolution",
    "AnalyzeData",
]

tasks = {
    "GatherRequirements": GatherRequirements,
    "DataModelling": DataModelling,
    "DesignSolution": DesignSolution,
    "PlanDevelopment": PlanDevelopment,
    "ImplementSolution": ImplementSolution,
    "AnalyzeData": AnalyzeData
}

def get_task(name):
    if name in tasks:
        return tasks[name]
    else:
        raise ValueError(f"Task '{name}' not found. Available tasks: {list(tasks.keys())}")
    
    