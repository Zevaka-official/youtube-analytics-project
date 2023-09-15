from src.api_item import ApiItem
import isodate
from datetime import timedelta


class Video(ApiItem):
    video_url = ApiItem.base_url_h1

    _PART_VIDEO_INFO = "Video"

    def __init__(self, id: str) -> None:
        super().__init__()
        self._id = id
        try:
            self._video = Video.youtube.videos().list(id=self._id, part='snippet,statistics,contentDetails').execute()
        except Exception as e:
            self._video = None

    def __str__(self):
        return self.title if self.title else "None"

    @property
    def title(self):
        if self._video and self._video['items']:
            return self._video['items'][0]['snippet']['title']
        else:
            return None

    @property
    def view_count(self):
        if self._video and self._video['items']:
            return int(self._video['items'][0]['statistics']['viewCount'])
        else:
            return None

    @property
    def like_count(self):
        if self._video and self._video['items']:
            return int(self._video['items'][0]['statistics']['likeCount'])
        else:
            return None

    @property
    def video_id(self):
        return self._id

    @property
    def url(self):
        return f'{Video.video_url}/{self._id}' if self._video else None

    @property
    def video_duration(self) -> timedelta:
        if self._video and self._video['items']:
            duration_iso_str = self._video_info["contentDetails"]["duration"]
            return isodate.parse_duration(duration_iso_str)
        else:
            return None


class PLVideo(Video):
    _PART_PLVIDEO_INFO = "PlaylistItem"

    def __init__(self, id: str, playlist_id: str, check_playlist_item=True) -> None:
        super().__init__(id)
        self._playlist_id = playlist_id
        try:
            self._playlist_video = PLVideo.youtube.playlistItems().list(playlistId=playlist_id,
                                                                        part='contentDetails',
                                                                        maxResults=50,
                                                                        videoId=self._id
                                                                        ).execute()
        except Exception as e:
            self._playlist_video = None

        if check_playlist_item and not self.playlist_item_info:
            raise Exception("Такого видео нет в плейлисте.")

    @property
    def playlist_id(self):
        return self._playlist_id

    @property
    def playlist_item_info(self):
        """ информация о плейлисте """
        if not self._playlist_video:
            return None
        items = self._api_object_info_raw(PLVideo._PART_PLVIDEO_INFO)["items"]
        if len(items) == 0:
            return None
        return items[0]
