import json

from googleapiclient.discovery import build
import os
from src.utils import printj


class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.__channel = Channel.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""

        printj(self.__channel)

    @property
    def id(self):
        return self.__channel_id

    @property
    def title(self):
        return self.__channel["items"][0]["snippet"]["title"]

    @property
    def description(self):
        return self.__channel["items"][0]["snippet"]["description"]

    @property
    def url(self):
        return f'https://www.youtube.com/channel/{self.__channel_id}'

    @property
    def subscriber_count(self):
        return self.__channel["items"][0]["statistics"]["subscriberCount"]

    @property
    def video_count(self):
        return self.__channel["items"][0]["statistics"]["videoCount"]

    @property
    def view_count(self):
        return self.__channel["items"][0]["statistics"]["viewCount"]

    @classmethod
    def get_service(cls):
        return cls.youtube

    def to_json(self, filename):
        with open(filename, encoding='UTF-8', mode="w") as f:
            json.dump({"id": self.__channel_id,
                       "title": self.title,
                       "description": self.description,
                       "url": self.url,
                       "subscriber_count": self.subscriber_count,
                       "video_count": self.video_count,
                       "view_count": self.view_count}, f, ensure_ascii=False)
