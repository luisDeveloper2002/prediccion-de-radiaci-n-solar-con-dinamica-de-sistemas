from intefaces import IPresenter, IModel, IView

class Presenter(IPresenter):
    def __init__(self, model: IModel, view: IView):
        self.model: IModel = model
        self.view: IView = view
        self.model.set_presenter(self)
        self.view.set_presenter(self)

    def start_simulation(self, days:int):
        self.model.start_simulation(days)

    def show_results(self, result):
        self.view.show_results(result)
    
    def get_comparison_data(self, x: list[int], y1: list[float], y2: list[float], max_x_len = 35
                            ) -> tuple[list[int], list[float], list[float], str]:
        return self.model.get_comparison_data(x, y1, y2, max_x_len=max_x_len)