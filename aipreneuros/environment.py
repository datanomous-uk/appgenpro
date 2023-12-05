from pathlib import Path
import chainlit as cl
import pprint
import json
from aipreneuros.utils import logger
from aipreneuros.config import CONFIG
from aipreneuros.utils.write_utils import save_document, save_code
from aipreneuros.utils.github_utils import push_to_github

'''
    The Environment class manages and maintain the context of a software development lifecycle. 
'''
class Environment:

    def __init__(
            self,
            request_prompt: str = None,
            codebase: dict = None,
            requirements: list = None,
            design: list = None,
            backlog: list = None,
            team: dict = None,
            directory: Path = None,
            **kwargs
        ):
        
        self.request_prompt = request_prompt
        self.codebase = codebase
        self.requirements = requirements
        self.design = design
        self.backlog = backlog
        self.team = team
        self.directory = directory



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


    def _save_artifacts(self):
        logger.info(f"Saving artifacts: {CONFIG.artifacts}")
        

        if "backlog" in CONFIG.artifacts:
            backlog = CONFIG.artifacts["backlog"]
            for name, content_class in backlog.items():
                logger.debug("Filename:{}. Doc:{}".format(content_class, name))
                save_document(content_class, name+".md", self.directory)


        if "docs" in CONFIG.artifacts:
            docs = CONFIG.artifacts["docs"]
            for name, content_class in docs.items():
                logger.debug("Filename:{}. Doc:{}".format(content_class, name))
                save_document(content_class, name+".md", self.directory)
                logger.debug("{content_class} artifact saved.")

            backlog_class = docs.get("backlog", None)
            if backlog_class:
                dependencies = backlog_class.RequiredPackages
                requirements_file_path = self.directory / "requirements.txt"
                requirements_file_path.write_text(dependencies)
                logger.debug("Requirements.txt saved.")
            else:
                logger.warning(f"The Development Backlog document wasn't found. Skipping the creation of requirements.txt.")

        if "code" in CONFIG.artifacts:
            code = CONFIG.artifacts["code"]
            for filename, code in code.items():
                logger.debug("Filename:{}. Code:{}".format(filename, code))
                save_code(code, filename, self.directory)
            logger.debug("Code artifact saved.")



    def _push_to_repo(self, github_token:str, repository_name:str):
        # Push workspace to github and create message to share github repo link.
        link_to_repo = push_to_github(
            local_folder_path = self.directory,
            github_token = github_token,
            repository_name = repository_name,
        )
        return link_to_repo
    
      
    
    def get_role(self, role_name: str):
        role = self.team.get(role_name, None)
        if not role:
            raise ValueError(f"Role '{role_name}' not found in the team. You must hire this role.")
        return role
    

    def dict(self):
        return {
            "request_prompt": self.request_prompt,
            "codebase": self.codebase,
            "requirements": self.requirements,
            "design": self.design,
            "backlog": self.backlog,
            "team": self.team,
            "directory": self.directory
        }
    
    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        return f"request_prompt:{pprint.pformat(self.request_prompt)}\ncodebase:{pprint.pformat(self.codebase)}\nrequirements:{pprint.pformat(self.requirements)}\ndesign:{pprint.pformat(self.design)}\nbacklog:{pprint.pformat(self.backlog)}\nteam:{pprint.pformat(self.team)}\ndirectory:{pprint.pformat(self.directory)}"
 
    def log(self, msg):
        logger.debug(f"**After the execution of the task: {msg}**\n\n{self.__str__()}\n\n")


