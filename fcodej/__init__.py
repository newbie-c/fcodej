import os

import jinja2
import typing

from redis import asyncio as aioredis
from starlette.applications import Starlette
from starlette.config import Config
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from webassets import Environment as AssetsEnvironment
from webassets.ext.jinja2 import assets

from .api.auth import (
    CreatePassword, GetPassword, Login, Logout, ResetPassword)
from .api.main import Captcha, IndexPage
from .ava.views import show_avatar
from .auth.attri import groups, permissions
from .captcha.views import show_captcha
from .main.views import show_index, show_favicon

base = os.path.dirname(__file__)
static = os.path.join(base, 'static')
templates = os.path.join(base, 'templates')
settings = Config(os.path.join(os.path.dirname(base), '.env'))

try:
    from .addenv import SITE_NAME, SITE_DESCRIPTION, MAIL_PASSWORD
    if SITE_NAME:
        settings.file_values["SITE_NAME"] = SITE_NAME
    if SITE_DESCRIPTION:
        settings.file_values["SITE_DESCRIPTION"] = SITE_DESCRIPTION
    if MAIL_PASSWORD:
        settings.file_values["MAIL_PASSWORD"] = MAIL_PASSWORD
except ModuleNotFoundError:
    pass


class J2Templates(Jinja2Templates):
    def _create_env(self, directory: str) -> "jinja2.Environment":
        @jinja2.pass_context
        def url_for(
                context: dict, name: str, **path_params: typing.Any) -> str:
            request = context["request"]
            return request.url_for(name, **path_params)

        loader = jinja2.FileSystemLoader(directory)
        assets_env = AssetsEnvironment(static, '/static')
        assets_env.debug = settings.get('ASSETS_DEBUG', bool)
        env = jinja2.Environment(
            loader=loader, autoescape=True, extensions=[assets])
        env.assets_environment = assets_env
        env.globals["url_for"] = url_for
        env.globals["permissions"] = permissions
        env.globals["groups"] = groups
        return env

middleware = [
    Middleware(
        SessionMiddleware,
        secret_key=settings.get('SECRET_KEY'),
        max_age=settings.get('SESSION_LIFETIME', cast=int))]

app = Starlette(
    debug=settings.get('DEBUG', cast=bool),
    routes=[Route('/', show_index, name='index'),
            Route('/favicon.ico', show_favicon, name='favicon'),
            Mount('/api', name='api', routes=[
                Route('/index', IndexPage, name='aindex'),
                Route('/captcha', Captcha, name='acaptcha'),
                Route('/login', Login, name='alogin'),
                Route('/logout', Logout, name='alogout'),
                Route('/get-password', GetPassword, name='areg'),
                Route('/create-password', CreatePassword, name='crp'),
                Route('/reset-password', ResetPassword, name='rsp')]),
            Mount('/ava', name='ava', routes=[
                Route('/{hash}/{size:int}', show_avatar, name='avatar')]),
            Mount('/captcha', name='captcha', routes=[
                Route('/{suffix}', show_captcha, name='captcha')]),
            Mount('/static',
                  app=StaticFiles(directory=static), name='static')],
    middleware=middleware)
app.config = settings
app.jinja = J2Templates(directory=templates)
app.rc = aioredis.from_url(settings.get('REDI'), decode_responses=True)
