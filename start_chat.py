
import traceback
import openai
from pathlib import Path
from aipreneuros import App
import chainlit as cl
from aipreneuros.utils import logger
from aipreneuros.utils.const import AVATARS_ROOT, WORKSPACE_ROOT, EXAMPLES_ROOT
from aipreneuros.config import CONFIG
import json



'''
    Creates any application as declared in the configuration
'''

@cl.on_chat_start
async def start():

    try:
        ## Load the app configuration
        with open('aipreneuros_chat_config.json', 'r') as file:
            config = json.load(file)

        # Replace the placeholder in the configuration
        if 'config' in config and '{EXAMPLES_ROOT}' in config['config']:
            config['config'] = config['config'].replace('{EXAMPLES_ROOT}', str(EXAMPLES_ROOT))

        config_path = f"{config['config']}"
        app_name = config['name']
        
        github_token = CONFIG.github_token
        if (github_token is not None) and (github_token == ''):
            github_token = None

    except Exception as e:
        cl.run_sync(
            cl.Message(
                content=f"**There was an unexpected error:{e}!**"
            ).send()
        )

    try:
        ## Initialize the Chat
        TASK_STATUS = cl.TaskStatus.RUNNING.name
        avatar_image_path = f"{AVATARS_ROOT}/aipreneuros.png"
        if Path(avatar_image_path).exists():
            await cl.Avatar(name="aipreneuros", path=avatar_image_path).send()
        else:
            logger.warning(f"Avatar image for role 'aipreneuros' not found at {avatar_image_path}. Skipping.")
        
        ## Ask client what to do 
        res = await cl.AskUserMessage(content="Hello! What can I build for you today??", timeout=2000).send()
        TASK = res['content'] 

        ## Start the development lifecycle. Build the app
        lifecycle = App(
            config_path=config_path,
            idea=TASK,
            name=app_name,
            root_dir=Path(WORKSPACE_ROOT),
            use_chainlit=True,
            github_token=github_token
        )

        lifecycle.setup_environment()
        await lifecycle.asynch_execute()


        github_url = lifecycle.post_processing()

        if TASK_STATUS != cl.TaskStatus.RUNNING.name: return
        TASK_STATUS = cl.TaskStatus.DONE.name
        cl.run_sync(
            cl.Message(
                content=f"** Application is generated successfully! Total estimated cost: ${CONFIG.total_cost:.2f}**\n**Thank you for using aipreneuros! \n Please don't close the window just yet!.**"
            ).send()
        )
        lifecycle.update_chat_status(task_status=TASK_STATUS, github_url=github_url)
        
        msg = f"Application is generated, and pushed to {github_url} successfully! Thank you for using aipreneuros! Final estimated cost: ${CONFIG.total_cost:.2f}"
        logger.debug(msg)
        logger.info(msg)

    except Exception as e: 
        if isinstance(e, openai.RateLimitError):
            err_msg = f"Open AI Rate limit exceeded: {traceback.format_exc()}"
        else: 
            err_msg = f"Unexpected error: {traceback.format_exc()}"
    
        ## Inform the UI with the exception message
        TASK_STATUS = cl.TaskStatus.FAILED.name
        cl.run_sync(
            cl.Message(
                content=f"**There was an error {err_msg}! Please check the logs for more info.**\n**Total estimated cost: ${CONFIG.total_cost:.2f}**"
            ).send()
        )
        lifecycle.update_chat_status(task_status=TASK_STATUS)

        logger.debug(err_msg)
        logger.error(err_msg)

    
@cl.on_stop
async def stop():
    exit(0)

@cl.on_chat_end
async def end():
    logger.info("Chat ended")



