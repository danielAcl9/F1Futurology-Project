import fastf1 as ff1
import pandas as pd
from fastf1.ergast import Ergast

# Create the dataframe
ergast = Ergast()
df = pd.DataFrame()

# Inputs for year and race
num_year = input("Insert season year: ")
num_race = input("Insert race number: ")

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

#Cargar la sesión de la carrera
race = ff1.get_session(int(num_year), int(num_race), 'R')
#Cargar la carrera de clasificación
quali = ff1.get_session(int(num_year), int(num_race), 'Q')

race.load(weather = True)
quali.load()

laps = race.laps
res = race.results
res_Q = quali.results

#Asignar nombre, abreviación, equipo, e información del circuito
df['driver_number'] = res.DriverNumber
df['driver_name'] = res.BroadcastName
df['driver_abb'] = res.Abbreviation

df['team_name'] = res.TeamName

# Get circuit data, name and country
grand_prix = ergast.get_circuits(season = num_year, round = num_race)

# Convert value to string and then truncate
gp_circuit = str(grand_prix['circuitName'])
gp_country = str(grand_prix['country'])

cir_name = gp_circuit.rsplit('\n', 3)[0]
coun_name = gp_country.rsplit('\n', 3)[0]
cir_name2 = cir_name[5:]
coun_name2 = coun_name[5:]

df['circuit_name'] = cir_name2
df['circuit_country'] = coun_name2

#Obtener informaciónd el clima en la carrera
clima = race.weather_data

temp = clima['AirTemp'].mean()
rain = clima['Rainfall'].mean()

#Agregar la información del clima al DF
df['circuit_temp'] = temp
df['circuit_rain'] = rain


# Add quali data, and replace the empty values with the last registered time
q_laptime = pd.Series(res_Q['Q3'])
q_laptime = q_laptime.fillna(res_Q['Q2'])
q_laptime = q_laptime.fillna(res_Q['Q1'])

# Transform from datetime64 to total seconds in their quali best laptime
q_laptime = q_laptime.dt.total_seconds()

# Add Quali final position and best laptime
df['quali_pos'] = res_Q['Position']
df['quali_time'] = q_laptime

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# Add final position
df['race_pos'] = res.Position

#Print data set
print(df)

#Function to export as a CSV
def ToCSV(data):
    data.to_csv(f'df_{num_year}_{num_race}{coun_name2}.csv', encoding='utf-8')

ToCSV(df)