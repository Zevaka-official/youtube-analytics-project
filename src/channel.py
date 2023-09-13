import json
from src.api_item import ApiItem
from src.utils import printj


class Channel(ApiItem):
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.__channel = Channel.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()

    def __str__(self):
        return f'{self.title} ({self.url})'

    def __add__(self, other):
        return self.subscriber_count + other.subscriber_count

    def __sub__(self, other):
        return self.subscriber_count - other.subscriber_count

    def __eq__(self, other):
        return self.subscriber_count == other.subscriber_count

    def __ne__(self, other):
        return self.subscriber_count != other.subscriber_count

    def __lt__(self, other):
        return self.subscriber_count < other.subscriber_count

    def __le__(self, other):
        return self.subscriber_count <= other.subscriber_count

    def __gt__(self, other):
        return self.subscriber_count > other.subscriber_count

    def __ge__(self, other):
        return self.subscriber_count >= other.subscriber_count

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
        return int(self.__channel["items"][0]["statistics"]["subscriberCount"])

    @property
    def video_count(self):
        return self.__channel["items"][0]["statistics"]["videoCount"]

    @property
    def view_count(self):
        return self.__channel["items"][0]["statistics"]["viewCount"]

    def to_json(self, filename):
        with open(filename, encoding='UTF-8', mode="w") as f:
            json.dump({"id": self.__channel_id,
                       "title": self.title,
                       "description": self.description,
                       "url": self.url,
                       "subscriber_count": self.subscriber_count,
                       "video_count": self.video_count,
                       "view_count": self.view_count}, f, ensure_ascii=False)
