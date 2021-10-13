from functools import partial

class EventListener:
    def __init__(self):
        self.__events = {}

    def __getitem__(self, key):
        item = None
        if isinstance(key, str):
            if key in self.__events:
                item = self.__events[key]
            else:
                raise EventListenerError(f"{key} does not exist.")
        else:
            raise EventListenerError(f"{key} must be a string.")

        return item

    def __dict__(self):
        return self.__events
    
    def on(self, event: str, fn, *args):
        if not event:
            raise EventListenerError("Event argument cannot be empty.")

        if type(fn) != "function":
            raise EventListenerError(f"{fn} is not a function.")

        if not self[event]:
            self[event] = []
        
        self[event].insert(len(self[event]), partial(fn, *args))

        return self

    def off(self, event: str, fn_pointer):
        if not event:
            raise EventListenerError("Event argument cannot be empty.")

        if type(fn_pointer) != "function":
            raise EventListenerError(f"{fn_pointer} is not a function.")

        if not self[event]:
            raise EventListenerError(f"There is no event named {event}")

        if not fn_pointer in self.__events[event]:
            raise EventListenerError(f"{fn_pointer} is not subscibed to {event}")
        
        self[event].remove(fn_pointer)

        return self

    def clear(self):
        self.__events = {}

    def call(self, event: str):
        if not event:
            raise EventListenerError("Event argument cannot be empty.")

        if not self[event]:
            raise EventListenerError(f"There is no event named {event}")
        
        for fn in self[event]:
            fn()

class EventListenerError(Exception):
    def __init__(self, *args):
        self.message = args[0] if args else None

    def __str__(self):
        return f"LISTENER ERROR: {self.message}" if self.message else f"LISTENER ERROR has been raised!"