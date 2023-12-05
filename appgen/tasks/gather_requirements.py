from appgen.tasks import Task
from appgen.config import CONFIG

class GatherRequirements(Task):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    

    def update_environment(self, environment, rsp):
        reqs = CONFIG.artifacts["docs"]["prd"]
        environment.requirements.append(reqs)

