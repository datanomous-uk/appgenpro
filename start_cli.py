import argparse
import traceback
from pathlib import Path
import openai
from aipreneuros import App
from aipreneuros.utils.const import WORKSPACE_ROOT, EXAMPLES_ROOT
from aipreneuros.config import CONFIG
from aipreneuros.utils import logger


'''
    Creates any application as declared in the configuration
'''
def main():

    # Let the development lifecyle begin
    try:
        lifecycle = App(
            config_path=args.config,
            idea=args.idea,
            name=args.name,
            root_dir=args.root_dir,
            use_chainlit=False,
            github_token=CONFIG.github_token
        )

        doc = ''
        try:
            ## Load backlog documentation
            with open(f"{Path(WORKSPACE_ROOT)}/{args.backlog}", 'r', encoding='utf-8') as file:
                doc = file.read()
        
        except Exception as e:
            logger.error(f"Failed to load backlog documentation: {e}")


        lifecycle.setup_environment({args.root_dir}, backlog =[doc])
        lifecycle.execute()
        ## Save the artifacts and push the code into github repo
        lifecycle.post_processing()
        msg = f"Application is generated (and deployed) successfully! Thank you for using aipreneuros! Final estimated cost: ${CONFIG.total_cost:.2f}"
        logger.debug(msg)
        logger.info(msg)
    except Exception as e:
        if isinstance(e, openai.RateLimitError):
            err_msg = f"Open AI Rate limit exceeded: {traceback.format_exc()}"
        else: 
            err_msg = f"Unexpected error: {traceback.format_exc()}"

        logger.debug(err_msg)
        logger.error(err_msg)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, help="The configuration file of the app", required=True)
    parser.add_argument("--idea", type=str, help="Enter the app idea", required=True)
    parser.add_argument("--name", type=str, help="The name of the app to be generated", required=True)
    ## Optional
    parser.add_argument("--root_dir", type=Path, help="The workspace directory where the app will be generated", default=Path(WORKSPACE_ROOT), required=False)
    ## Optional - if not provided, they will be generated with human in the loop
    parser.add_argument("--backlog", type=str, help="The technical backlog of the app to be generated, if any", default=None, required=False)
    parser.add_argument("--requirements", type=str, help="The requirements of the app to be generated, if any", default=None, required=False)
    parser.add_argument("--design", type=str, help="The technical design of the app to be generated, if any", default=None, required=False)
    args = parser.parse_args()

    main()