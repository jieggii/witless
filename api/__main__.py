from fastapi import FastAPI
import uvicorn
import asyncio
import logging

import api
import api.util
from api.generator import generator


logging.basicConfig(level="INFO")


app = FastAPI()
MESSAGES = {}


@app.on_event("startup")
async def update_messages_wrapper():
    loop = asyncio.get_event_loop()
    loop.create_task(update_messages())


@app.get("/generate")
async def generate(data: dict):
    peer_id = data["peer_id"]
    size = data["size"]

    storage = api.MessagesStorage(peer_id)
    messages = await storage.get()

    result = generator.generate(
        samples=messages, tries_count=25, size=api.util.convert_size(size)
    )
    if result:
        result = await api.censor_result(result)
        result = await api.improve_result(result)
        return {"success": True, "result": result}

    else:  # not enough samples to generate message
        return {"success": False}


@app.get("/count")
async def get(data: dict):
    peer_id = data["peer_id"]

    storage = api.MessagesStorage(peer_id)
    count = len(await storage.get())
    return {"success": True, "result": count}


@app.get("/wipe")
async def delete(data: dict):
    peer_id = data["peer_id"]

    storage = api.MessagesStorage(peer_id)
    result = await storage.wipe()

    if result:
        return {"success": True}

    else:  # *.raw file does not exist yet
        return {"success": False}


@app.get("/push")
async def add(data: dict):
    peer_id = data["peer_id"]
    message = data["message"]

    try:
        MESSAGES[peer_id].append(message)

    except KeyError:
        MESSAGES[peer_id] = [message]

    return {"success": True}


@app.get("/stats")
async def stats(data: dict):
    count, global_size, local_size = await api.Stats.get(data["peer_id"])
    return {
        "success": True,
        "count": count,
        "global_size": global_size,
        "local_size": local_size,
    }


async def update_messages():
    while True:
        logging.info(f"Writing {MESSAGES}")
        for peer_id, messages in MESSAGES.copy().items():
            storage = api.MessagesStorage(peer_id)
            await storage.push(messages)

        MESSAGES.clear()

        await asyncio.sleep(25)


uvicorn.run(app)
