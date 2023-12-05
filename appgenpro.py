#!/usr/bin/env python3
import argparse
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
            config_path=f"{EXAMPLES_ROOT}/biapp/bi_app.json", ## TODO: hardcoded for now. it will be made configurable in the future.
            idea=TASK,
            project_name="bi_report_project", ## TODO: hardcoded for now. it will be made configurable in the future.
            root_dir=Path(WORKSPACE_ROOT),
            use_chainlit=True,
            github_token=CONFIG.github_token
        )
        task_chain.setup_environment()
        await task_chain.a_execute()
    except: 
        TASK_STATUS = cl.TaskStatus.FAILED.name
        cl.run_sync(
            cl.Message(
                content=f"**There as an unexpected error! Please check the logs for more info.**\n**Total estimated cost: ${CONFIG.total_cost:.2f}**"
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


def main():
    try:
        task_chain = TaskChain(
            config_path=args.config,
            idea=args.idea,
            project_name=args.project_name,
            root_dir=args.root_dir,
            use_chainlit=False,
            github_token=args.github_token
        )
        task_chain.setup_environment()
        task_chain.execute()
    except:
        err_msg = f"Unexpected error: {traceback.format_exc()}"
        task_chain.post_processing(task_status=cl.TaskStatus.FAILED.name)
        logger.debug(err_msg)
        logger.error(err_msg)
    finally:
        task_chain.post_processing(task_status=cl.TaskStatus.DONE.name)
        msg = f"Process completed sucessfully! All artifacts have been saved. Final estimated cost: ${CONFIG.total_cost:.2f}"
        logger.debug(msg)
        logger.info(msg)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, help="Path to config file", default=Path(f"{EXAMPLES_ROOT}/biapp/bi_app.json"))
    parser.add_argument("--idea", type=str, help="The app idea", required=True)
    parser.add_argument("--project_name", type=str, help="The name of the project", default="bi_report")
    parser.add_argument("--root_dir", type=Path, help="The root directory", default=Path(WORKSPACE_ROOT))
    parser.add_argument("--github_token", type=str, help="The github token", default=CONFIG.github_token)
    args = parser.parse_args()

    main()