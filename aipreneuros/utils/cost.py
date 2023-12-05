from aipreneuros.utils import logger 
from aipreneuros.config import CONFIG 
from openai.types.chat import ChatCompletion

import chainlit as cl

price1K = {
        "text-ada-001": 0.0004,
        "text-babbage-001": 0.0005,
        "text-curie-001": 0.002,
        "code-cushman-001": 0.024,
        "code-davinci-002": 0.1,
        "text-davinci-002": 0.02,
        "text-davinci-003": 0.02,
        "gpt-3.5-turbo": (0.0015, 0.002),
        "gpt-3.5-turbo-instruct": (0.0015, 0.002),
        "gpt-3.5-turbo-0301": (0.0015, 0.002),  # deprecate in Sep
        "gpt-3.5-turbo-0613": (0.0015, 0.002),
        "gpt-3.5-turbo-16k": (0.003, 0.004),
        "gpt-3.5-turbo-16k-0613": (0.003, 0.004),
        "gpt-35-turbo": (0.0015, 0.002),
        "gpt-35-turbo-16k": (0.003, 0.004),
        "gpt-35-turbo-instruct": (0.0015, 0.002),
        "gpt-4": (0.03, 0.06),
        "gpt-4-32k": (0.06, 0.12),
        "gpt-4-0314": (0.03, 0.06),  # deprecate in Sep
        "gpt-4-32k-0314": (0.06, 0.12),  # deprecate in Sep
        "gpt-4-0613": (0.03, 0.06),
        "gpt-4-32k-0613": (0.06, 0.12),
        "gpt-4-1106-preview": (0.01, 0.03),
        "gpt-4-1106-vision-preview": (0.01, 0.03),
}

def estimate_cost_of_completion(rsp:ChatCompletion):
    model = rsp.model
    usage = rsp.usage
    n_input_tokens = usage.prompt_tokens
    n_output_tokens = usage.completion_tokens
    cost = estimate_cost(model, n_input_tokens, n_output_tokens)
    CONFIG.total_cost += cost 
    msg = f"*Model: {model}. Estimated cost: ${cost:.2f}. Number of Input tokens: {n_input_tokens}. Number of Output tokens: {n_output_tokens}. Running total: ${CONFIG.total_cost:.2f}.*"
    cost_msg = f"**Estimated cost of last API call:** \${cost:.2f}. **Running total:** \${CONFIG.total_cost:.2f}."
    logger.info(cost_msg)
    logger.debug(msg)
    if CONFIG.use_chainlit:
        cl.run_sync(
            cl.Message(
                content=cost_msg
            ).send()
        )
    return cost

def estimate_cost(model:str, n_input_tokens, n_output_tokens):
    if model in price1K:
        if isinstance(price1K[model], tuple):
            return (price1K[model][0] * n_input_tokens + price1K[model][1] * n_output_tokens) / 1000
        else:
            return price1K[model] * (n_input_tokens + n_output_tokens) / 1000
    else:
        return 0