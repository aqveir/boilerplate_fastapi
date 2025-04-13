from modules.base.events.base import BaseEvent

class LoginEvent(BaseEvent):
    """
    Event triggered when a user logs in.
    """

    event_name: str = "login_event"

    # def __init__(self):
    #     super().__init__()

    # @staticmethod
    # def register(func):
    #     return super().register(func)

    # @staticmethod
    # def raise_event(data: dict):
    #     """
    #     Raises the login event.

    #     Args:
    #         data (dict): The data associated with the event.
    #     """
    #     return super().post_event(data)