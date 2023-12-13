import traceback
from pathlib import Path

from appgen import TaskChain
import chainlit as cl
from appgen.utils import logger
from appgen.utils.const import AVATARS_ROOT, WORKSPACE_ROOT, EXAMPLES_ROOT
from appgen.config import CONFIG


@cl.on_chat_start
async def start():

    try:
        TASK_STATUS = cl.TaskStatus.RUNNING.name
        avatar_image_path = f"{AVATARS_ROOT}/AppGenPro.png"
        if Path(avatar_image_path).exists():
            await cl.Avatar(name="AppGenPro", path=avatar_image_path).send()
        else:
            logger.warning(f"Avatar image for role 'AppGenPro' not found at {avatar_image_path}. Skipping.")
        
        res = await cl.AskUserMessage(content="Hello! What can I build for you today??", timeout=2000).send()
        TASK = res['content'] 

        task_chain = TaskChain(
            config_path=f"{EXAMPLES_ROOT}/webapp/web_app.json", ## TODO: hardcoded for now. it will be made configurable in the future.
            idea=TASK,
            project_name="web_app_project", ## TODO: hardcoded for now. it will be made configurable in the future.
            root_dir=Path(WORKSPACE_ROOT),
            use_chainlit=True,
            github_token=CONFIG.github_token
        )
        task_chain.setup_environment()
        await task_chain.a_execute()
    except Exception as e: 
        TASK_STATUS = cl.TaskStatus.FAILED.name
        cl.run_sync(
            cl.Message(
                content=f"**There was an unexpected error:{e}! Please check the logs for more info.**\n**Total estimated cost: ${CONFIG.total_cost:.2f}**"
            ).send()
        )
        task_chain.post_processing(task_status=TASK_STATUS)
        err_msg = f"Unexpected error: {traceback.format_exc()}"
        logger.debug(err_msg)
        logger.error(err_msg)
    finally:
        if TASK_STATUS != cl.TaskStatus.RUNNING.name: return
        TASK_STATUS = cl.TaskStatus.DONE.name
        cl.run_sync(
            cl.Message(
                content=f"**The {task_chain.project_name} project is completed. Total estimated cost: ${CONFIG.total_cost:.2f}**\n**I will now save all artifacts and do some post-processing. Please don't close the window just yet!.**"
            ).send()
        )
        task_chain.post_processing(task_status=TASK_STATUS)
        msg = f"Process completed sucessfully! All artifacts have been saved. Final estimated cost: ${CONFIG.total_cost:.2f}"
        logger.debug(msg)
        logger.info(msg)
    

@cl.on_stop
async def stop():
    exit(0)

@cl.on_chat_end
async def end():
    logger.info("Chat ended")