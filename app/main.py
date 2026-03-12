from fastapi import FastAPI

from app.routes import auth


app = FastAPI(
    title="YOUR PROJECT NAME",
)


app.include_router(auth.router)


@app.get("/")
async def root():
    return {
        "message": "API",
        "docs": "/docs",
        "endpoints": {
            "auth": "/auth",
        },
    }


@app.get("/health")
async def health_check():
    return {"status": "ok"}
