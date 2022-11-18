from gurobipy import Model, GRB, quicksum

#las casas 
I = range(1,6)
#las personas
J = {"Hermione", "Ron", "Ginny", "Neville", "Hagrid"}
#las bebidas 
K = {"te", "vino de sauco", "chocolate caliente", "cerveza de mantequilla", "zumo de calabaza"}
#las varitas
L = {"sauco", "acebo", "pino", "sauce", "alamo"}
#los hechizos
M = {"alohomora", "lumos", "accio", "expecto patronum", "avada kedabra"}
#las casas de magia
N = {"Gryffindor", "Hufflepuff", "Ravenclaw", "Slytherin", "Muggle"}


#### ESCRIBA SU MODELO AQUI ####
modelo = Model()
modelo.setParam("TimeLimit", 30)


###################
##  Variables:   ##
###################
# Función binaria con valor 1 si es que la combinación es correcta y 0 en otro caso
# Tal que x[i, j, k, l, m, n]
x = modelo.addVars(I, J, K, L, M, N, vtype = GRB.BINARY, name = "x")


###########################
##  Función Objetivo:    ##
###########################
funcion_objetivo = quicksum(x[i, j, k, l, m, "Muggle"] for i in I for j in J for k in K for l in L for m in M)
modelo.setObjective(funcion_objetivo, GRB.MINIMIZE)


#######################
##  Restricciones:   ##
#######################

# Codigo base de restricciones:
# modelo.addConstr(x[i, j, k, l, m, n] == 0 for i in I for j in J for k in K for l in L for m in M
#                  for n in N if .....)


# R1: Hermione tiene la varita de Álamo
modelo.addConstrs(x[i, "Hermione", k, l, m, n] == 0
                  for i in I for k in K for l in L for m in M for n in N if l != "alamo")

modelo.addConstrs(x[i, j, k, "alamo", m, n] == 0
                  for i in I for j in J for k in K for m in M for n in N if j != "Hermione")

# R2: La casa favorita de Ron es Gryffindor
modelo.addConstrs(x[i, "Ron", k, l, m, n] == 0
                  for i in I for k in K for l in L for m in M for n in N if n != "Gryffindor")

modelo.addConstrs(x[i, j, k, l, m, "Gryffindor"] == 0
                  for i in I for j in J for k in K for l in L for m in M if j != "Ron")

# R3: Ginny toma Té
modelo.addConstrs(x[i, "Ginny", k, l, m, n] == 0
                  for i in I for k in K for l in L for m in M for n in N if k != "te")

modelo.addConstrs(x[i, j, "te", l, m, n] == 0
                  for i in I for j in J for l in L for m in M for n in N if j != "Ginny")

# R4: Hagrid vive en la Primera Casa
modelo.addConstrs(x[i, "Hagrid", k, l, m, n] == 0
                  for i in I for k in K for l in L for m in M for n in N if i != 1)

modelo.addConstrs(x[1, j, k, l, m, n] == 0
                  for j in J for k in K for l in L for m in M for n in N if j != "Hagrid")

# R5: El hechizo favorito de Neville es Alohomora
modelo.addConstrs(x[i, "Neville", k, l, m, n] == 0
                  for i in I  for k in K for l in L for m in M for n in N if m != "alohomora")

modelo.addConstrs(x[i, j, k, l, "alohomora", n] == 0
                  for i in I for j in J for k in K for l in L for n in N if j != "Neville")

# R6: La varita de Saúco está a la izquierda (a distancia 1) de la varita de Pino
modelo.addConstrs(quicksum(x[i - 1, j, k, "sauco", m, n] - x[i, j, k, "pino", m, n]
                   for j in J for k in K for m in M for n in N) == 0 for i in range(2,6))

# R7: Quien tiene la varita de Sauco toma Vino de Sauco
modelo.addConstrs(x[i, j, k, "sauco", m, n] == 0      
                  for i in I for j in J for k in K for m in M for n in N if k != "vino de sauco")

modelo.addConstrs(x[i, j, "vino de sauco", l, m, n] == 0
                  for i in I for j in J for l in L for m in M for n in N if l != "sauco")

# R8: El hechizo favorito de la persona que más le gusta Hufflepuff es Lumos.
modelo.addConstrs(x[i, j, k, l, m, "Hufflepuff"] == 0
                  for i in I for j in J for k in K for l in L for m in M if m != "lumos")

modelo.addConstrs(x[i, j, k, l, "lumos", n] == 0
                  for i in I for j in J for k in K for l in L for n in N if n != "Hufflepuff")

# R9: Quien tiene la varita de Acebo le gusta el hechizo Accio.
modelo.addConstrs(x[i, j, k, "acebo", m, n] == 0
                  for i in I for j in J for k in K for m in M for n in N if m != "accio")

modelo.addConstrs(x[i, j, k, l, "accio", n] == 0
                  for i in I for j in J for k in K for l in L for n in N if l != "acebo")

# R10: La persona que vive en la 3ra casa toma chocolate caliente
modelo.addConstrs(x[3, j, k, l, m, n] == 0
                  for j in J for k in K for l in L for m in M for n in N if k != "chocolate caliente")

modelo.addConstrs(x[i, j, "chocolate caliente", l, m, n] == 0
                  for i in I for j in J for l in L for m in M for n in N if i != 3)

# R11: Quien tiene por favorito Expecto Patronum es vecino de a quien le gusta Ravenclaw
modelo.addConstrs(quicksum(x[i, j, k, l, "expecto patronum", n]
                  for j in J for k in K for l in L for n in N) <=
                  quicksum(x[i+1, j, k, l, m, "Ravenclaw"] + x[i-1, j, k, l, m, "Ravenclaw"]
                  for j in J for k in K for l in L for m in M) for i in range(2,5))

modelo.addConstr(quicksum(x[1, j, k, l, "expecto patronum", n]
                  for j in J for k in K for l in L for n in N) == quicksum(x[2, j, k, l, m, "Ravenclaw"]
                  for j in J for k in K for l in L for m in M))

modelo.addConstr(quicksum(x[5, j, k, l, "expecto patronum", n]
                  for j in J for k in K for l in L for n in N) == quicksum(x[4, j, k, l, m, "Ravenclaw"]
                  for j in J for k in K for l in L for m in M))


# R12: A quien le gusta Slytherin tiene por vecino a quien le gusta Accio
modelo.addConstrs(quicksum(x[i, j, k, l, m, "Slytherin"]
                  for j in J for k in K for l in L for m in M) <=
                  quicksum(x[i+1, j, k, l, "accio", n] + x[i-1, j, k, l, "accio", n]
                  for j in J for k in K for l in L for n in N) for i in range(2,5))

modelo.addConstr(quicksum(x[1, j, k, l, m, "Slytherin"]
                  for j in J for k in K for l in L for m in M) == quicksum(x[2, j, k, l, "accio", n]
                  for j in J for k in K for l in L for n in N))

modelo.addConstr(quicksum(x[5, j, k, l, m, "Slytherin"]
                  for j in J for k in K for l in L for m in M) == quicksum(x[4, j, k, l, "accio", n]
                  for j in J for k in K for l in L for n in N))

# R13: EL hechizo favorito de quien bebe Cerveza de mantequilla es Avada Kedabra
modelo.addConstrs(x[i, j, "cerveza de mantequilla", l, m, n] == 0 for i in I for j in J for l in L
                  for m in M for n in N if m != "avada kedabra")

modelo.addConstrs(x[i, j, k, l, "avada kedabra", n] == 0 for i in I for j in J for k in K for l in L
                  for n in N if k != "cerveza de mantequilla")

# R14: Quien toma Zumo de Calabaza y quien tiene por hechizo favorito Expecto Patronum son vecinos
modelo.addConstrs(quicksum(x[i, j, "zumo de calabaza", l, m, n]
                  for j in J for l in L for m in M for n in N) <=
                  quicksum(x[i+1, j, k, l, "expecto patronum", n] + x[i-1, j, k, l, "expecto patronum", n]
                  for j in J for k in K for l in L for n in N) for i in range(2,5))

modelo.addConstr(quicksum(x[1, j, "zumo de calabaza", l, m, n]
                  for j in J for l in L for m in M for n in N) == quicksum(x[2, j, k, l, "expecto patronum", n]
                  for j in J for k in K for l in L for n in N))

modelo.addConstr(quicksum(x[5, j, "zumo de calabaza", l, m, n]
                  for j in J for l in L for m in M for n in N) == quicksum(x[4, j, k, l, "expecto patronum", n]
                  for j in J for k in K for l in L for n in N))

# R15: Hagrid Vive al lado de quien tiene la varita de sauce
modelo.addConstrs(quicksum(x[i, "Hagrid", k, l, m, n] for k in K for l in L for m in M for n in N) ==
                  quicksum(x[i+1, j, k, "sauce", m, n] for j in J for k in K for m in M for n in N)
                  for i in range(1,5))

# R16: La variable no puede ser 1 si es que alguno de los subindices coincide
#      con una combinacion que haya arrojado por valor 1 (no se puede repetir ningun atributo)
modelo.addConstrs(quicksum(x[i, j, k, l, m, n] for i in I for j in J for k in K for l in L
                  for m in M) == 1 for n in N)          # Para todas las casas de magia
                 
modelo.addConstrs(quicksum(x[i, j, k, l, m, n] for i in I for j in J for k in K for l in L
                  for n in N) == 1 for m in M)          # Para todos los hechizos

modelo.addConstrs(quicksum(x[i, j, k, l, m, n] for i in I for j in J for k in K for m in M
                  for n in N) == 1 for l in L)           # Para todas las varitas

modelo.addConstrs(quicksum(x[i, j, k, l, m, n] for i in I for j in J for l in L for m in M
                  for n in N) == 1 for k in K)           # para todas las bebidas

modelo.addConstrs(quicksum(x[i, j, k, l, m, n] for i in I for k in K for l in L for m in M
                  for n in N) == 1 for j in J)           # Para todos los personajes

modelo.addConstrs(quicksum(x[i, j, k, l, m, n] for j in J for k in K for l in L for m in M
                  for n in N) == 1 for i in I)           # Para todas las casas

# R17: Que la suma de las combinaciones sea igual a 5:
modelo.addConstr(quicksum(x[i, j, k, l, m, n] for i in I for j in J for k in K for l in L
                  for m in M for n in N) == 5)


# Que se actualice y comience el programa:
modelo.update()
modelo.optimize()

# Soluciones:
modelo.printAttr("x")
