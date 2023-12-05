from appgen.tasks import Task
from appgen.config import CONFIG

class PlanDevelopment(Task):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def update_environment(self, environment, rsp):
        doc=CONFIG.artifacts["docs"]["backlog"]
        environment.backlog.append(doc)

