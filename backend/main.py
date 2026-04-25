from fastapi import FastAPI
from routes.audit import router as audit_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "*",  # Allow all during development
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # or ["*"] for testing
    allow_credentials=True,
    allow_methods=["*"],          # allow all HTTP methods
    allow_headers=["*"],          # allow all headers
)

app.include_router(audit_router, prefix="/api")

@app.get("/")
def root():
    return {"message": "AI Expense Auditor API is running"}