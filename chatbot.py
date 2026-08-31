import os
import chainlit as cl
from chainlit.data.sql_alchemy import SQLAlchemyDataLayer
from core.database import authenticate
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableConfig
from typing import cast, Optional

from functools import lru_cache

MODEL_IDS = {"qwen3:4b", "llama3.2:1b", "tinyllama:latest"}
DEFAULT_MODEL = "tinyllama:latest"

REASONING_TEMPS = {"low": 0.5, "high": 1.2}
DEFAULT_REASONING = "low"

@cl.data_layer
def get_data_layer():
    return SQLAlchemyDataLayer(conninfo=os.environ["DATABASE_URL"],show_logger=True)

@cl.password_auth_callback
async def auth_callback(username:str, password:str) -> Optional[str]:
    user = await authenticate(username, password)
    if user:
        return cl.User(identifier=user.username, metadata={"role": user.role, "provider": "credentials"})
    return None


def build_runnable(model_id: str, reasoning: str):
    temperature = REASONING_TEMPS.get(reasoning, 1.2)
    model = ChatOllama(model=model_id, temperature=temperature, num_ctx=1536)
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You're a very knowledgeable historian who provides accurate and eloquent answers to historical questions."),
            ("human", "{question}"),
        ]
    )
    return prompt | model | StrOutputParser()


@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("chat_history", [])
    model_mode = cl.Mode(
        id="model",
        name="Model",
        options=[
            cl.ModeOption(id="qwen3:4b", name="Qwen3:4b", icon="sparkles"),
            cl.ModeOption(id="llama3.2:1b", name="Llama3.2:1b", icon="sparkles"),
            cl.ModeOption(id="tinyllama:latest", name="TinyLlama", icon="bolt", default=True),
        ],
    )
    reasoning_mode = cl.Mode(
        id="reasoning",
        name="Reasoning",
        options=[
            cl.ModeOption(id="high", name="High Effort", description="Think harder"),
            cl.ModeOption(id="low", name="Low Effort", description="Faster response", default=True),
        ],
    )
    await cl.context.emitter.set_modes([model_mode, reasoning_mode])

    # cache built runnables per (model, reasoning) combo for this session
    cl.user_session.set("runnable_cache", {})


@cl.on_chat_resume
async def on_chat_resume(thread):
    cl.user_session.set("runnable_cache", {})
    # cl.user_session.set("chat_history", [])

    # for step in thread.get("steps", []):
    #     if step.get("type") == "user_message":
    #         cl.user_session.get("chat_history").append({
    #             "role": "user",
    #             "content": step.get("output", "")
    #         })

    #     elif step.get("type") == "assistant_message":
    #         cl.user_session.get("chat_history").append({
    #             "role": "assistant",
    #             "content": step.get("output", "")
    #         })

    
@cl.on_message
async def on_message(message: cl.Message):

    # cl.user_session.get("chat_history",[]).append({"role": "user", "content": message.content})

    model_id = message.modes.get("model", DEFAULT_MODEL) if message.modes else DEFAULT_MODEL
    reasoning = message.modes.get("reasoning", DEFAULT_REASONING) if message.modes else DEFAULT_REASONING

    cache = cl.user_session.get("runnable_cache") or {}
    cache_key = (model_id, reasoning)

    runnable = cache.get(cache_key)
    if runnable is None:
        runnable = build_runnable(model_id, reasoning)
        cache[cache_key] = runnable
        cl.user_session.set("runnable_cache", cache)

    msg = cl.Message(content="")
    async for chunk in runnable.astream(
        {"question": message.content},
        config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()]),
    ):
        await msg.stream_token(chunk)
    await msg.send()

