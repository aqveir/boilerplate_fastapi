""" Import the required modules """
from modules.base.events.base import BaseEvent

class OrganizationCreateEvent(BaseEvent):
    """ Create event """

    event_name: str = "organization_create_event"

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


class OrganizationUpdateEvent(BaseEvent):
    """ Update event """

    event_name: str = "organization_update_event"

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


class OrganizationDeleteEvent(BaseEvent):
    """ Delete event """

    event_name: str = "organization_delete_event"

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