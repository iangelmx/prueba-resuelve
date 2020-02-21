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

def get_team_compliance(players :dict, levels_goals:dict) -> float:
	"""
	Process that from the levels and minimum goals return a dict with the compliance by team
	Receives a dict player and a dict list of levels:
		player <dict>,
		levels_goals <list>[
			{
				'nivel' :'A',
				'goles_min' : 5
			}, ...
		]
	Returns a dict like:
		{
			'level_x' : compliance (float)
		}
		"""
	goals_team = {}
	compliance_team = {}

	for jugador in players:
		team = jugador.get('equipo')
		
		goal_level = levels_goals.get( jugador.get('nivel'), 0)
		goals_scored = jugador.get('goles', 0)

		if team not in goals_team:
			goals_team[ team ] = { 'acum':goals_scored, 'goal':goal_level }
		else:
			goals_team[ team ]['acum'] += goals_scored
			goals_team[ team ]['goal'] += goal_level
	
	for team in goals_team:
		if team not in compliance_team:
			if goals_team[team].get('acum', 0) > goals_team[team].get('goal', 0):
				compliance_team[ team ] = { 'compliance':100  }
			else:
				try:
					compliance_team[ team ] = {
						'compliance' : (goals_team[team].get('acum',0) * 100)/goals_team[team].get('goal',0)
					}
				except ZeroDivisionError as ex:
					print(f"Warning: An error has ocurred while calculating compliance of team. ZeroDivision in team: {team}; with a goal of: {goals_team[team].get('goal')}")
		
	#print("Cumplimiento equipo:", compliance_team)
	return compliance_team

def get_individual_compliance(player : dict, min_goals_level : int) -> dict:
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
	real_goals = player.get('goles')
	if real_goals is None:
		return {'ok' : False, 'description_error':f'No hay registro de goles para el jugador: {player}'}
	
	if min_goals_level is None:
		return {'ok' : False, 'description_error':f'El jugador pertenece a un nivel sin goles mínimos: {player}'}
	
	
	individual_compliance = 0
	if real_goals > min_goals_level:
		individual_compliance = 100
	else:
		individual_compliance = (100*real_goals) / min_goals_level
	
	return {'ok': True, 'description':{'value':individual_compliance}}

def get_levels_of_team() -> dict:
	"""
	Return the levels in a dict way from a dict list
	{
		'level_x' : goles_min (integer)
	}
	"""
	input_levels = [
		{
			'nivel':'A',
			'goles_min' : 5
		},
		{
			'nivel':'B',
			'goles_min' : 10
		},
		{
			'nivel':'C',
			'goles_min' : 15
		},
		{
			'nivel':'Cuauh',
			'goles_min' : 20
		}
	]
	levels = {}
	for level in input_levels:
		levels[ level['nivel'] ] = level['goles_min']
	return levels

def calculate_player_bonus(player:dict, min_goals_level:int, team_compliance:float) -> dict:
	"""
	This is the process to calculate de salary of individual player
	Receive a JSON of the player like:
	player <- {  
		"nombre":"Juan Perez",
		"nivel":"C",
		"goles":10,
		"sueldo":50000,
		"bono":25000,
		"sueldo_completo":null,
		"equipo":"rojo"
	}
	"""

	bonus = player.get('bono')
	if bonus is None or bonus < 0:
		return {'ok' : False, 'description_error':f'El jugador no tiene un bono asignado o es negativo: {player}'}

	individual_compliance = get_individual_compliance(player, min_goals_level)
	
	if individual_compliance.get('ok') in [False, None]:
		print(f"Error while calculating individual compliance with:{player}\nDetalles: {individual_compliance.get('description_error')}")
		return {'ok':False, 'description': individual_compliance.get('description') }
	
	individual_compliance = individual_compliance.get('description', {}).get('value',0)
	
	final_compliance = (individual_compliance + team_compliance)/2

	final_bonus = bonus * (final_compliance/100)
	
	return {'ok':True, 'description': {'value':final_bonus} }

def get_players_salary(input_data:dict, traceback = False) -> str:
	"""
	Devuelve un arreglo de JSONs con el sueldo completo de los jugadores de
	Resuelve FC
	[
		{  
			"nombre":"Juan Perez",
			"goles_minimos":10,
			"goles":10,
			"sueldo":50000,
			"bono":25000,
			"sueldo_completo":null,
			"equipo":"rojo"
		}
	]
	"""
	
	#Getting the levels of the Resuelve FC
	levels_goals = get_levels_of_team()
	#Getting the compliance of all the teams
	teams_compliance = get_team_compliance(input_data, levels_goals)
	#Initialize the list that save the players with errors
	failed = []

	for jugador in input_data:
		#Getting the minimum goals according the level of the current player
		min_goals = levels_goals.get(jugador.get('nivel'))
		team_player = jugador.get('equipo')
		if team_player is None:
			print(f'Warning: Unexpected name of team for: {jugador}. Can not calculate salary.')
			failed.append(jugador)
			continue
		#Getting the compliance of their team
		team_compliance = teams_compliance.get( team_player, {}  ).get('compliance', 0)
		#Getting the bonus for the player
		bonus = calculate_player_bonus(jugador, min_goals, team_compliance )

		if bonus.get('ok') == True:
			final_bonus = bonus.get('description', {}).get('value', 0)
		else:
			print(f"Warning: An error has ocurred while calculating bonus of {jugador}:\n", bonus)
			failed.append(jugador)
			continue
		#Getting the fixed salary of the current player
		fixed_salary = jugador.get('sueldo')
		if fixed_salary is None:
			failed.append(jugador)
			print(f"Warning: An error has ocurred while getting value of 'sueldo':\n", {'ok':False, 'description_error':f'Sueldo no estipulado para el jugador:{jugador}'})
			continue
			
		#Add the rest of the values to the Dict of player
		jugador['sueldo_completo'] = final_bonus + fixed_salary
		jugador['goles_minimos'] = min_goals
		#Remove the 'nivel' key and its value
		jugador.pop("nivel", None)
	
	
	output_data = json.dumps(input_data, indent=2)

	response = {'ok':True, 'description':input_data, 'failed':failed}

	if traceback == True:
		#Transform the list of dicts to a JSONs array
		output = json.dumps(response, indent=2)
	else:	
		#Transform the list of dicts to a JSONs array
		output = output_data
	
	#Print the output
	print(output)
	
	return output

if __name__ == "__main__":
	#Read the input data
	input_data = read_input_players()
	while input_data is None:
		print("Intente ingresarlo nuevamente...")
		input_data = read_input_players()
	
	# Se obtiene el salario de los jugadores
	# El JSON de salida en formato STR está en la variable salario_jugadores
	salario_jugadores = get_players_salary(input_data)