from functools import partial
from collections.abc import Callable

class EventEmitter:
    def __init__(self):
        self.__events = {}

    def __getitem__(self, key):
        item = None
        if isinstance(key, str):
            if key in self.__events:
                item = self.__events[key]
            else:
                raise EventEmitterError(f"{key} does not exist.")
        else:
            raise EventEmitterError(f"{key} must be a string.")

        return item

    def __dict__(self):
        return self.__events
    
    def on(self, event: str, fn: Callable, *args):
        if not fn:
            EventEmitterError.MissingArgument("fn")

        if not event:
            raise EventEmitterError.MissingArgument("event")

        if not event in self.__events:
            self.__events[event] = []
        
        self.__events[event].insert(len(self.__events[event]), partial(fn, *args))

        return self

    def off(self, event: str, fn_pointer: Callable):
        if not fn_pointer:
            EventEmitterError.MissingArgument("fn")
        
        if not event:
            raise EventEmitterError.MissingArgument("event")
        
        if not event in self.__events:
            raise EventEmitterError.EventNotFound(event)

        if not fn_pointer in self.__events[event]:
            raise EventEmitterError(f"{fn_pointer} is not subscribed to {event}")
        
        self.__events[event].remove(fn_pointer)

        return self

    def clear(self):
        self.__events = {}

    def emit(self, event: str, *payload):
        if not event:
            raise EventEmitterError.MissingArgument("event")

        if not self[event]:
            raise EventEmitterError.EventNotFound(event)
        
        for fn in self[event]:
            fn(*payload)

class EventEmitterError(Exception):
    def __init__(self, *args):
        self.message = args[0] if args else None

    def __str__(self):
        return f"LISTENER ERROR: {self.message}" if self.message else f"LISTENER ERROR has been raised!"

    @classmethod
    def MissingArgument(self, arg: str):
        return self(f"{arg.capitalize()} argument is missing.");

    @classmethod
    def NotAFunction(self, fn):
        return self(f"{fn} is not a function.")

    @classmethod
    def EventNotFound(self, event: str):
        return self(f"{event.capitalize()} does not exist.")