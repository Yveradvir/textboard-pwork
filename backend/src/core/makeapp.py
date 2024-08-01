from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

def makeapp(lifespan) -> FastAPI:
    """
        Function that makes instance of FastAPI and sets it up.
        
        Args:
            lifespan (async generator) - to make actions before and after app initialization.
        Return:
            app (FastApi) - instance of web application.
    """
    app = FastAPI(
        debug=True, 
        lifespan=lifespan
    )
    
    app.add_middleware(
        CORSMiddleware, allow_credentials = True, 
        allow_origins = [
            "http://localhost:4200"
        ],
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
        allow_headers=["*"],
    ) # this line allows provided methods and header only from allow_origins
    
    return app