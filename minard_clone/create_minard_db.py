import pandas as pd
import sqlite3

class CreateMinardDB:
    def __init__(self):
        with open("data/minard.txt") as f:
            self.lines = f.readlines()

        column_names = self.lines[2].split()
        # print(column_names)

        patterns_to_be_replaced = {"(", ")", "$", ","}
        abjusted_column_names = []
        for column_name in column_names:
            for pattern in patterns_to_be_replaced:
                if pattern in column_name:
                    column_name = column_name.replace(pattern, "")
            abjusted_column_names.append(column_name)
        # print(patterns_to_be_replaced)
        self.column_names_city = abjusted_column_names[:3]
        self.column_names_temperature = abjusted_column_names[3:7]
        self.column_names_troop = abjusted_column_names[7:]
        # print(column_name_city,'\n',column_name_temperature,'\n',column_name_troop)

    def create_city_df(self):
        i = 6
        longitudes, latitudes, cities = [], [], []
        while i <= 25:
            long, lat, city = self.lines[i].split()[0:3]
            longitudes.append(float(long))
            latitudes.append(float(lat))
            cities.append(city)
            i += 1
        # print(longitudes,'\n',latitudes,'\n',cities)

        city_data = (longitudes, latitudes, cities)
        city_df = pd.DataFrame()
        for column_name, data in zip(self.column_names_city, city_data):
            city_df[column_name] = data
        return city_df

    def create_temperature_df(self):
        i = 6
        longitude, tempterature, days, dates = [], [], [], []
        while i <= 14:
            lont, temp, day = self.lines[i].split()[3:6]
            date = self.lines[i].split()[6] + " " + self.lines[i].split()[7]
            longitude.append(float(lont))
            tempterature.append(int(temp))
            days.append(day)
            if i == 10:
                dates.append('Nov 24')
            else:
                dates.append(date)
            i += 1
        # print(longitude, '\n',tempterature, '\n', days, '\n', dates)
        temperature_data = (longitude, tempterature, days, dates)
        temperature_df = pd.DataFrame()
        for column_name, data in zip(self.column_names_temperature, temperature_data):
            temperature_df[column_name] = data
        return temperature_df

    def create_troop_df(self):
        i = 6
        longitude, latitude, survival, direction, division = [], [], [], [], []
        while i <= 53:
            lonp, latp, surviv, direc, div = self.lines[i].split()[-5:]
            longitude.append(float(lonp))
            latitude.append(float(latp))
            survival.append(int(surviv))
            direction.append(direc)
            division.append(int(div))
            i += 1
        # print(longitude,'\n', latitude,'\n', survival,'\n', direction,'\n', division)
        troop_data = (longitude, latitude, survival, direction, division)
        troop_df = pd.DataFrame()
        for column_name, data in zip(self.column_names_troop, troop_data):
            troop_df[column_name] = data
        return troop_df
    
    def create_minard_db(self):
        connection = sqlite3.connect('data/minard.db')
        df_dict = {
            "cities":self.create_city_df(),
            "temperatures":self.create_temperature_df(),
            "troops":self.create_troop_df()
        }
        for k, v in df_dict.items():
            v.to_sql(name=k, con=connection, index=False, if_exists='replace')
        connection.close()

create_minard_db = CreateMinardDB()
create_minard_db.create_minard_db()
