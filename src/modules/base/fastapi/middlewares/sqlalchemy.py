""" Import the required modules """
from uuid import uuid4

from starlette.types import ASGIApp, Receive, Scope, Send

from modules.base.db.session import set_session_context, reset_session_context, session


class SQLAlchemyMiddleware:
    """ SQL Alchemy Middleware """
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        session_id = str(uuid4())
        context = set_session_context(session_id=session_id)

        try:
            await self.app(scope, receive, send)
        except Exception as e:
            raise e
        finally:
            await session.remove()
            reset_session_context(context=context)
