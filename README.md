# Resolución Problema Ingeniería Resuelve

En este archivo README se explica a mejor detalle la solución generada al problema de ingeniería de Resuelve (disponible en: [https://github.com/resuelve/prueba-ing-backend](https://github.com/resuelve/prueba-ing-backend))

# Descripción del problema:
De forma sintetizada, se necesita generar una solución o programa que pueda recibir a la entrada un JSON con la estructura siguiente:

    [
	  {
	    "nombre":"Juan Perez",
	    "nivel":"C",
        "goles":10,
        "sueldo":50000,
        "bono":25000,
        "sueldo_completo":null,
        "equipo":"rojo"
	  },
	  ...,
	  {
	    "nombre":"EL Cuauh",
	    "nivel":"Cuauh",
        "goles":30,
        "sueldo":100000,
        "bono":30000,
        "sueldo_completo":null,
        "equipo":"azul"
	  }
	]
    
De acuerdo al nivel de cada jugador, deberá anotar un número de goles, el cual dependiendo de su cumplimiento decidirá si se le paga de forma completa o parcial su bono.
Para mayor detalle, tablas de niveles y ejemplo de casos, se puede consultar de forma completa el problema en:
[https://github.com/resuelve/prueba-ing-backend#problema](https://github.com/resuelve/prueba-ing-backend#problema)


# Análisis y diseño

## Requisitos funcionales a cubrir:
- Calcular su sueldo completo contemplando el sueldo fijo y el variable con el *bono calculado*
- Llenar en el JSON de salida la llave ``sueldo_completo`` del JSON de entrada con la siguiente estructura:
	 `[
	    {
	      "nombre":"El Rulo",
	      "goles_minimos":10,
	      "goles":9,
	      "sueldo":30000,
	      "bono":15000,
	      "sueldo_completo": 14250,
	      "equipo":"rojo"
	    }
	]`

## Requerimientos no funcionales a cubrir:
- Calcular el alcance individual de cada jugador de acuerdo a la cantidad de goles anotados contra la meta que debió cubrir.
- Calcular el alcance por equipo de los jugadores de acuerdo a la cantidad de goles anotados en conjunto contra los que se debían anotar.
- Calcular el bono que se le deberá pagar a cada jugador con base en el alcance individual y el de su equipo.

## Diseño general de la solución

El programa funcionará bajo un diseño funcional, puesto que no requiere de mayor complejidad el cálculo del sueldo completo de cada jugador de Resuelve FC.

### Módulos necesarios identificados

 1. **Obtener salario de los jugadores**: Será el proceso maestro, encargado de orquestar e invocar al resto de los métodos.
 2. **Lectura/obtención de los datos de entrada** : *suponiendo que el programa se ejecutará de forma independiente a un sistema*, es el procedimiento que desde la entrada estándar leerá el JSON con los datos de los equipos.
 3. **Obtener los niveles y goles mínimos para Resuelve FC**: Es la función que nos proporcionará los goles mínimos de cada equipo.
 4. **Calcular el bono de un jugador**: Es el proceso que recibirá el JSON que representa a un jugador y calculará su sueldo completo.
 5. **Calcular el alcance individual de un jugador**: Es el proceso que con base en los goles anotados y al nivel del jugador, regresará el porcentaje de alcance obtenido por el jugador.
 6. **Calcular el alcance por equipo**: Es el proceso que con base en los goles anotados y niveles de los jugadores del equipo, calculará y retornará el alcance del equipo.