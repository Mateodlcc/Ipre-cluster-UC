import matplotlib.pyplot as plt


###############################################
######       DEFINICION DE VALORES       ######
###############################################
Q = float(input("Valor inicial de la carga: "))
V = float(input("Valor inicial del voltaje: "))
dt = float(input("Valor de Delta t (salto [mientras menor sea este valor (positivo), mejor sera la curva resultante]): "))
R = float(input("Valor de la resistencia: "))
Vmax = float(input("Valor de Voltaje maximo: "))
c = float(input("Valor de la capacitancia: "))
T = float(input("Tiempo de evaluacion: "))
grafica = input("¿Desea graficar Voltaje (V), Carga (Q) o ambos (A)?: ")

def validar_grafica(grafica):
    if grafica not in ["V", "Q", "A"]:        # Para verificar que sea algo válido
        print()
        print("Invalido!")
        grafica = input("¿¿Desea graficar Voltaje (V), Carga (Q) o ambos (A)?: ")
        validar_grafica(grafica)

ambos = input("¿Desea graficar carga (C), descarga (D) o ambos (A)?: ")

def validar_ambos(ambos):
    if ambos not in ["C", "D", "A"]:        # Para verificar que sea algo válido
        print()
        print("Invalido!")
        ambos = input("¿Desea graficar carga (C), descarga (D) o ambos (A)?: ")
        validar_ambos(ambos)

# VALORES DE TESTEO
# Q = 0
# V = 0
# dt = .1
# R = 10
# Vmax = 3
# c = .5
# T = 50

# Creacion de los plts correspondientes
if grafica == "V":              # Creación del plot para V
    fig2, ax2 = plt.subplots()

elif grafica == "Q":            # Creación del plot para Q
    fig1, ax1 = plt.subplots()

elif grafica == "A":
    fig1, ax1 = plt.subplots()
    fig2, ax2 = plt.subplots()

###############################################
######         FUNCIONES PARA Q          ######
###############################################
def calcular_q_carga(Q, dt, R, Vmax, c, T, ambos):
    t = 0
    while t < T:
        dQ = Vmax*dt/R - Q*dt/(R*c)
        Q = Q + dQ
        if Q < 0:
            Q = 0
        t = t + dt

        ax1.plot(t, Q, "or")

        ax1.set(xlabel='tiempo [s]', ylabel='Q [C]', title='Carga v/s tiempo')
        ax1.grid()

    if ambos is True:
        calcular_q_descarga(Q, dt, R, c, T, t)

def calcular_q_descarga(Q, dt, R, c, T, t0):
    t = t0
    while t < T + t0:
        dQ = -Q*dt/(R*c)
        Q = Q + dQ
        if Q < 0:
            Q = 0
        t = t + dt

        ax1.plot(t, Q, "or")
        ax1.set(xlabel='tiempo [s]', ylabel='Q [C]', title='Carga v/s tiempo')
        ax1.grid()

###############################################
######         FUNCIONES PARA V          ######
###############################################
def calcular_v_carga(V, dt, R, Vmax, c, T, ambos):
    t = 0
    while t < T:
        dV = Vmax*dt/R*c - V*dt/(R*c**2)
        V = V + dV
        t = t + dt

        ax2.plot(t, V, "or")

        ax2.set(xlabel='tiempo [s]', ylabel='V [V]', title='Voltaje  v/s tiempo')
        ax2.grid()

    if ambos is True:
        calcular_v_descarga(V, dt, R, c, T, t)

def calcular_v_descarga(V, dt, R, c, T, t0):
    t = t0
    while t < T + t0:
        dV = -V*dt/(R*c**2)
        V = V + dV
        if V < 0:
            V = 0
        t = t + dt

        ax2.plot(t, V, "or")
        ax2.set(xlabel='tiempo [s]', ylabel='V [V]', title='Voltaje v/s tiempo')
        ax2.grid()

###############################################
######         REALIZAR LO PEDIDO        ######
###############################################
if grafica == "V":
    if ambos == "A":
        calcular_v_carga(V, dt, R, Vmax, c, T, True)
    elif ambos == "C":
        calcular_v_carga(V, dt, R, Vmax, c, T, False)
    elif ambos == "D":
        calcular_v_descarga(V, dt, R, c, T, 0)

elif grafica == "Q":
    if ambos == "A":
        calcular_q_carga(Q, dt, R, Vmax, c, T, True)
    elif ambos == "C":
        calcular_q_carga(Q, dt, R, Vmax, c, T, False)
    elif ambos == "D":
        calcular_q_descarga(Q, dt, R, c, T, 0)

elif grafica == "A":
    if ambos == "A":
        calcular_q_carga(Q, dt, R, Vmax, c, T, True)
        calcular_v_carga(Q, dt, R, Vmax, c, T, True)
    elif ambos == "C":
        calcular_q_carga(Q, dt, R, Vmax, c, T, False)
        calcular_v_carga(Q, dt, R, Vmax, c, T, False)
    elif ambos == "D":
        calcular_q_descarga(Q, dt, R, c, T, 0)
        calcular_v_descarga(Q, dt, R, c, T, 0)


# if grafica == "V":              # Guardado del plot para V
#     fig2.savefig("Plot V MDLCC Tarea 6 FTEM.png")

# elif grafica == "Q":            # Guardado del plot para Q
#     fig1.savefig("Plot Q MDLCC Tarea 6 FTEM.png")

# elif grafica == "A":
#     fig1.savefig("Plot Q MDLCC Tarea 6 FTEM.png")
#     fig2.savefig("Plot V MDLCC Tarea 6 FTEM.png")

plt.show()
