from abc import ABC, abstractmethod


class ScraperInterface(ABC):

    @abstractmethod
    def extract_results(self, search_term: str, results: list, lock, stop_event, condition: str = "used"):
        pass

