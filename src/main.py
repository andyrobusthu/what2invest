from fastapi import FastAPI,Depends,Response
from src.core.config import Settings


app = FastAPI(description="fastapi项目练习实战")


@app.get("/")
def read_root(settings: Settings=Depends()):
    return {
        "message": f"Hello from the {settings.app_name}",
        "database_url": settings.database_url,
        "jwt_secret": settings.jwt_secret
    }


@app.get("/health")
async def health_check(response: Response):
    response.status_code = 200
    return {"status":"ok man!"}
