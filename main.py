from fastapi import FastAPI
from src.routers.v1.invoices import router as router_invoices_version_1
from src.routers.v1.users import router as router_users_version_1
from src.routers.v1.auth import router as router_auth_version_1

tags_metadata = [
    {"name": "Users",
     "description": "Operations with users.",
     },
    {"name": "Auth",
     "description": "The **login** ",
     },
    {"name": "Invoices",
     "description": "Manage Invoices. ",
     },
]

app = FastAPI(title="ExFastAPI",
              version="0.1.1",
              contact={"name": "Perfecto Vidal LLoret",
                       "email": "perfecto.vidal.lloret@gmail.com",
                       },
              license_info={"name": "Apache 2.0",
                            "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
                            },
              openapi_tags=tags_metadata
              )

routers = [router_auth_version_1,
           router_users_version_1,
           router_invoices_version_1,
           ]

for router in routers:
    app.include_router(router)
