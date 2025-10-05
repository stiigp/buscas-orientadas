from matriz import Matriz
from typing import List
import copy

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
mat = Matriz(copy.deepcopy(estadoFinal), estadoFinal, "A*", "quantidade_blocos_errados")
mat.user_embaralha()
mat.resolve()
