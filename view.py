from intefaces import IView, IPresenter, IModel
from data_models import RadiationDayData, Result
from model import Model
from presenter import Presenter
import tkinter as tk
from tkinter import messagebox
import threading
import matplotlib.pyplot as plt
import time

class LoadingCircle:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.canvas = tk.Canvas(root, width=100, height=100)
        self.canvas.pack(expand=True, fill=tk.BOTH, pady=20)
        self.arc = None
        self.angle = 0
        self.canvas.bind("<Configure>", self.update_arc_position)
        self.animate()

    def update_arc_position(self, event=None):
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        size = 0.8 * min(canvas_width, canvas_height)
        x0 = (canvas_width - size) / 2
        y0 = (canvas_height - size) / 2
        x1 = x0 + size
        y1 = y0 + size
        if self.arc:
            self.canvas.delete(self.arc)
        self.arc = self.canvas.create_arc(
            x0, y0, x1, y1,
            start=self.angle,
            extent=210,
            style=tk.ARC,
            outline="#3498db",
            width=min(canvas_width, canvas_height)*0.1
        )

    def animate(self):
        self.angle = (self.angle + 10) % 360
        self.canvas.itemconfig(self.arc, start=self.angle)
        def update():
            if self.root.winfo_exists():
                try:
                    self.animate()
                except tk.TclError:
                    pass
        self.root.after(50, update)

class View(tk.Tk, IView):
    def __init__(self):
        super().__init__()
        self.presenter : IPresenter = None
        self.load_frame = None
        self.title("Aplicación")
        self.geometry("500x500")
        self.configure(bg="#f0f0f0")
        self.update_idletasks()
        self.geometry("+{}+{}".format(int(self.winfo_screenwidth()/2 - self.winfo_width()/2), int(self.winfo_screenheight()/2 - self.winfo_height()/2)))
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.label = tk.Label(self.main_frame, text="Simulador de radiacion solar")
        self.label.config(font=("Arial", 25))
        self.label.pack(pady=10)
        label_input = tk.Label(self.main_frame, text="Ingrese el numero de dias a simular:")
        label_input.config(font=("Arial", 15))
        label_input.pack(pady=10)
        input = tk.Entry(self.main_frame)
        input.pack(pady=10)
        def on_start():
            try:
                input_value = int(input.get())
                if input_value < 1:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Ingrese un numero valido de dias")
                return
            if input_value > 4059:
                messagebox.showerror("Error", "No se puede simular mas de 4059 dias")
                return
            self.show_load_frame()
            input.delete(0, tk.END)
            def func_thread():
                time.sleep(2)
                self.presenter.start_simulation(input_value)
            threading.Thread(target=func_thread, daemon=True).start()
        tk.Button(self.main_frame, text="Iniciar Simulación", command=on_start).pack(pady=10)

    def show_load_frame(self):
        if not self.load_frame:
            self.create_load_frame()
        else:
            self.load_frame.pack(fill=tk.BOTH, expand=True)
        self.main_frame.pack_forget()

    def create_load_frame(self):
        self.load_frame = tk.Frame(self)
        self.load_frame.pack(fill=tk.BOTH, expand=True)
        LoadingCircle(self.load_frame)
        self.load_label = tk.Label(self.load_frame, text="Cargando simulacion...")
        self.load_label.config(font=("Arial", 20))
        self.load_label.pack(fill=tk.X, expand=True)

    def set_presenter(self, presenter):
        self.presenter = presenter

    def show_results(self, result: Result):
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        self.geometry("{}x{}".format(width, height))
        self.update_idletasks()
        self.geometry("+{}+{}".format(int(self.winfo_screenwidth()/2 - self.winfo_width()/2), int(self.winfo_screenheight()/2 - self.winfo_height()/2)))
        results_frame = tk.Frame(self)
        title = tk.Label(results_frame, text="Resultados")
        title.config(font=("Arial", 25))
        title.pack(pady=30)
        initial_data_title = tk.Label(results_frame, text="Datos iniciales (t0):")
        initial_data_title.config(font=("Arial", 15))
        initial_data_title.pack(pady=10)
        initial_data_frame = tk.Frame(results_frame)
        initial_data_frame.pack(pady=10)
        initial_data_frame.columnconfigure(0, weight=1)
        initial_data_frame.columnconfigure(1, weight=1)
        initial_data_frame.columnconfigure(2, weight=1)
        initial_data_frame.columnconfigure(3, weight=1)
        initial_data_frame.columnconfigure(4, weight=1)
        initial_solar_light_label = tk.Label(initial_data_frame, text="Brillo solar (h)")
        initial_solar_light_label.config(font=("Arial", 12))
        initial_solar_light_label.grid(row=0, column=0, ipadx=10)
        initial_cloudiness_label = tk.Label(initial_data_frame, text="Nubosidad")
        initial_cloudiness_label.config(font=("Arial", 12))
        initial_cloudiness_label.grid(row=0, column=1, ipadx=10)
        initial_relative_humidity_label = tk.Label(initial_data_frame, text="Humedad relativa (%)")
        initial_relative_humidity_label.config(font=("Arial", 12))
        initial_relative_humidity_label.grid(row=0, column=2, ipadx=10)
        initial_rainfall_label = tk.Label(initial_data_frame, text="Precipitacion (mm)")
        initial_rainfall_label.config(font=("Arial", 12))
        initial_rainfall_label.grid(row=0, column=3, ipadx=10)
        initial_radiation_label = tk.Label(initial_data_frame, text="Radiacion (cal/cm2)")
        initial_radiation_label.config(font=("Arial", 12))
        initial_radiation_label.grid(row=0, column=4, ipadx=10)
        initial_solar_light_value = tk.Label(initial_data_frame, text=f"{result.initial_data.solar_light:.2f}")
        initial_solar_light_value.config(font=("Arial", 12))
        initial_solar_light_value.grid(row=1, column=0, ipadx=10)
        initial_cloudiness_value = tk.Label(initial_data_frame, text=f"{result.initial_data.cloudiness:.2f}")
        initial_cloudiness_value.config(font=("Arial", 12))
        initial_cloudiness_value.grid(row=1, column=1, ipadx=10)
        initial_relative_humidity_value = tk.Label(initial_data_frame, text=f"{result.initial_data.relative_humidity:.2f}")
        initial_relative_humidity_value.config(font=("Arial", 12))
        initial_relative_humidity_value.grid(row=1, column=2, ipadx=10)
        initial_rainfall_value = tk.Label(initial_data_frame, text=f"{result.initial_data.rainfall:.2f}")
        initial_rainfall_value.config(font=("Arial", 12))
        initial_rainfall_value.grid(row=1, column=3, ipadx=10)
        initial_radiation_value = tk.Label(initial_data_frame, text=f"{result.initial_data.radiation:.2f}")
        initial_radiation_value.config(font=("Arial", 12))
        initial_radiation_value.grid(row=1, column=4, ipadx=10)
        average_data_title = tk.Label(results_frame, text="Datos promedio:")
        average_data_title.config(font=("Arial", 15))
        average_data_title.pack(pady=10)
        average_data_frame = tk.Frame(results_frame)
        average_data_frame.pack(pady=10)
        average_data_frame.columnconfigure(0, weight=1)
        average_data_frame.columnconfigure(1, weight=1)
        average_data_frame.columnconfigure(2, weight=1)
        obtained_radiation_average_label = tk.Label(average_data_frame, text="Promedio de radiacion obtenida (cal/cm2)")
        obtained_radiation_average_label.config(font=("Arial", 12))
        obtained_radiation_average_label.grid(row=0, column=0, ipadx=10)
        predicted_radiation_average_label = tk.Label(average_data_frame, text="Promedio de radiacion real (cal/cm2)")
        predicted_radiation_average_label.config(font=("Arial", 12))
        predicted_radiation_average_label.grid(row=0, column=1, ipadx=10)
        error_label = tk.Label(average_data_frame, text="Error (%)")
        error_label.config(font=("Arial", 12))
        error_label.grid(row=0, column=2, ipadx=10)
        obtained_radiation_average_value = tk.Label(average_data_frame, text=f"{result.radiation_obtained_average:.2f}")
        obtained_radiation_average_value.config(font=("Arial", 12))
        obtained_radiation_average_value.grid(row=1, column=0, ipadx=10)
        predicted_radiation_average_value = tk.Label(average_data_frame, text=f"{result.radiation_predicted_average:.2f}")
        predicted_radiation_average_value.config(font=("Arial", 12))
        predicted_radiation_average_value.grid(row=1, column=1, ipadx=10)
        error_value = tk.Label(average_data_frame, text=f"{result.error:.2f} %")
        error_value.config(font=("Arial", 12))
        error_value.grid(row=1, column=2, ipadx=10)
        formulas_title = tk.Label(results_frame, text="Formulas:")
        formulas_title.config(font=("Arial", 15))
        formulas_title.pack(pady=10)
        radiation_formula_label = tk.Label(results_frame, text=result.radiation_formula)
        radiation_formula_label.config(font=("Arial", 12))
        radiation_formula_label.pack(pady=10)
        solar_light_formula_label = tk.Label(results_frame, text=result.solar_light_formula)
        solar_light_formula_label.config(font=("Arial", 12))
        solar_light_formula_label.pack(pady=10)
        cloudiness_formula_label = tk.Label(results_frame, text=result.cloudiness_formula)
        cloudiness_formula_label.config(font=("Arial", 12))
        cloudiness_formula_label.pack(pady=10)
        relative_humidity_formula_label = tk.Label(results_frame, text=result.relative_humidity_formula)
        relative_humidity_formula_label.config(font=("Arial", 12))
        relative_humidity_formula_label.pack(pady=10)
        x = [data.day for data in result.radiation_data_obtained]
        y1 = [data.radiation for data in result.radiation_data_predicted]
        y2 = [data.radiation for data in result.radiation_data_obtained]
        x_data, y1_data, y2_data, label1 = self.presenter.get_comparison_data(x, y1, y2)
        def on_show_comparison():
            self.show_comparison(x_data, y1_data, y2_data, 'Radiacion real', 'Radiacion obtenida', 
                                 'Comparacion de comportamiento de radiacion', label1, 'valor de radiacion (cal/cm2)')
        see_comparison_button = tk.Button(results_frame, text="Ver Comparacion", command=on_show_comparison)
        see_comparison_button.pack(pady=10)
        def on_back():
            self.reset_view(results_frame)
            results_frame.destroy()
        tk.Button(results_frame, text="Volver", command=on_back).pack(pady=10)
        self.load_frame.pack_forget()
        self.main_frame.pack_forget()
        results_frame.pack(fill=tk.BOTH, expand=True)

    def show_comparison(self, x, y1, y2, label1, label2, title, x_label, y_label):
        plt.figure(figsize=(13, 4))
        plt.step(x, y1, label=label1, color='blue', linestyle='--')
        plt.step(x, y2, label=label2, color='red', linestyle='--')
        plt.scatter(x, y1, color='blue')
        plt.scatter(x, y2, color='red')
        plt.xticks(ticks=x, labels=x)
        plt.legend()
        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.show()
    
    def reset_view(self, frame: tk.Frame):
        self.geometry("500x500")
        self.configure(bg="#f0f0f0")
        self.update_idletasks()
        self.geometry("+{}+{}".format(int(self.winfo_screenwidth()/2 - self.winfo_width()/2), int(self.winfo_screenheight()/2 - self.winfo_height()/2)))
        frame.pack_forget()
        self.main_frame.pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    model: IModel = Model()
    view: IView = View()
    presenter = Presenter(model, view)
    view.mainloop()