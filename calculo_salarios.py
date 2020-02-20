# -----------------------------------------------------------
# Prueba técnica backend, Resuelve
#
# (C) 2020 Angel Negib Ramirez Alvarez, CDMX, Mexico
# Released under GNU Public License (GPL)
# email iangelmx.isc@gmail.com {
# Este script calcula el salario completo del Resuelve FC
# con base en un JSON de entrada. El problema a resolver se
# encuentra disponible en:
# https://github.com/resuelve/prueba-ing-backend
# El presente fue construido con Python en su versión 3.7.3 
# Está diseñado para la puesta en producción en sistemas 
# que soporten el paradigma de la programación estructurada.
# La documentación completa de la solución está disponible en
# el archivo README del repositorio:
# https://github.com/iangelmx/solucion-prueba-resuelve
# -----------------------------------------------------------

import json


def read_input_players() -> dict:
    """
    Process that read from the std input a JSON to calculate the salary of the players received
    This receives an string like:
    [  
        {  
            "nombre":"Juan Perez",
            "nivel":"C",
            "goles":10,
            "sueldo":50000,
            "bono":25000,
            "sueldo_completo":null,
            "equipo":"rojo"
        }, ...
    ]

    And this return a dict of the input received.
    """
    arreglo_json = ""
    renglon = input("Dame la entrada del JSON, se detendrá la lectura en EOF\n")
    while True:
        arreglo_json += renglon
        try:
            renglon = input("")
        except EOFError:
            print("JSON Recibido.")
            break
    
    try:
        entrada = json.loads( arreglo_json )
        return entrada
    except Exception as ex:
        print("Fatal error: La entrada del JSON de jugadores no tiene un formato válido de JSON. \nDetails:", ex)
        return None

def get_team_compliance():
    pass

def get_individual_compliance(player : dict, min_goals_level : int) -> float:
    """
    Process that calculates the individual compliance of a player.
    Receive a dict of player like:
    {  
        "nombre":"Juan Perez",
        "nivel":"C",
        "goles":10,
        "sueldo":50000,
        "bono":25000,
        "sueldo_completo":null,
        "equipo":"rojo"
    }
    AND the minimum goals that the player has to score : int

    Return compliance : float
    """
    real_goals = player.get('goles', None)
    if real_goals is None:
        return {'ok' : False, 'description_error':f'No hay registro de goles para el jugador: {player}'}
    
    bonus = player.get('bono', None)
    if bonus is None:
        return {'ok' : False, 'description_error':f'El jugador no tiene un bono asignado: {player}'}

    team_player = player.get('equipo', None)
    if team_player is None:
        return {'ok' : False, 'description_error':f'Nombre de equipo inesperado para el jugador: {player}'}

    if min_goals_level is None:
        return {'ok' : False, 'description_error':f'El jugador pertenece a un nivel sin goles mínimos: {player}'}
    
    
    individual_compliance = 0
    if real_goals > min_goals_level:
        individual_compliance = 100
    else:
        individual_compliance = (100*real_goals) / min_goals_level
    
    return individual_compliance

def get_levels_of_team():
    pass

def calculate_player_bonus():
    pass

def get_players_salary(input_data:str) -> str:
    print(input_data)

    print(get_individual_compliance(input_data[0], 20))

if __name__ == "__main__":
    #Read the input data
    input_data = read_input_players()
    while input_data is None:
        print("Intente ingresarlo nuevamente...")
        input_data = read_input_players()
    get_players_salary(input_data)