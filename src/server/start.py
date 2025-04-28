import logging

from fastapi import FastAPI
from contextlib import asynccontextmanager

# Import the middlewares
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

# Import the application module routes
from modules.auth.routes.route import router as auth_router
from modules.base.models.response import JsonSuccessResponse
from modules.user.routes.route import router as user_router

# Import the project exception handler
from modules.base.exceptions.base import *
from modules.base.exceptions.handler import custom_exception_handler

# Import the project event handlers
# from modules.user.listeners.user_listener import setup_log_event_handlers

# Import the project configuration
from modules.base.config import config


# Setup loggers
# https://docs.python.org/3/library/logging.config.html#logging.config.fileConfig
logging.config.fileConfig('config/logging.conf', disable_existing_loggers=False)

# Get root logger
logger = logging.getLogger(__name__)  # the __name__ resolve to "main" since we are at the root of the project. 
                                      # This will get the root logger since no logger in the configuration has this name.


# Lifespan Event Handler
@asynccontextmanager
async def lifespan(app: FastAPI):
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
    lifespan=lifespan,
    default_response_class=JsonSuccessResponse,
    swagger_ui_parameters={
        "syntaxHighlight": {"theme": "obsidian"}
    }
)


# Create an instance of the OAuth2PasswordBearer class
#oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


""" CORS Middleware

CORS (Cross-Origin Resource Sharing) is a security feature
implemented in web browsers to restrict JavaScript code.

The origins variable contains the list of origins that are
allowed to access the API. This is used to restrict the
access to the API to only the specified origins.
"""
origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


""" Trusted Host Middleware

The TrustedHostMiddleware is used to restrict the access to the
API to only the specified origins. The origins variable contains
the list of origins that are allowed to access the API.

A list of domain names that should be allowed as hostnames. Wildcard 
domains such as *.example.com are supported for matching subdomains. 
To allow any hostname either use allowed_hosts=["*"] or omit the 
middleware.
"""
allowed_hosts: list[str] = config.ALLOWED_DOMAINS

app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=allowed_hosts
)


""" Add Routers
This is used to add the routers to the application. This will 
make the routes available in the app.

The include_router function takes the router as an argument 
and adds the routes to the app.
"""
app.include_router(auth_router)
app.include_router(user_router)


""" Add Exception Handlers

This is used to handle the exceptions raised in the application.
"""
app.add_exception_handler(
    exc_class_or_status_code=BadRequestException,
    handler=custom_exception_handler(),
)
app.add_exception_handler(
    exc_class_or_status_code=DuplicateValueException,
    handler=custom_exception_handler(),
)
app.add_exception_handler(
    exc_class_or_status_code=EntityNotFoundException,
    handler=custom_exception_handler(),
)
app.add_exception_handler(
    exc_class_or_status_code=AuthenticationException,
    handler=custom_exception_handler(),
)
app.add_exception_handler(
    exc_class_or_status_code=InvalidTokenException,
    handler=custom_exception_handler(),
)
app.add_exception_handler(
    exc_class_or_status_code=ForbiddenException,
    handler=custom_exception_handler(),
)
app.add_exception_handler(
    exc_class_or_status_code=UnauthorizedException,
    handler=custom_exception_handler(),
)


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/health", status_code=200)
def health():
    """Api health endpoint."""
    return {"Api is up and running"}
