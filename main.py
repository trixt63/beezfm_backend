# See PyCharm help at https://www.jetbrains.com/help/pycharm/
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.apis import objects, datapoints

app = FastAPI(
    title="Hotel Monitoring System API",
    description="RESTful API for managing hotel objects and datapoints",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Modify for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(objects.router, tags=["Objects"])
app.include_router(datapoints.router, tags=["Datapoints"])

@app.get("/", tags=["Root"])
async def root():
    return {"message": "Welcome to Hotel Monitoring System API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)