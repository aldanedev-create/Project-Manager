"""Compose the CLI starter's modules, staff backoffice, and Teloce SPA."""

import settings
from types import SimpleNamespace
from pathlib import Path
from urllib.parse import urlsplit
from flaxon.middleware import BodyLimitMiddleware, TrustedHostsMiddleware
from flaxon import Flaxon, Request
from flaxon.http import JSONResponse
from modules.welcome.module import welcome
from settings import (
    ROOT,
    DATA_DIR,
    DATABASE_PATH,
    ADMIN_DATABASE_PATH,
    DEBUG,
    PUBLIC_ORIGIN,
)


def create_app(database_path=None, admin_path=None, debug=None):
    debug = DEBUG if debug is None else debug
    values = {key: getattr(settings, key) for key in dir(settings) if key.isupper()}
    values.update(DEBUG=debug)
    if database_path is not None:
        values["DATABASE_URL"] = f"sqlite://{Path(database_path).resolve()}"
    if admin_path is not None:
        values["ADMIN_STORAGE_PATH"] = Path(admin_path)
    app = Flaxon.from_settings(SimpleNamespace(__file__=settings.__file__, **values))
    app.add_middleware(BodyLimitMiddleware, max_size=256 * 1024)
    if not debug:
        app.add_middleware(
            TrustedHostsMiddleware, allowed_hosts=[urlsplit(PUBLIC_ORIGIN).hostname]
        )
    app.public_origin = PUBLIC_ORIGIN
    for module, prefix in [
        (welcome, "/api/welcome"),
    ]:
        app.mount_module(module, prefix=prefix)
    if app.is_management:
        return app


    @app.get("/health/course")
    async def health():
        from models import User
        await User.all().limit(1)
        return {"data": {"status": "ok"}}

    @app.get("/")
    async def home():
        return {"data": {"message": "Backend lesson ready. The SPA starts in chapter 8."}}

    return app


app = create_app()
