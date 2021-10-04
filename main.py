from fastapi import FastAPI
from src.users.routers.version_1 import router as v1_user_router
from src.invoices.routers.version_1 import router as v1_invoice_router

app = FastAPI(title="ExFastAPI")

routers = [v1_user_router,
           v1_invoice_router,
           ]

for router in routers:
    app.include_router(router)
