from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from app.database import engine, Base
from app.routers import auth, customers, opportunities, activities, ai_agent, leads, products

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Hosho CRM")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
async def serve_register(): return FileResponse(os.path.join(static_dir, "pages/register.html"))
@app.get("/login")
async def serve_login(): return FileResponse(os.path.join(static_dir, "index.html"))
@app.get("/dashboard")
async def serve_dashboard(): return FileResponse(os.path.join(static_dir, "pages/dashboard.html"))

app.include_router(auth.router, prefix="/api/v1/auth")
app.include_router(customers.router, prefix="/api/v1/customers")
app.include_router(opportunities.router, prefix="/api/v1/opportunities")
app.include_router(activities.router, prefix="/api/v1/activities")
app.include_router(ai_agent.router, prefix="/api/v1/ai")
app.include_router(leads.router, prefix="/api/v1/leads")
app.include_router(products.router, prefix="/api/v1/products")
