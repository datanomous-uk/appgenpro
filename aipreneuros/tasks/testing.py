from aipreneuros.tasks import Task
from aipreneuros.config import CONFIG

class Testing(Task):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def update_environment(self, environment, rsp):
        doc=CONFIG.artifacts["docs"]["sdd"]
        environment.design.append(doc)