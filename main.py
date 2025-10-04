from matriz import Matriz
from typing import List
import copy

mat = Matriz([[1, 2, 3], [0, 4, 5], [6, 7, 8]], [[2, 3, 5], [1, 4, 0], [6, 7, 8]], "euclidiana")
poss = mat.best_first()

def exibe_matriz(mat: List[List]):
    for linha in mat:
        for ele in linha:
            print(ele, end=" ")
        print()
    print()

def recebeEstadoFinalUsuario()->List:
    res = [[],[],[]]
    entrada_str = input("Digite o estado final desejado em formato linear (e.g: 145023867)")
    for char in entrada_str[0:3]:
        res[0].append(int(char))
    for char in entrada_str[3:6]:
        res[1].append(int(char))
    for char in entrada_str[6:]:
        res[2].append(int(char))
    
    return res

estadoFinal = recebeEstadoFinalUsuario()
mat = Matriz(copy.deepcopy(estadoFinal), estadoFinal, "quantidade_blocos_errados")
mat.user_embaralha()
mat.resolve_best_first()
