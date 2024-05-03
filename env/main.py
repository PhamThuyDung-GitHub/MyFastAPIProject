from fastapi import FastAPI, WebSocket, HTTPException
from pydantic import BaseModel
from typing import Optional
import asyncio

app = FastAPI()

class SensorData(BaseModel):
    temperature: Optional[float] = None
    light: Optional[int] = None

# In-memory storage to simulate database operations
data_store = {
    "sensor_data": SensorData()
}

@app.get("/", response_model=SensorData)
async def get_data():
    return {
        "error": False,
        "message": "Fetched sensor data",
        "data": data_store["sensor_data"]
    }

@app.post("/", response_model=SensorData)
async def post_data(data: SensorData):
    data_store["sensor_data"] = data
    return {
        "error": False,
        "message": "Data updated",
        "data": data_store["sensor_data"]
    }

@app.put("/", response_model=SensorData)
async def put_data(data: SensorData):
    if not data_store["sensor_data"]:
        raise HTTPException(status_code=404, detail="Data not found")
    data_store["sensor_data"] = data
    return {
        "error": False,
        "message": "Data replaced",
        "data": data_store["sensor_data"]
    }

@app.delete("/", response_model=SensorData)
async def delete_data():
    data_store["sensor_data"] = SensorData()
    return {
        "error": False,
        "message": "Data cleared",
        "data": data_store["sensor_data"]
    }

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = data_store["sensor_data"]
            await websocket.send_json({
                "error": False,
                "message": "Live sensor data",
                "data": data
            })
            await asyncio.sleep(1)  # Send data every second
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        await websocket.close()
        print("WebSocket connection closed")
