from fastapi import FastAPI

import src.users.routers.version_1
import src.invoices.routers.version_1

app = FastAPI(title="ExFastAPI")

routers = [src.users.routers.version_1.router,
           src.invoices.routers.version_1.router,
           ]

for router in routers:
    app.include_router(router)
