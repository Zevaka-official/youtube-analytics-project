from googleapiclient.discovery import build
import os


class ApiItem:
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)
    base_url_h1 = r'https://youtu.be'
    base_url_h2 = r'https://www.youtube.com'

    @classmethod
    def get_service(cls):
        return cls.youtube

    def __init__(self):
        self.__api_object_raw_info = {}
        self.__api_request = {}

    def _set_request_obj(self, part, request_obj):
        self.__api_request[part] = request_obj

    def _update_api_object_info(self, part):
        """ force update api object info """
        api_request = self.__api_request.get(part, None)
        if api_request is None:
            raise NotImplementedError("Wrong API object implementation: request object is not changed")
        self.__api_object_raw_info[part] = api_request.execute()
        return self.__api_object_raw_info[part]

    def _api_object_info_raw(self, part):
        """ full response json """
        raw_info = self.__api_object_raw_info.get(part, None)
        if raw_info is None:
            raw_info = self._update_api_object_info(part)
        return raw_info
