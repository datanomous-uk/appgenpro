from pathlib import Path
import chainlit as cl
import pprint

from appgen.utils import logger
from appgen.config import CONFIG
from appgen.utils.write_utils import save_document, save_code
from appgen.utils.github_utils import push_to_github


class Environment:

    def __init__(
            self,
            request_prompt: str = None,
            codebase: dict = None,
            requirements: list = None,
            design: list = None,
            backlog: list = None,
            team: dict = None,
            project_directory: Path = None,
            **kwargs
        ):
        
        self.request_prompt = request_prompt
        self.codebase = codebase
        self.requirements = requirements
        self.design = design
        self.backlog = backlog
        self.team = team
        self.project_directory = project_directory


    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        return f"request_prompt:{pprint.pformat(self.request_prompt)}\ncodebase:{pprint.pformat(self.codebase)}\nrequirements:{pprint.pformat(self.requirements)}\ndesign:{pprint.pformat(self.design)}\nbacklog:{pprint.pformat(self.backlog)}\nteam:{pprint.pformat(self.team)}\nproject_directory:{pprint.pformat(self.project_directory)}"
 
    def log(self, msg):
        logger.debug(f"**After the execution of the task: {msg}**\n\n{self.__str__()}\n\n")


    def dict(self):
        return {
            "request_prompt": self.request_prompt,
            "codebase": self.codebase,
            "requirements": self.requirements,
            "design": self.design,
            "backlog": self.backlog,
            "team": self.team,
            "project_directory": self.project_directory
        }

    def get_role(self, role_name: str):
        role = self.team.get(role_name, None)
        if not role:
            raise ValueError(f"Role '{role_name}' not found in the team. You must hire this role.")
        return role
    
    def create_task_list(self):
        self.task_list = cl.TaskList()

    async def _display_task(self, title) -> cl.Task:
        task = cl.Task(title=title, status=cl.TaskStatus.RUNNING)
        await self.task_list.add_task(task)
        await self.task_list.send()
        return task
    
    async def _finish_task(self, task):
        task.status = cl.TaskStatus.DONE
        await self.task_list.send()

    async def _update_tasks_status(self, status):
        self.task_list.status = status
        await self.task_list.send()

    def _setup_project_env(self):
        "Setup the package directory and write the requirements.txt."
        doc_name = "backlog"
        backlog_class = CONFIG.artifacts["docs"].get(doc_name, None)
        if backlog_class is None:
            logger.warning(f"The Development Backlog document named '{doc_name}' wasn't found. Cannot save the requirements.txt.")
        else:
            # package_name = backlog_class.PythonPackageName
            dependencies = backlog_class.RequiredPythonPackages
            requirements_file_path = self.project_directory / "requirements.txt"
            requirements_file_path.write_text(dependencies)

    def _save_artifacts(self):
        logger.info("Saving artifacts...")

        if "docs" in CONFIG.artifacts:
            docs = CONFIG.artifacts["docs"]
            for name, content_class in docs.items():
                save_document(content_class, name+".md", self.project_directory)
        if "code" in CONFIG.artifacts:
            code = CONFIG.artifacts["code"]
            for filename, code in code.items():
                logger.debug("Filename:{}. Code:{}".format(filename, code))
                save_code(code, filename, self.project_directory)


    def _push_project_to_repo(self, github_token:str, repository_name:str):
        # Push workspace to github and create message to share github repo link.
        link_to_repo = push_to_github(
            local_folder_path = self.project_directory,
            github_token = github_token,
            repository_name = repository_name,
        )
        return link_to_repo
    
      
    

