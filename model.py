from intefaces import IModel, IPresenter
from data_models import DistributionData, RadiationDayData, Result
from numbers_model import NumbersModel
from scipy.stats import norm
from sklearn.linear_model import LinearRegression
import re
import pandas as pd

class Model(IModel):
    def __init__(self):
        self.presenter: IPresenter = None
        self.numbers_model = NumbersModel()
        self.df = None
        self.total = 0
        self.models_df = None
        self.input_df = None
        self.radiation_model = None
        self.solar_light_model = None
        self.cloudiness_model = None
        self.relative_humidity_model = None
        self.min_rainfall = 0
        self.max_rainfall = 0
        self.distribution_info = { "radiation": DistributionData(10, 1), 
                                  "solar_light": DistributionData(10, 1), 
                                  "cloudiness": DistributionData(10, 1), 
                                  "relative_humidity": DistributionData(10, 1)}

    def set_presenter(self, presenter):
        self.presenter: IPresenter = presenter

    def __load_data(self):
        df = pd.read_csv('radiacion_depurada.csv', sep=';')
        self.df = df
        total_rows = len(df)
        amount_inputs = int(total_rows * 0.10) 

        choice_index = []
        while len(choice_index) <  amount_inputs:
          index = int(self.__get_pseudo_random_number() * total_rows)
          if index not in choice_index:
           choice_index.append(index)


        df_inputs = df.iloc[choice_index].reset_index(drop=True)
        df_modelos = df.drop(index=choice_index).reset_index(drop=True)

        self.input_df = df_inputs
        self.models_df = df_modelos
        self.__process_df()

    def __process_df(self):
        cols = [
            'RadiacionGlobal_(cal/cm2)',
            'Brillo_Solar_(h)',
            'Humedad_Relativa_(%)',
            'Precipitacion_(mm)',
            'Nubosidad'
        ]
        for col in cols:
            self.df[col] = self.df[col].apply(self.__clean_and_process)
        self.df = self.df.dropna(subset=cols).reset_index(drop=True)
        self.total = len(self.df)
        
    def __clean_and_process(self, text):
        text = str(text).replace(',', '.').strip()
        match = re.search(r'\d+\.\d+|\d+', text)
        return float(match.group()) if match else None

    def __generate_models(self):
        self.models_df['RadiacionGlobal_(cal/cm2)'] =  self.models_df['RadiacionGlobal_(cal/cm2)'].apply(self.__clean_and_process)
        self.models_df['Brillo_Solar_(h)'] =  self.models_df['Brillo_Solar_(h)'].apply(self.__clean_and_process)
        self.models_df['Humedad_Relativa_(%)'] =  self.models_df['Humedad_Relativa_(%)'].apply(self.__clean_and_process)
        self.models_df['Precipitacion_(mm)'] =  self.models_df['Precipitacion_(mm)'].apply(self.__clean_and_process)
        self.models_df['Nubosidad'] =  self.models_df['Nubosidad'].str.replace(',', '.').apply(self.__clean_and_process)
        self.models_df['Radiacion_t'] =  self.models_df['RadiacionGlobal_(cal/cm2)'].shift(1)
        self.models_df['Brillo_t'] =  self.models_df['Brillo_Solar_(h)'].shift(1)
        self.models_df['Humedad_t'] =  self.models_df['Humedad_Relativa_(%)'].shift(1)
        self.models_df['Precipitacion_t'] =  self.models_df['Precipitacion_(mm)'].shift(1)
        self.models_df['Nubosidad_t'] =  self.models_df['Nubosidad'].shift(1)
        self.models_df =  self.models_df.dropna()

        X_rad =  self.models_df[['Radiacion_t', 'Brillo_t','Precipitacion_t','Nubosidad_t']]
        y_rad =  self.models_df['RadiacionGlobal_(cal/cm2)']
        self.radiation_model = LinearRegression().fit(X_rad, y_rad)

        X_bril =  self.models_df[['Brillo_t','Precipitacion_t','Nubosidad_t']]
        y_bril =  self.models_df['Brillo_Solar_(h)']
        self.solar_light_model = LinearRegression().fit(X_bril, y_bril)

        X_nub =  self.models_df[['Nubosidad_t','Humedad_t','Precipitacion_t']]
        y_nub =  self.models_df['Nubosidad']
        self.cloudiness_model = LinearRegression().fit(X_nub, y_nub)

        X_hum =  self.models_df[['Humedad_t','Precipitacion_t']]
        y_hum =  self.models_df['Humedad_Relativa_(%)']
        self.relative_humidity_model = LinearRegression().fit(X_hum, y_hum)
        
    def __generate_distributions(self):
        df = self.input_df

        self.distribution_info["radiation"] = DistributionData(
            avg=df['RadiacionGlobal_(cal/cm2)'].astype(str).str.replace(',', '.').astype(float).mean(),
            desv=df['RadiacionGlobal_(cal/cm2)'].astype(str).str.replace(',', '.').astype(float).std()
        )
        self.distribution_info["solar_light"] = DistributionData(
            avg=df['Brillo_Solar_(h)'].astype(str).str.replace(',', '.').astype(float).mean(),
            desv=df['Brillo_Solar_(h)'].astype(str).str.replace(',', '.').astype(float).std()
        )
        self.distribution_info["cloudiness"] = DistributionData(
            avg=df['Nubosidad'].astype(str).str.replace(',', '.').astype(float).mean(),
            desv=df['Nubosidad'].astype(str).str.replace(',', '.').astype(float).std()
        )
        self.distribution_info["relative_humidity"] = DistributionData(
            avg=df['Humedad_Relativa_(%)'].astype(str).str.replace(',', '.').astype(float).mean(),
            desv=df['Humedad_Relativa_(%)'].astype(str).str.replace(',', '.').astype(float).std()
        )
        self.min_rainfall = df["Precipitacion_(mm)"].astype(str).str.replace(',', '.').astype(float).min()
        self.max_rainfall = df["Precipitacion_(mm)"].astype(str).str.replace(',', '.').astype(float).max()

        print('radiation: ', self.distribution_info["radiation"].avg, self.distribution_info["radiation"].desv)
        print('solar_light: ', self.distribution_info["solar_light"].avg, self.distribution_info["solar_light"].desv)
        print('cloudiness: ', self.distribution_info["cloudiness"].avg, self.distribution_info["cloudiness"].desv)
        print('relative humidity: ', self.distribution_info["relative_humidity"].avg, self.distribution_info["relative_humidity"].desv)
        print('rainfall: ', self.min_rainfall, self.max_rainfall)
        

    def start_simulation(self, days:int):
        self.numbers_model.init_numbers()
        if self.models_df is None and self.input_df is None:
            self.__load_data()
            self.__generate_models()
            self.__generate_distributions()
        init_data = self.__generate_initial_data()
        last_data = init_data
        results : list[RadiationDayData] = []
        for i in range(1,days+1):
            data_obtained = self.__generate_day_radiation_data(i, last_data)
            results.append(data_obtained)
            last_data = data_obtained
        results_radiation_avg = sum([result.radiation for result in results])/days
        radiation_from_data = self.__get_n_days_from_dataset(days)
        from_data_average = sum([result.radiation for result in radiation_from_data])/days
        error = self.__get_error(from_data_average, results_radiation_avg)
        radiation_formula = "Radiación(t+1) = {:.3f}*Radiación(t) + {:.3f}*Brillo(t) + {:.3f}*Precipitacion(t) + {:.3f}*Nubosidad(t) + {:.3f}".format(
            *self.radiation_model.coef_, self.radiation_model.intercept_)
        solar_light_formula = "Brillo(t+1) = {:.3f}*Brillo(t) + {:.3f}*Precipitacion(t) + {:.3f}*Nubosidad(t) + {:.3f}".format(
            *self.solar_light_model.coef_, self.solar_light_model.intercept_)
        cloudiness_formula = "Nubosidad(t+1) = {:.3f}*Nubosidad(t) + {:.3f}*Humedad(t) + {:.3f}*Precipitacion(t) + {:.3f}".format(
            *self.cloudiness_model.coef_, self.cloudiness_model.intercept_)
        relative_humidity_formula = "Humedad(t+1) = {:.3f}*Humedad(t) + {:.3f}*Precipitacion(t) + {:.3f}".format(
            *self.relative_humidity_model.coef_, self.relative_humidity_model.intercept_)
        result = Result(results, radiation_from_data, init_data, results_radiation_avg, from_data_average, error,
                        radiation_formula, solar_light_formula, cloudiness_formula, relative_humidity_formula)
        self.presenter.show_results(result)

    def __generate_initial_data(self) -> RadiationDayData:
        solar_ligt_dist = self.distribution_info["solar_light"]
        cloudiness_dist = self.distribution_info["cloudiness"]
        relative_humidity_dist = self.distribution_info["relative_humidity"]
        radiation_dist = self.distribution_info["radiation"]
        solar_light = self.__ni_normal_function(self.__get_pseudo_random_number(), solar_ligt_dist.avg, 
                                                solar_ligt_dist.desv)
        cloudiness = self.__ni_normal_function(self.__get_pseudo_random_number(), cloudiness_dist.avg, 
                                                cloudiness_dist.desv)
        relative_humidity = self.__ni_normal_function(self.__get_pseudo_random_number(), relative_humidity_dist.avg, 
                                                relative_humidity_dist.desv)
        rainfall = self.__ni_uniform_function(self.__get_pseudo_random_number(), self.min_rainfall, self.max_rainfall)
        radiation = self.__ni_normal_function(self.__get_pseudo_random_number(), radiation_dist.avg, 
                                                radiation_dist.desv)
        return RadiationDayData(solar_light, cloudiness, relative_humidity, rainfall, radiation)
    
    def __generate_day_radiation_data(self, day:int, last_data: RadiationDayData) -> RadiationDayData:
        rad = last_data.radiation
        bril = last_data.solar_light
        nub = last_data.cloudiness
        hum = last_data.relative_humidity
        pluv = last_data.rainfall

        rad_pred = self.radiation_model.predict([[rad, bril, pluv, nub]])[0]
        bril_pred = self.solar_light_model.predict([[bril, pluv, nub]])[0]
        nub_pred = self.cloudiness_model.predict([[nub, hum, pluv]])[0]
        hum_pred = self.relative_humidity_model.predict([[hum, pluv]])[0]

        #rainfall = self.__ni_uniform_function(self.__get_pseudo_random_number(), self.min_rainfall, self.max_rainfall)

        return RadiationDayData(bril_pred, nub_pred, hum_pred, pluv, rad_pred,day=day)
        
    def __get_pseudo_random_number(self):
        return self.numbers_model.get_next_pseudo_random_number()
    
    def __ni_normal_function(self, r_i, avg, desv):
        return float(norm.ppf(r_i, loc=avg, scale=desv))
    
    def __ni_uniform_function(self, r_i, a, b):
        return a + (b - a) * r_i
    
    def __get_n_days_from_dataset(self, days:int) -> list[RadiationDayData]:
        init = int(self.__ni_uniform_function(self.__get_pseudo_random_number(), 0, self.total))
        if init + days <= self.total:
            last = init + days
            selection = self.df.iloc[init:last]
        else:
            init = self.total - days
            selection = self.df.iloc[init:]
        selection = selection.reset_index(drop=True)
        return [RadiationDayData(row['Brillo_Solar_(h)'], row['Nubosidad'], row['Humedad_Relativa_(%)'], 
                                 row['Precipitacion_(mm)'], row['RadiacionGlobal_(cal/cm2)']) for _, row in selection.iterrows()]
    
    def __get_error(self, real, pred):
        error = abs((real - pred) / real) * 100
        return round(error, 2)
    
    def get_comparison_data(self, x: list[int], y1: list[float], y2: list[float], max_x_len = 35
                            ) -> tuple[list[int], list[float], list[float], str]:
        days = len(x)
        weeks = days / 7
        months = days / 30
        init_day = 0
        end_day = None
        value = None
        div = None
        label = "dia"
        if days > max_x_len and weeks <= max_x_len:
            end_day = 7
            value = weeks
            div = 7
            label = "semana (7 dias)"
        elif weeks > max_x_len and months <= max_x_len:
            end_day = 30
            value = months
            div = 30
            label = "mes (30 dias)"
        elif months > max_x_len:
            end_day = 365
            value = days / 365
            div = 365
            label = "año (365 dias)"
        if end_day is not None:
            x_new = []
            y1_new = []
            y2_new = []
            its = int(value) + 1 if value % 1 != 0 else int(value)
            for i in range(its):
                y1_i = y1[init_day:end_day]
                y2_i = y2[init_day:end_day]
                avg_y1 = sum(y1_i) / len(y1_i)
                avg_y2 = sum(y2_i) / len(y2_i)
                x_new.append(i+1)
                y1_new.append(avg_y1)
                y2_new.append(avg_y2)
                init_day += div
                end_day += min(div, days - init_day)
            return x_new, y1_new, y2_new, label
        return x, y1, y2, label