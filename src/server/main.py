import uvicorn

from fastapi import FastAPI

# Import the middlewares
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

# Import the application module routes
from modules.auth.routes.route import router as auth_router
from modules.user.routes.route import router as user_router

# Import the project exception handler
from modules.base.exceptions.base import *
from modules.base.exceptions.handler import custom_exception_handler

# Import the project event handlers
from modules.user.listeners.user_listener import setup_log_event_handlers


# Create an instance of the FastAPI class
app = FastAPI()


# Create an instance of the OAuth2PasswordBearer class
#oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


"""
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


"""
The TrustedHostMiddleware is used to restrict the access to the
API to only the specified origins. The origins variable contains
the list of origins that are allowed to access the API.

A list of domain names that should be allowed as hostnames. Wildcard 
domains such as *.example.com are supported for matching subdomains. 
To allow any hostname either use allowed_hosts=["*"] or omit the 
middleware.
"""
allowed_hosts = [
    "localhost",
    "aqveir.in",
    "*.aqveir.in",
]

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


# Add event handlers



@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/health", status_code=200)
def health():
    """Api health endpoint."""
    return {"Api is up and running"}

def start_server():
    # print('Starting Server...')       
    uvicorn.run(
        "server.main:app",
        host="0.0.0.0",
        port=8080,
        log_level="debug",
        reload=True
    )
    # webbrowser.open("http://127.0.0.1:8080")
    # uvicorn server.main:app --host 0.0.0.0 --port 8080

if __name__ == "__main__":
    start_server()