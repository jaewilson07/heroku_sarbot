
import os
import asyncio
from fastapi import FastAPI
import uvicorn
from slack_bolt.async_app import AsyncApp as AsyncSlackApp
from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler

from listeners import register_listeners
from routes import init_routes

api = FastAPI()

# Initialize Slack app
async_slack_app = AsyncSlackApp(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET"))

register_listeners(async_slack_app)

# Register routes
api.include_router(init_routes(async_slack_app))

async def start_socket_mode():
    socket_handler = AsyncSocketModeHandler(async_slack_app,
                                          os.environ["SLACK_APP_TOKEN"])
    await socket_handler.start_async()

async def start_http():
    config = uvicorn.Config(api, host="0.0.0.0", port=3000)
    server = uvicorn.Server(config)
    await server.serve()

async def main():
    await asyncio.gather(
        start_socket_mode(),
        start_http()
    )

if __name__ == "__main__":
    asyncio.run(main())
