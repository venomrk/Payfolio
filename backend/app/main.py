from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.routers import auth, users, accounts, transactions, assets, liabilities, insights, billing

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Unified Financial Operating System API",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://payfolio.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Routers
app.include_router(auth.router, prefix="/v1/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/v1/users", tags=["Users"])
app.include_router(accounts.router, prefix="/v1/accounts", tags=["Accounts"])
app.include_router(transactions.router, prefix="/v1/transactions", tags=["Transactions"])
app.include_router(assets.router, prefix="/v1/assets", tags=["Assets"])
app.include_router(liabilities.router, prefix="/v1/liabilities", tags=["Liabilities"])
app.include_router(insights.router, prefix="/v1/insights", tags=["Insights"])
app.include_router(billing.router, prefix="/v1/billing", tags=["Billing"])


@app.get("/")
async def root():
    return {"message": "Payfolio API", "version": settings.APP_VERSION}


@app.get("/health")
async def health():
    return {"status": "healthy"}
