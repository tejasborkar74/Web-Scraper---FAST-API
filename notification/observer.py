from typing import List, Dict
from logging import Logger

class Observer:
    def __init__(self):
        self.recipients: List[str] = []
        
    def add_recipient(self, recipient: str):
        self.recipients.append(recipient)
        
    def notify(self, content: Dict, logger: Logger):
        raise NotImplementedError("Subclasses must implement the 'update' method.")


class SlackNotifier(Observer):
    def notify(self, content: Dict, logger: Logger):
        for recipient in self.recipients:
            logger.info(f"Slack Notification sent to {recipient}: {content}")


class EmailNotifier(Observer):
    def notify(self, content: Dict, logger: Logger):
        for recipient in self.recipients:
            logger.info(f"Email Notification sent to {recipient}: {content}")