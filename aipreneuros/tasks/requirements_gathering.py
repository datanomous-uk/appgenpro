from aipreneuros.tasks import Task
from aipreneuros.config import CONFIG

class RequirementsGathering(Task):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    

    def update_environment(self, environment, rsp):

        if "prd" in CONFIG.artifacts["docs"]:
            reqs = CONFIG.artifacts["docs"]["prd"]
            environment.requirements.append(reqs)

