from src.api_item import ApiItem


class Video(ApiItem):
    def __init__(self, id: str) -> None:
        self._id = id
        self._video = Video.youtube.videos().list(id=self._id, part='snippet,statistics').execute()

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
        return f'https://youtu.be/{self._id}'


class PLVideo(Video):
    def __init__(self, id: str, playlist_id: str) -> None:
        super().__init__(id)
        self._playlist_id = playlist_id
        self._playlist_video = PLVideo.youtube.playlistItems().list(playlistId=playlist_id,
                                                                    part='contentDetails',
                                                                    maxResults=50,
                                                                    videoId=self._id
                                                                    ).execute()
        if not self._playlist_video['items']:
            raise Exception("Такого видео нет в плейлисте.")

    @property
    def playlist_id(self):
        return self._playlist_id

