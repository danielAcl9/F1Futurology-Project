import pickle
import pandas as pd
import numpy as np
from functions import *

dfF = pd.DataFrame(columns=['NNUM', 'DRIVER', 'PRED-POS', 'CIRCUIT', 'DDD2'])

with open('jupyter\\rfr_model.pkl', 'rb') as archivo:
    rfr_model = pickle.load(archivo)

with open('jupyter\\ridge_model.pkl', 'rb') as archivo:
    ridge_model = pickle.load(archivo)

with open('jupyter\lasso_model.pkl', 'rb') as archivo:
    lasso_model = pickle.load(archivo)

with open('jupyter\knn_model.pkl', 'rb') as archivo:
    knn_model = pickle.load(archivo) 

with open('jupyter\\xgbmodel.pkl', 'rb') as archivo:
    xgb_model = pickle.load(archivo)

print("Lista de modelos\n 1. Random Forest Regressor \n 2. Ridge Regression \n 3.LASSO Regression \n 4. K-Nearest Neighbour \n 5. XGBoost")

model = int(input("Seleccione modelo a crear:"))

pilotos = [1, 2, 4, 10, 11, 14, 16, 18, 20, 22, 23, 24, 27, 31, 40, 44, 55, 63, 77, 81]
numR = 13


for i in pilotos:
    numD = i

    driverSeasonRank = get_driver_season_rank(numD)
    driverSeasonPoints = get_driver_season_points(numD)
    driverSeasonGps = get_driver_season_gps(numD)
    driverSeasonWins = get_driver_season_wins(numD)
    driverSeasonPodiums = get_driver_season_podiums(numD)
    driverSeasonPoles = get_driver_season_poles(numD)
    driverSeasonFastLaps = get_driver_season_fastlaps(numD)
    driverSeasonLeadlaps = get_driver_season_leadlaps(numD)
    driverCareerWins = get_driver_career_wins(numD)
    driverCareerPodiums = get_driver_career_podiums(numD)
    driverCareerPoles = get_driver_career_poles(numD)
    driverCareerFastlaps = get_driver_career_fastlaps(numD)
    driverCareerGps = get_driver_career_gps(numD)
    driverCareerSeason = get_driver_career_season(numD)

    #-------------------------- Equipos --------------------------
    #Estos dos no entran en el data set
    teamId = get_team_id(numD)
    teamName = get_team_name(teamId)
    
    teamSeasonWins = get_team_season_wins(teamId)
    teamSeasonPodiums = get_team_season_podiums(teamId)
    teamSeasonPoles = get_team_season_poles(teamId)
    teamSeasonFastlaps = get_team_season_fastlaps(teamId)
    teamSeasonLeadlaps = get_team_season_leadlaps(teamId)
    teamSeasonPoints = get_team_season_points(teamId)
    teamAverageWins = get_team_average_wins(teamId)
    teamAveragePodiums = get_team_average_podiums(teamId)
    teamTotalGps = get_team_total_gps(teamId)
    teamSeasons = get_team_seasons(teamId)

    #-------------------------- Pista --------------------------

    #Este no va
    circuitName = get_circuit_name(numR)

    circuitLength = get_circuit_length(numR)
    circuitTemp = get_circuit_temp(numR)
    circuitRain = get_circuit_rain(numR)

    qualiPos = get_quali_pos(numD, numR)
    qualiTime = get_quali_time(numD, numR)

    driverName = get_driver_name(numD)
    datos = {'driver_season_rank': [driverSeasonRank],
            'driver_season_points': [driverSeasonPoints],
            'driver_season_gps': [driverSeasonGps],
            'driver_season_wins': [driverSeasonWins],
            'driver_season_podiums': [driverSeasonPodiums],
            'driver_season_poles': [driverSeasonPoles],
            'driver_season_fastlaps': [driverSeasonFastLaps],
            'driver_season_leadlaps': [driverSeasonLeadlaps],
            'driver_career_wins_avg': [driverCareerWins],
            'driver_career_podiums_avg': [driverCareerPodiums], #10
            'driver_career_poles': [driverCareerPoles],
            'driver_career_fastlaps': [driverCareerFastlaps],
            'driver_career_gps': [driverCareerGps],
            'driver_career_season': [driverCareerSeason],
            'team_season_wins': [teamSeasonWins],
            'team_season_podiums': [teamSeasonPodiums],
            'team_season_poles': [teamSeasonPoles], #17
            'team_season_fastlaps': [teamSeasonFastlaps],
            'team_season_leadlaps': [teamSeasonLeadlaps],
            'team_season_points': [teamSeasonPoints], #20
            'team_average_wins': [teamAverageWins],
            'team_average_podiums': [teamAveragePodiums],
            'team_total_gps': [teamTotalGps],
            'team_seasons': [teamSeasons],
            'circuit_length': [circuitLength],
            'circuit_temp': [circuitTemp],
            'circuit_rain': [circuitRain],
            'quali_pos': [qualiPos],
            'quali_time': [qualiTime],
            'circuit_id': [numR], #30
            'team_id': [teamId]
    }
    
    dfEnviar = pd.DataFrame(datos)
    dfEnviar = np.array(dfEnviar)

    if model == 1:
        name = 'Random Forest Regressor Predictions'
        nueva_pred = rfr_model.predict(dfEnviar)
            
        nn = float(nueva_pred)
        res = float("{:.2f}".format(nn))
    
    elif model == 2:
        name = 'Ridge Regressor Predictions'
        nueva_pred = ridge_model.predict(dfEnviar)
            
        nn = float(nueva_pred)
        res = float("{:.2f}".format(nn))

    elif model == 3:
        name = 'Lasso Predictions'
        nueva_pred = lasso_model.predict(dfEnviar)
            
        nn = float(nueva_pred)
        res = float("{:.2f}".format(nn))
            
    elif model == 4:
        name = 'KNN Predictions'
        nueva_pred = knn_model.predict(dfEnviar)
            
        nn = float(nueva_pred)
        res = float("{:.2f}".format(nn))

    elif model == 5:
        name = 'XGBoost Predictions'
        nueva_pred = knn_model.predict(dfEnviar)
            
        nn = float(nueva_pred)
        res = float("{:.2f}".format(nn))
 

    dfF.loc[len(dfF.index)] = [i, driverName, res, circuitName, 0]
    dfF = dfF.sort_values(by='PRED-POS', ascending=True)



dfF.loc[dfF['NNUM'] == 1, 'DDD2'] = 3
dfF.loc[dfF['NNUM'] == 14, 'DDD2'] = 77
dfF.loc[dfF['NNUM'] == 40, 'DDD2'] = 300


print(f'{name}')
print(dfF)


# dfF.to_csv(f'{name}_results.csv', encoding='utf-8')