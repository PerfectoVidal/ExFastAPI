from fastapi import FastAPI
from src.routers.v1.invoices import router as router_invoices_version_1
from src.routers.v1.users import router as router_users_version_1
from src.routers.v1.auth import router as router_auth_version_1

app = FastAPI(title="ExFastAPI")

routers = [router_auth_version_1,
           router_users_version_1,
           router_invoices_version_1,
           ]

for router in routers:
    app.include_router(router)
