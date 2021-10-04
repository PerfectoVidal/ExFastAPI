from fastapi import FastAPI

import src.users.routers
import src.invoices.routers

app = FastAPI(title="ExFastAPI")

routers = [src.users.routers.router,
           src.invoices.routers.router,
           ]

for router in routers:
    app.include_router(router)
