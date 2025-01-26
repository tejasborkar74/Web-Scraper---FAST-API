from typing import List, Dict
from logging import Logger
from notification.observer import Observer

class NotificationService:
    def __init__(self):
        self._observers: List[Observer] = []

    def subscribe(self, observer: Observer):
        self._observers.append(observer)

    def unsubscribe(self, observer: Observer):
        self._observers.remove(observer)

    def notify(self, content: Dict, logger: Logger):
        for observer in self._observers:
            observer.notify(content, logger)
