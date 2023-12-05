import json

from pathlib import Path
import chainlit as cl

from aipreneuros import Environment
from aipreneuros.utils import logger
from aipreneuros.utils.const import AVATARS_ROOT
from aipreneuros.config import CONFIG
from aipreneuros.tasks import get_task
from aipreneuros.roles.role import Role

''' 
The App class is designed to automate the software development lifecycle. 
'''

class App:

    def __init__(
            self,
            config_path: str = None,
            idea: str = None,
            name: str = None,
            root_dir: Path = None,
            use_chainlit: bool = False,
            github_token: str = None,
            **kwargs
        ):

        self.config_path = config_path
        self.idea = idea
        self.name = name
        self.root_dir = root_dir

        with open(self.config_path, 'r', encoding="utf8") as file:
            self.config_path = json.load(file)

        self.use_chainlit = use_chainlit
        CONFIG.use_chainlit = self.use_chainlit

        self.use_github = github_token is not None
        if self.use_github:
            self.github_token = github_token
        
        if self.use_github and self.github_token is None:
            raise Exception("You must provide your '--github-token' to use github.")


    '''
    Initializes the environment, codebase, requirements, design, backlog, and team.
    Reads tasks from the configuration and initializes them in the envrionment.
    '''
    def setup_environment(self, codebase={}, requirements=[], design=[], backlog=[]):
        
        # Initialize the workspace 
        directory = self._initialize_directory()
        
        # Initialize the team 
        team = self._initialize_team()


        # Initialize the environment that manages 
        self.environment = Environment(
            request_prompt=self.idea,
            codebase=codebase,
            requirements=requirements,
            design=design,
            backlog=backlog,
            team=team,
            directory=directory
        )


        # Initialize the tasks
        self.tasks = []
        for task in self.config_path["tasks"]:
            task_class_name = task.pop("name")
            task_class = get_task(task_class_name)
            self.tasks.append(task_class(**task))

        if self.use_chainlit:
            self.environment.create_task_list()


    '''
    Creates the root directory and a sub-directory to store the app generated, ensuring they exist.
    '''
    def _initialize_directory(self) -> Path:
        self.root_dir.mkdir(parents=True, exist_ok=True)
        dir = self.root_dir / self.name
        dir.mkdir(parents=True, exist_ok=True)
        return dir
    


    '''
    Reads team roles from the configuration and creates corresponding role objects.
    For Chainlit integration, sets up user sessions and avatars for team roles.
    '''
    def _initialize_team(self):
        team = {}
        for role_dict in self.config_path["team"]:
            role_class = Role.from_dict(role_dict)
            # role_class = get_role(role_name)
            # role = role_class(profile=role_name)
            role_name = role_dict.get("role")
            team[role_name] = role_class
            
            if self.use_chainlit:
                cl.user_session.set(role_name, team[role_name])
                avatar_image_path = f"{AVATARS_ROOT}/{role_name}.png"
                if Path(avatar_image_path).exists():
                    cl.run_sync(cl.Avatar(
                        name=role_name,
                        path=avatar_image_path
                    ).send())
                else:
                    logger.warning(f"Avatar image for role '{role_name}' not found. Skipping.")
        return team
    




    '''
     Iterates over the tasks list and executes each task synchronously in the order they appear.
    '''
    def execute(self):
        for task in self.tasks:
            task.execute(self.environment)

    

    '''
    Used by the chainlint integration.
    Updates the task status to RUNNING using Chainlit.
    Iterates over the tasks list and executes each task asynchronously.
    '''
    async def asynch_execute(self):
        await self.environment._update_tasks_status(cl.TaskStatus.RUNNING.name)
        for task in self.tasks:
            await task.a_execute(self.environment)
    


    '''
    Perform the post-processing steps after the execution of all tasks.
    If GitHub integration is enabled, pushes the app to a GitHub repository.
    '''
    def post_processing(self):
        
        self.environment._save_artifacts()
        
        url =None
        if self.use_github:
            url = self.environment._push_to_repo(self.github_token, self.name)

        return url
    

    '''
    For Chainlit integration, sends completion messages and updates task status.
    '''
    def update_chat_status(self, task_status=cl.TaskStatus.DONE.name, github_url=None):
        
        if github_url:
            cl.run_sync(
                cl.Message(
                    content=f'All artifacts have been pushed to GitHub!\nPlease visit this link: {github_url}',
                ).send()
            )

        if self.use_chainlit:
            self.environment._update_tasks_status(task_status)


    def __repr__(self) -> str:
        return self.__str__()
    
    def __str__(self):
        return f"config_path:{self.config_path}\nidea:{self.idea}\nname:{self.name}\nroot_dir:{self.root_dir}\ntasks:{self.tasks}\nuse_chainlit:{self.use_chainlit}"




