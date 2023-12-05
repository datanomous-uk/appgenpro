# Configuration of app types

<<<<<<< Updated upstream
Appgenpro currently can be configured/extended with the config JSON files under `examples`. An example of this is at `examples/biapp/bi_app.json`.
For each app type, create a new configuration file with a team and tasks that team members will perform (similar apps will use the same configuration). You can change the config and other details at `appgenpro.py` before running.
=======
aipreneuros currently can be configured/extended with the config JSON files under `examples`. An example of this is at `examples/app_name/app_config.json` or `examples/app_name/app_inplement_only_config.json`.

For each app type, create a new configuration file with a team and tasks that team members will perform (similar apps will use the same configuration). You can change the config and other details at `aipreneuros.py` or `chat_aipreneurostpro.py` before running.
>>>>>>> Stashed changes

The JSON file will include the following configurations:

1. `team` is a list of dictionaries as well. This list describes all the various specialized agents that are used in the `tasks`. Each dictionary represents a `Role` object with the following configurable fields:
    - `role` this is the name of the role. This name must be used to specify roles used in the `tasks` and the `watch_list` of the role.
    - `goal` is the goal of the role (not task-specific, just general goal). This field forms a part of the prefix template that is used when the role makes LLM calls while executing tasks. 
    - `constraints` makes up a part of the prefix template as well. This helps guide the output of the role when it makes LLM calls.
    - `watch_list` is a list of role names (the `role` of the roles). This means that whenever this specific role sends a message, our role will be able to "think" about using one of the specified `actions` and act accordingly. You must specify `watch_list` if you specified any `actions`. If there are no `watch_list` then the agent will not act, it will only be capable of making LLM calls and following its prefix template to execute tasks.
    - `actions` is a list of actions that must be implemented as a class under `aipreneuros/actions`. These actions will be ran by the agent if the agent is talking to any role specified in `watch_list` and the action is appropriate to execute given the context of the conversation at the time. 

<<<<<<< Updated upstream
2. `tasks` is a list of dictionaries. This list describes the `TaskChain` that will be executed to build a particular app. Each dictionary represents a `TaskChain` object with configurable fields:
    - `name` of the task. This must be an implemented class under `appgen/tasks`.
=======

2. `tasks` is a list of dictionaries. This list describes the `Tasks` that will be executed to build a particular app. The tasks comes with configurable fields:
    - `name` of the task. This must be an implemented class under `aipreneuros/tasks`.
>>>>>>> Stashed changes
    - `description` of what the task does.
    - `assistant_role_name` is the assistant agent role that will work on the task. The role name must be specified in the `team`.
    - `user_role_name` is the user proxy agent that will instruct the assistant agent role to carry out the task. The role name must be specified in the `team`.
    - `task_prompt` is the prompt/prompt template that the user proxy agent will instruct the assistant agent with. this prompt must detail out what this task is and guide the output of the task carefully. you may specify placeholders in this prompt template.
    the placeholders can EITHER be the fields of the `Environment` class in the `aipreneuros/environment.py` (i.e. `requirements`, `design`, `backlog` are the environment variables that are filled in as the tasks are executed.) file OR they could be custom placeholders (constants)that you must specify.
    - `placeholders` is a dictionary where the keys are any custom placeholders you used in the `task_prompt`. organization_standards is where each user can update to customize.


