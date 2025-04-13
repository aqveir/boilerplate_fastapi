from typing import Callable


class BaseEvent:
    event_name: str = "unique_event_name"

    def __init__(self):
        self.subscribers = dict()

    def register(self, func: Callable):
        if not self.event_name in self.subscribers:
            self.subscribers[self.event_name] = []

        print(f"Registering {func.__name__} for event {self.event_name}")
        self.subscribers[self.event_name].append(func)


    def unregister(self):
        if self.event_name in self.subscribers:
            self.subscribers.remove(self.event_name)
        

    def raise_event(self, data):
        if not self.event_name in self.subscribers:
            print(f"No subscribers for Event: {self.event_name}")
            return
        for func in self.subscribers[self.event_name]:
            print(f"Raising event {self.event_name} for {func.__name__}")
            func(data)

    # def notify_observers(self, message):
    #     for observer in self.observers:
    #         observer.update(message)