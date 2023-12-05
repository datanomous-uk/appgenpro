from appgen.tasks import Task
from appgen.config import CONFIG

class ImplementSolution(Task):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def update_environment(self, environment, rsp):
        environment.codebase.update(CONFIG.artifacts["code"])


 
    
