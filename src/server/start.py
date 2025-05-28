""" Import the required modules """
import logging

from contextlib import asynccontextmanager
from typing import List
from fastapi import FastAPI

# Import the middlewares
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

# Import the application module routes
from modules.base.models.response import JsonSuccessResponse
from modules.auth.routes.route import router as auth_router
from modules.core.routes.organization_router import router as organization_router
from modules.core.routes.lookup_router import router as lookup_router
from modules.user.routes.route import router as user_router
from modules.base.fastapi.middlewares import SQLAlchemyMiddleware

# Import the project exception handler
from modules.base.exceptions import (
    BadRequestException,
    DuplicateValueException,
    EntityNotFoundException,
    AuthenticationException,
    InvalidTokenException,
    ForbiddenException,
    UnauthorizedException,
    NotFoundException,
    InternalServerErrorException,
    AWSValueException
)
from modules.base.exceptions.handler import custom_exception_handler

# Import the project event handlers
# from modules.user.listeners.user_listener import setup_log_event_handlers

# Import the project configuration
from modules.base.config import config


# Setup loggers
# https://docs.python.org/3/library/logging.config.html#logging.config.fileConfig
logging.config.fileConfig('config/logging.conf', disable_existing_loggers=False)

# Get root logger
# the __name__ resolve to "main" since we are at the root of the project.
# This will get the root logger since no logger in the configuration has
# this name.
logger = logging.getLogger(__name__)


# Make Middlewares
def make_middleware() -> List[Middleware]:
    """ Add Middlewares """

    return [
        Middleware(
            # CORS Middleware

            # CORS (Cross-Origin Resource Sharing) is a security feature
            # implemented in web browsers to restrict JavaScript code.

            # The origins variable contains the list of origins that are
            # allowed to access the API. This is used to restrict the
            # access to the API to only the specified origins.         
            CORSMiddleware,
            allow_origins=[
                "http://localhost",
                "http://localhost:8080",
            ],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
        Middleware(
            # Trusted Host Middleware

            # The TrustedHostMiddleware is used to restrict the access
            # to the API to only the specified origins. The origins
            # variable contains the list of origins that are allowed to
            # access the API.

            # A list of domain names that should be allowed as hostnames.
            # Wildcard domains such as *.example.com are supported for
            # matching subdomains. To allow any hostname either use
            # allowed_hosts=["*"] or omit the middleware.
            TrustedHostMiddleware,
            allowed_hosts=config.ALLOWED_DOMAINS
        ),
        # Middleware(
        #     AuthenticationMiddleware,
        #     backend=AuthBackend(),
        #     on_error=on_auth_error,
        # ),
        Middleware(SQLAlchemyMiddleware),
        # Middleware(ResponseLoggerMiddleware),
    ]


# Add Routers
def init_routers(_app: FastAPI) -> None:
    """ Initialize the routers for the FastAPI app.

    This is used to add the routers to the application. This will
    make the routes available in the app.

    The include_router function takes the router as an argument and 
    adds the routes to the app.
    """
    _app.include_router(auth_router)
    _app.include_router(organization_router)
    _app.include_router(lookup_router)
    _app.include_router(user_router)


def init_handlers(_app: FastAPI) -> None:
    """ Initialize Handlers """
    _app.add_exception_handler(
        exc_class_or_status_code=BadRequestException,
        handler=custom_exception_handler(),
    )
    _app.add_exception_handler(
        exc_class_or_status_code=DuplicateValueException,
        handler=custom_exception_handler(),
    )
    _app.add_exception_handler(
        exc_class_or_status_code=EntityNotFoundException,
        handler=custom_exception_handler(),
    )
    _app.add_exception_handler(
        exc_class_or_status_code=AuthenticationException,
        handler=custom_exception_handler(),
    )
    _app.add_exception_handler(
        exc_class_or_status_code=InvalidTokenException,
        handler=custom_exception_handler(),
    )
    _app.add_exception_handler(
        exc_class_or_status_code=ForbiddenException,
        handler=custom_exception_handler(),
    )
    _app.add_exception_handler(
        exc_class_or_status_code=UnauthorizedException,
        handler=custom_exception_handler(),
    )
    _app.add_exception_handler(
        exc_class_or_status_code=NotFoundException,
        handler=custom_exception_handler(),
    )
    _app.add_exception_handler(
        exc_class_or_status_code=InternalServerErrorException,
        handler=custom_exception_handler(),
    )
    _app.add_exception_handler(
        exc_class_or_status_code=AWSValueException,
        handler=custom_exception_handler(),
    )


# Lifespan Event Handler
@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Lifespan event handler for the FastAPI app.

    This function is called when the app starts and stops.
    It is used to set up and tear down resources that are needed
    for the app to run.
    """
    # Setup log event handlers
    # setup_log_event_handlers()
    try:
        # Starting the server
        logger.info("********** Starting the server **********")

        # Initialize routers
        init_routers(_app=_app)

        # Initilize Exception Handlers
        # init_handlers(_app=_app)

        yield
    finally:
        # Stopping the server
        logger.info("********** Stopping the server **********")

        # Cleanup log event handlers
        # cleanup_log_event_handlers()

        # Cleanup resources here if needed
        logger.info("********** Server Stopped **********")


# Create an instance of the FastAPI class
app = FastAPI(
    title=config.APP_NAME,
    description=config.APP_DESCRIPTION,
    version=config.APP_VERSION,
    debug=config.DEBUG,
    docs_url=None if config.ENVIRONMENT == "production" else "/docs",
    redoc_url=None if config.ENVIRONMENT == "production" else "/redoc",
    lifespan=lifespan,
    middleware=make_middleware(),
    default_response_class=JsonSuccessResponse,
    swagger_ui_parameters={
        "syntaxHighlight": {"theme": "obsidian"}
    },
)


# Create an instance of the OAuth2PasswordBearer class
#oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

""" Add Exception Handlers

This is used to handle the exceptions raised in the application.
"""
init_handlers(app)

@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Hello World"}

@app.get("/health", status_code=200)
def health():
    """Api health endpoint."""
    return {"Api is up and running"}
