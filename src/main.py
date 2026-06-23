from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional

from fastapi import FastAPI

from src.core.config import settings
from src.services.prompts import PromptRegistryService

prompt_registry = PromptRegistryService()
app: Optional[FastAPI] = None


@asynccontextmanager
async def lifespan(app_instance: FastAPI) -> AsyncGenerator[None, None]:
    prompt_registry.load_all_prompts()
    yield


if settings.HTTP_MODE:
    app = FastAPI(
        title=settings.app.name,
        lifespan=lifespan,
    )
else:
    prompt_registry.load_all_prompts()
