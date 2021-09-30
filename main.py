from fastapi import FastAPI

import src.users.routers

app = FastAPI(title="ExFastAPI")

routers = [src.users.routers.router,
           ]

for router in routers:
    app.include_router(router)
