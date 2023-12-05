from aipreneuros.tasks import Task

class DataAnalysis(Task):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    

    def update_environment(self, environment, rsp):
        environment.requirements.append(rsp)

