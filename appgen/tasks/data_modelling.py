from appgen.tasks import Task
from appgen.config import CONFIG

class DataModelling(Task):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def update_environment(self, environment, rsp):
        doc=CONFIG.artifacts["docs"]["data_model"]
        environment.design.append(doc)




