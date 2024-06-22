from abc import ABC, abstractmethod

class Server(ABC):
    def __init__(self, url, api_key):
        self.url = url
        self.api_key = api_key

    @abstractmethod
    def create_backup(self):
        raise NotImplementedError

    # @abstractmethod
    # def restore_backup(self):
    #     raise NotImplementedError