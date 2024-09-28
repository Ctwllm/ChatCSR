import os

import javalang.parse
# from langchain import PromptTemplate
from langchain_core.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain.memory import ChatMessageHistory
from langchain_community.callbacks import get_openai_callback

import tiktoken
import openai

from src.llm.config import API_KEY, MAX_PROMPT_TOKENS
from src.utils.syntactic_repair import SyntacticRepair
from prompt_templates import system_prompt
from src.utils.log import logger

number_to_word = {
    1: "first",
    2: "second",
    3: "third",
    4: "fourth",
    5: "fifth",
    6: "sixth",
    7: "seventh",
    8: "eighth",
    9: "ninth",
    10: "tenth"
}


def ask_llm(message: str, package_name: str, save_path: str, max_try_times=5) -> bool:
    chat = ChatOpenAI(model='gpt-3.5-turbo', temperature=0.2, api_key=API_KEY, openai_api_base="https://hk.xty.app/v1")

    prompt_template = ChatPromptTemplate.from_messages(
        [
            SystemMessage(content=system_prompt.system_prompt),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )

    chain = prompt_template | chat

    chat_history = ChatMessageHistory()
    chat_history.add_user_message(message=message)

    if num_tokens_from_chatmessagehistory(chat_history.messages) > MAX_PROMPT_TOKENS:
        print("The number of tokens in the prompt is too large, please try again")
        return False

    while max_try_times > 0:
        try:
            response = chain.invoke({"messages": chat_history.messages})

            syntactic_repair = SyntacticRepair(response.content)

            test_code_without_code_block = syntactic_repair.remove_code_block()

            #  这里的修复逻辑还不完整，缺少编译错误的修复
            if not syntactic_repair.is_syntactic_correct(test_code_without_code_block):
                code_after_syntactic_repair = syntactic_repair.structure_repair()
                code_after_package_repair = syntactic_repair.package_repair(package_name)
            else:
                code_after_package_repair = syntactic_repair.package_repair(package_name)

            folder_path = os.path.dirname(save_path)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            with open(save_path, 'w', encoding='utf-8') as file:
                file.write(code_after_package_repair)
                logger.info(f"Save test code to {save_path}")
            return True
        except Exception as e:
            print(f"Error: {e}")
            if "This model's maximum context length is 4097 tokens." in str(e):
                logger.error("This model's maximum context length is 4097 tokens.")
                break
            if "Connection error." in str(e):
                logger.error("openai.APIConnectionError")
        max_try_times -= 1
    return False


def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613"):
    """Return the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model in {
        "gpt-3.5-turbo-0613",
        "gpt-3.5-turbo-16k-0613",
        "gpt-4-0314",
        "gpt-4-32k-0314",
        "gpt-4-0613",
        "gpt-4-32k-0613",
        }:
        tokens_per_message = 3
        tokens_per_name = 1
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif "gpt-3.5-turbo" in model:
        print("Warning: gpt-3.5-turbo may update over time. Returning num tokens assuming gpt-3.5-turbo-0613.")
        return num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613")
    elif "gpt-4" in model:
        print("Warning: gpt-4 may update over time. Returning num tokens assuming gpt-4-0613.")
        return num_tokens_from_messages(messages, model="gpt-4-0613")
    else:
        raise NotImplementedError(
            f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens."""
        )
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens


def num_tokens_from_string(string: str, encoding_name="cl100k_base") -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


"""
    Returns the number of tokens in a prompt template.
"""
def num_tokens_from_template(prompt_template: ChatPromptTemplate, encoding_name="cl100k_base") -> int:
    num_tokens = 0
    for template in prompt_template.messages:
        # print(template.content)
        # print(num_tokens_from_string(template.content))
        num_tokens += num_tokens_from_string(template.content)
    return num_tokens


def num_tokens_from_chatmessagehistory(history_messages: list, encoding_name="cl100k_base") -> int:
    num_tokens = 0
    for message in history_messages:
        # print(template.content)
        # print(num_tokens_from_string(template.content))
        num_tokens += num_tokens_from_string(message.content)
    return num_tokens


if __name__ == '__main__':
    prompt = system_prompt.system_prompt
    print(num_tokens_from_string(prompt))
