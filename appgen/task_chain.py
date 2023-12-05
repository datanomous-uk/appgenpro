import json

from pathlib import Path
import chainlit as cl

from appgen import Environment
from appgen.utils import logger
from appgen.utils.const import AVATARS_ROOT
from appgen.config import CONFIG
from appgen.tasks import get_task
from appgen.roles.role import Role

class TaskChain:

    def __init__(
            self,
            config_path: str = None,
            idea: str = None,
            project_name: str = None,
            root_dir: Path = None,
            use_chainlit: bool = False,
            github_token: str = None,
            **kwargs
        ):

        self.config_path = config_path
        self.idea = idea
        self.project_name = project_name
        self.root_dir = root_dir

        with open(self.config_path, 'r', encoding="utf8") as file:
            self.config = json.load(file)

        self.use_chainlit = use_chainlit
        CONFIG.use_chainlit = self.use_chainlit

        self.use_github = github_token is not None
        if self.use_github:
            self.github_token = github_token
        
        if self.use_github and self.github_token is None:
            raise Exception("You must provide your '--github-token' to use github.")


        
    def setup_environment(self):
        # Initialize the team 
        team = self._initialize_team()
        project_directory = self._initialize_directory()

        # Initialize the environment
        self.environment = Environment(
            request_prompt=self.idea,
            codebase={},
            requirements=[],
            design=[],
            backlog=[],
            team=team,
            project_directory=project_directory
        )


        # Initialize the tasks
        self.tasks = []
        for task in self.config["tasks"]:
            task_class_name = task.pop("name")
            task_class = get_task(task_class_name)
            self.tasks.append(task_class(**task))


        if self.use_chainlit:
            self.environment.create_task_list()


    def execute(self):
        for task in self.tasks:
            task.execute(self.environment)

    
    async def a_execute(self):
        # logger.warning(cl.TaskStatus.RUNNING.name)
        await self.environment._update_tasks_status(cl.TaskStatus.RUNNING.name)
        for task in self.tasks:
            await task.a_execute(self.environment)
    


    def _initialize_team(self):
        team = {}
        for role_dict in self.config["team"]:
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
    
    def _initialize_directory(self) -> Path:
        self.root_dir.mkdir(parents=True, exist_ok=True)
        project_dir = self.root_dir / self.project_name
        project_dir.mkdir(parents=True, exist_ok=True)
        return project_dir
    

    def post_processing(self, task_status=cl.TaskStatus.DONE.name):
        self.environment._setup_project_env()
        self.environment._save_artifacts()
        if self.use_github:
            github_url = self.environment._push_project_to_repo(self.github_token, self.project_name)
        if self.use_chainlit and self.use_github:
            cl.run_sync(
                cl.Message(
                    content=f'All artifacts have been pushed to GitHub!\nPlease visit this link: {github_url}\nThank you for using AppGenPro!',
                ).send()
            )
        if self.use_chainlit:
            cl.run_sync(
                self.environment._update_tasks_status(task_status)
            )


    def __repr__(self) -> str:
        return self.__str__()
    
    def __str__(self):
        return f"config_path:{self.config_path}\nidea:{self.idea}\nproject_name:{self.project_name}\nroot_dir:{self.root_dir}\ntasks:{self.tasks}\nuse_chainlit:{self.use_chainlit}"




