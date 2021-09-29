from fastapi import FastAPI

import users.routers

app = FastAPI(title="ExFastAPI")

routers = [users.routers.router,
           ]

for router in routers:
    app.include_router(router)
