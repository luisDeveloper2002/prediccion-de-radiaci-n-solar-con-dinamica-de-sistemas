class DistributionData:
    def __init__(self, avg, desv):
        self.avg = avg
        self.desv = desv

class RadiationDayData:
    def __init__(self, solar_light: float, cloudiness: float, relative_humidity: float, 
                 rainfall: float, radiation: float, day=0):
        self.solar_light = solar_light
        self.cloudiness = cloudiness
        self.relative_humidity = relative_humidity
        self.rainfall = rainfall
        self.radiation = radiation
        self.day = day

class Result:
    def __init__(self, radiation_data_obtained: list[RadiationDayData], 
                 radiation_data_predicted: list[RadiationDayData], 
                 initial_data: RadiationDayData, radiation_obtained_average: float, 
                 radiation_predicted_average: float, error: float,
                 radiation_formula: str, solar_light_formula: str, 
                 cloudiness_formula: str, relative_humidity_formula: str):
        self.radiation_data_obtained = radiation_data_obtained
        self.radiation_data_predicted = radiation_data_predicted
        self.initial_data = initial_data
        self.radiation_obtained_average = radiation_obtained_average
        self.radiation_predicted_average = radiation_predicted_average
        self.error = error
        self.radiation_formula = radiation_formula
        self.solar_light_formula = solar_light_formula
        self.cloudiness_formula = cloudiness_formula
        self.relative_humidity_formula = relative_humidity_formula