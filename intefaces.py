from abc import ABC, abstractmethod

class IModel(ABC):
    @abstractmethod
    def set_presenter(self, presenter):
        pass

    @abstractmethod
    def start_simulation(self, days:int):
        pass

    @abstractmethod
    def get_comparison_data(self, x: list[int], y1: list[float], y2: list[float], max_x_len = 35
                            ) -> tuple[list[int], list[float], list[float], str]:
        pass

class IView(ABC):
    @abstractmethod
    def set_presenter(self, presenter):
        pass

    @abstractmethod
    def show_results(self, result):
        pass

class IPresenter(ABC):
    @abstractmethod
    def start_simulation(self, days:int):
        pass

    @abstractmethod
    def show_results(self, result):
        pass
    
    @abstractmethod
    def get_comparison_data(self, x: list[int], y1: list[float], y2: list[float], max_x_len = 35
                            ) -> tuple[list[int], list[float], list[float], str]:
        pass