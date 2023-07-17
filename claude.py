from os import getenv
from typing import Union

from fastapi import FastAPI, Depends, Header, HTTPException, status
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from sse_starlette.sse import EventSourceResponse

from slack import client
from  proxy import get_proxy
app = FastAPI()
server_token = getenv("SERVER_TOKEN")


async def must_token(x_token: Union[str, None] = Header(None)):
    if server_token and x_token != server_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "msg": "must token",
            }
        )


class ClaudeChatPrompt(BaseModel):
    prompt: str


@app.post("/claude/chat", dependencies=[Depends(must_token)])
async def chat(body: ClaudeChatPrompt):
    await client.open_channel()
    await client.chat(body.prompt)
    reply = await client.get_reply()
    print(reply)
    replyres  =await  get_proxy(reply)
    while replyres.strip() != reply.strip():
        await  client.chat( replyres)
        reply = await client.get_reply()
        replyres =await  get_proxy(reply)
    
    return {
        "claude": replyres
    }

# add --no-buffer to see the effect of streaming
# curl -X 'POST'  --no-buffer \
#  'http://127.0.0.1:8088/claude/stream_chat' \
#  -H 'accept: text/plain' \
#  -H 'Content-Type: application/json' \
#  -d '{
#  "prompt": "今天天气很不错吧"}'
@app.post("/claude/stream_chat", dependencies=[Depends(must_token)])
async def chat(body: ClaudeChatPrompt):
    await client.open_channel()
    await client.chat(body.prompt)
    return EventSourceResponse(client.get_stream_reply(), ping=100)

@app.post("/claude/reset", dependencies=[Depends(must_token)])
async def chat():
    await client.open_channel()
    await client.chat("请忘记上面的会话内容")

    return {
        "claude": await client.get_reply()
    }


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8088)
