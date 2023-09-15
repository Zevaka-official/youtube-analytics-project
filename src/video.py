from src.api_item import ApiItem
import isodate
from datetime import timedelta


class Video(ApiItem):
    video_url = ApiItem.base_url_h1

    _PART_VIDEO_INFO = "Video"

    def __init__(self, id: str) -> None:
        super().__init__()
        self._id = id
        self._video = Video.youtube.videos().list(id=self._id, part='snippet,statistics,contentDetails').execute()

    def __str__(self):
        return self.title

    @property
    def title(self):
        return self._video['items'][0]['snippet']['title']

    @property
    def view_count(self):
        return int(self._video['items'][0]['statistics']['viewCount'])

    @property
    def video_likes(self):
        return int(self._video['items'][0]['statistics']['likeCount'])

    @property
    def video_id(self):
        return self._id

    @property
    def url(self):
        return f'{Video.video_url}/{self._id}'

    @property
    def video_duration(self) -> timedelta:
        duration_iso_str = self._video_info["contentDetails"]["duration"]
        return isodate.parse_duration(duration_iso_str)


class PLVideo(Video):
    _PART_PLVIDEO_INFO = "PlaylistItem"

    def __init__(self, id: str, playlist_id: str, check_playlist_item=True) -> None:
        super().__init__(id)
        self._playlist_id = playlist_id
        self._playlist_video = PLVideo.youtube.playlistItems().list(playlistId=playlist_id,
                                                                    part='contentDetails',
                                                                    maxResults=50,
                                                                    videoId=self._id
                                                                    ).execute()

        if check_playlist_item:
            playlist_info = self.playlist_item_info
            if not playlist_info:
                raise Exception("Такого видео нет в плейлисте.")

    @property
    def playlist_id(self):
        return self._playlist_id

    @property
    def playlist_item_info(self):
        """ информация о плейлисте """
        items = self._api_object_info_raw(PLVideo._PART_PLVIDEO_INFO)["items"]
        if len(items) == 0:
            return None
        return items[0]
