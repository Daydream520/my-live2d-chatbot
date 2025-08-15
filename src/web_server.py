from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Backend is running"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received message: {data}")
            await websocket.send_text(f"Message received: {data}")
    except WebSocketDisconnect:
        pass
    finally:
        print("Client disconnected")
