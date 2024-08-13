from abc import ABC, abstractmethod


class NewsParse(ABC):

    @abstractmethod
    def load_articles(self):
        pass
