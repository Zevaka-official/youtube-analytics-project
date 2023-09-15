import datetime

import isodate

from src.api_item import ApiItem


class PlayList(ApiItem):
    """ Класс для представления плейлиста. """

    def __init__(self, playlist_id: str) -> None:
        self.playlist_id: str = playlist_id

        self.json_: dict = self.get_youtube_json()
        self.title: str = self.json_['items'][0]['snippet']['title']
        self.url: str = f'https://www.youtube.com/playlist?list={self.playlist_id}'

    def get_youtube_json(self):
        """ Возвращает словарь с данными о плейлисте. """
        return self.youtube.playlists().list(part='snippet,contentDetails',
                                             id=self.playlist_id
                                             ).execute()

    def __video_response(self):
        """ Возвращает словарь с данными о видео в плейлисте. """
        # получить данные по play-листам канала
        playlist_videos = self.youtube.playlistItems().list(playlistId=self.playlist_id,
                                                            part='contentDetails',
                                                            maxResults=50
                                                            ).execute()

        # получить все id видеороликов из плейлиста
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]

        # вывести длительности видеороликов из плейлиста
        video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                    id=','.join(video_ids)
                                                    ).execute()
        return video_response

    @property
    def total_duration(self) -> datetime.timedelta:
        """ Возвращает объект класса `datetime.timedelta` с суммарной длительностью плейлиста. """
        video_response = self.__video_response()

        # получить статистику и просуммировать длительность видео
        total_duration = datetime.timedelta()

        for video in video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += duration

        return total_duration

    def show_best_video(self) -> str:
        """ Возвращает ссылку на самое популярное видео из плейлиста. """
        video_response = self.__video_response()

        best_video_id, id_video, count_like = '', None, float('-inf')
        for k in video_response['items']:
            id_video = k['id']
            for key, value in k['statistics'].items():
                if key == 'likeCount' and int(value) >= count_like:
                    best_video_id = id_video
        return 'https://youtu.be/{}'.format(best_video_id)
