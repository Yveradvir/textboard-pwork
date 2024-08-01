import os
from uvicorn import run

from src.core.makeapp import makeapp
from src.core.lifespan import lifespan

if __name__ == "__main__":
    cwd = os.path.dirname(__file__)
    
    python_path = os.path.join(cwd)
    os.environ['PYTHONPATH'] = python_path 

    app = makeapp(
        lifespan=lifespan
    )

    run(app)