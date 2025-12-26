from fastapi import FastAPI
from .routers import threads, messages, alerts, channels, webhooks

app = FastAPI(title="ERP Procurement Communication Module", version="1.0.0")

app.include_router(threads.router, prefix="/threads", tags=["Threads"])
app.include_router(messages.router, prefix="/messages", tags=["Messages"])
app.include_router(alerts.router,   prefix="/alerts",   tags=["Alerts"])
app.include_router(channels.router, prefix="/channels", tags=["Channels"])
app.include_router(webhooks.router, prefix="/webhooks", tags=["Webhooks"])
