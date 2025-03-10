"""
Problem Statement:
Designing a notification system that sends notification to different channels, and channel will have different types like SMS, email, push notification.

Requirements:
1. Notification will have a title and content.
2. Notification service will send notification to different channels.
3. Notification service will have a list of channels.
4. Notification service will send notification to all channels by default, but user can specify which channels to send.
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Dict

# Enum for notification status
class NotificationStatus(Enum):
    SUCCESS = 1
    FAILED = 0

# User class
class User:
    def __init__(self, id, name, email=None, phone=None, device_token=None, allowed_channels=None):
        self.id = id
        self.name = name
        self.email = email
        self.phone = phone
        self.device_token = device_token # this is the unique identifier for each device
        self.allowed_channels = allowed_channels # this is the list of channels that the user is allowed to receive notifications

    def add_channel(self, channel):
        if channel not in self.allowed_channels:
            self.allowed_channels.append(channel)

# Notification class that contains the title and content
class Notification:
    def __init__(self, title, content):
        self.title = title
        self.content = content

# Abstract class for notification channels
class NotificationChannel(ABC):
    @abstractmethod
    def send(self, user, notification) -> NotificationStatus:
        pass

class EmailChannel(NotificationChannel):
    def send(self, user, notification) -> NotificationStatus:
        if not user.email:
            return NotificationStatus.FAILED
        
        return NotificationStatus.SUCCESS

class SMSChannel(NotificationChannel):
    def send(self, user, notification) -> NotificationStatus:
        if not user.phone:
            return NotificationStatus.FAILED
        
        return NotificationStatus.SUCCESS

class PushNotificationChannel(NotificationChannel):
    def send(self, user, notification) -> NotificationStatus:
        if not user.device_token:
            return NotificationStatus.FAILED
        
        return NotificationStatus.SUCCESS

# Notification service that handles the notification channels
class NotificationService:
    def __init__(self):
        self.channels = []

    def add_channel(self, channel):
        pass

    def send_notification(self, user, notification) -> NotificationStatus:
        results = {} # channel -> status
        for channel in user.allowed_channels:
            status = channel.send(user, notification)
            results[channel] = status
        return results

        