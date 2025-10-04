from typing import List, Tuple
from math import sqrt
import copy
import keyboard
import os
import time

class Matriz:
    def __init__(self, estadoAtual: List[List], estadoFinal: List[List], heuristica: str):
        self.estadoAtual = estadoAtual
        self.estadoFinal = estadoFinal
        if heuristica == "euclidiana":
            self.heuristica = self._dist_euclidiana
        elif heuristica == "manhattan":
            self.heuristica = self._dist_manhattan
        elif heuristica == "quantidade_blocos_errados":
            self.heuristica = self._item_esta_no_lugar_errado

    def _limpar_tela(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def _exibe_estado_atual(self):
        for linha in self.estadoAtual:
            for ele in linha:
                print(ele, end=" ")
            print()
        print()

    def _movimenta_matriz(self, movimento: Tuple):
        x, y = self._busca_no_estado(0, self.estadoAtual)
        par = (x, y)

        coord_troca = self._soma_pares(par, movimento)
        if not self._is_out_of_bounds(coord_troca):
            self.estadoAtual[y][x] = self.estadoAtual[coord_troca[1]][coord_troca[0]]
            self.estadoAtual[coord_troca[1]][coord_troca[0]] = 0

    def user_embaralha(self):
        
        while True:
            self._limpar_tela()
            print("Agora embaralhe você! Use as setas para movimentar o tabuleiro")
            print("Aperte esc quando tiver terminado de embaralhar.")
            self._exibe_estado_atual()

            tecla = keyboard.read_key()

            if tecla == "up":
                self._movimenta_matriz((0, 1))
                time.sleep(0.15)
            elif tecla == "down":
                self._movimenta_matriz((0, -1))
                time.sleep(0.15)
            elif tecla == "left":
                self._movimenta_matriz((1, 0))
                time.sleep(0.15)
            elif tecla == "right":
                self._movimenta_matriz((-1, 0))
                time.sleep(0.15)
            elif tecla == "esc":
                break

    def _busca_no_estado(self, itemBusca: int, estado: List[List]):
        for linha in estado:
            y = estado.index(linha)

            for item in linha:
                x = linha.index(item)

                if itemBusca == item:
                    return x, y

    def _dist_euclidiana(self, xI: int, yI: int, xF: int, yF: int)->int:
        return sqrt(pow(xF - xI, 2) + pow(yF - yI, 2))

    def _dist_manhattan(self, xI: int, yI: int, xF: int, yF: int)->int:
        return abs(xF - xI) + abs(yF - yI)
    
    def _item_esta_no_lugar_errado(self, xI: int, yI: int, xF: int, yF: int) -> int:
        return 0 if (xI == xF and yI == yF) else 1
    
    def _is_out_of_bounds(self, par: Tuple):
        return par[0] < 0 or par[0] > 2 or par[1] < 0 or par[1] > 2
    
    def _soma_pares(self, par: Tuple, par2: Tuple)->Tuple:
        assert len(par) == len(par2) == 2, "tentando somar tuplas de tamanho diferente de 2"

        return (par[0] + par2[0], par[1] + par2[1])

    def _calcula_heuristica(self, estado: List[List])->int:
        res = 0

        for linha in estado:
            yI = estado.index(linha)

            for item in linha:
                xI = linha.index(item)

                xF, yF = self._busca_no_estado(item, self.estadoFinal)
                res += self.heuristica(xI, yI, xF, yF)

        return res
    
    def _insere_ordenado_a_estrela(self, fila: List, estado_heuristica_nivel_caminho: Tuple):
        i = 0

        while i < len(fila) and fila[i][0] != estado_heuristica_nivel_caminho[0]:
            i += 1
        
        if i < len(fila) and fila[i][1] + fila[i][2] > estado_heuristica_nivel_caminho[1] + estado_heuristica_nivel_caminho[2]:
            fila[i] = estado_heuristica_nivel_caminho
            return
        
        if i == len(fila):
            i = 0

            while i < len(fila) and fila[i][1] + fila[i][2] <= estado_heuristica_nivel_caminho[1] + estado_heuristica_nivel_caminho[2]:
                i += 1

            fila.insert(i, estado_heuristica_nivel_caminho)
    
    def _gera_possibilidades_movimento(self)->List[List[List]]:

        x, y = self._busca_no_estado(0, self.estadoAtual)
        par = (x, y)
        res = []

        possibilidades = [(-1, 0), (0, -1), (1, 0), (0, 1)]

        for possibilidade in possibilidades:
            coord_troca = self._soma_pares(par, possibilidade)

            if not self._is_out_of_bounds(coord_troca):
                res_atual = copy.deepcopy(self.estadoAtual)

                res_atual[y][x] = res_atual[coord_troca[1]][coord_troca[0]]
                res_atual[coord_troca[1]][coord_troca[0]] = 0

                res.append(res_atual)
            
        return res
        
    def a_estrela(self)->List[List[List]]:
        fila = [(self.estadoAtual, self._calcula_heuristica(self.estadoAtual), 0, [self.estadoAtual])]

        res = [self.estadoAtual]

        while self.estadoAtual != self.estadoFinal:
            self.estadoAtual = fila[0][0]
            nivel_atual = fila[0][2]
            res = fila[0][3]
            fila.pop(0)

            for possibilidade in self._gera_possibilidades_movimento():
                self._insere_ordenado_a_estrela(fila, (possibilidade, self._calcula_heuristica(possibilidade), nivel_atual + 1, res+[possibilidade]))
        
        return res
    
    def _calcula_minimo_heuristica(self, possibilidades: List[List[List]])->List[List]:
        menor = possibilidades[0]
        for possibilidade in possibilidades[1:]:
            if self._calcula_heuristica(possibilidade) < self._calcula_heuristica(menor):
                menor = possibilidade

        return menor

    def hill_climbing(self) -> List[List[List]]:
        res = []

        while self.estadoAtual != self.estadoFinal:
            res.append(self.estadoAtual)

            possibilidades = self._gera_possibilidades_movimento()

            min_heuristica = self._calcula_minimo_heuristica(possibilidades)

            self.estadoAtual = min_heuristica
        
        res.append(self.estadoAtual)

        return res

    def _insere_ordenado_best_first(self, fila: List, estado_heuristica_caminho: Tuple):
        i = 0

        while i < len(fila) and fila[i][0] != estado_heuristica_caminho[0]:
            i += 1

        if i < len(fila) and fila[i][1] > estado_heuristica_caminho[1]:
            fila[i] = estado_heuristica_caminho
            return
        
        if i == len(fila):
            i = 0
            while i < len(fila) and fila[i][1] <= estado_heuristica_caminho[1]:
                i += 1
        
            fila.insert(i, estado_heuristica_caminho)

    def best_first(self) -> List[List[List]]:
        fila = [(self.estadoAtual, self._calcula_heuristica(self.estadoAtual), [self.estadoAtual])]

        # usando set pois é uma tabela hash e a busca funciona em O(1), ao contrário da List
        visited = set()

        res = [self.estadoAtual]

        while self.estadoAtual != self.estadoFinal:
            self.estadoAtual = fila[0][0]
            res = fila[0][2]
            fila.pop(0)

            # para adicionar em um set precisa ser hashable => transformar estado em tupla
            atualTupla = tuple(tuple(linha) for linha in self.estadoAtual)
            visited.add(atualTupla)

            for poss in self._gera_possibilidades_movimento():
                possTupla = tuple(tuple(linha) for linha in poss)
                if not possTupla in visited:
                    self._insere_ordenado_best_first(fila, (poss, self._calcula_heuristica(poss), res+[poss]))
        
        return res

    def _insere_ordenado_branch_and_bound(self, fila: List, estado_nivel: Tuple):
        i = 0
        while i < len(fila) and fila[i][1] <= estado_nivel[1]:
            i += 1
        
        fila.insert(i, estado_nivel)
    
    def branch_and_bound(self) -> List[List[List]]:
        fila = []
        res = []
        nivel_atual = 1
        
        while self.estadoAtual != self.estadoFinal:
            res.append(self.estadoAtual)

            possibilidades = self._gera_possibilidades_movimento()

            for poss in possibilidades:
                self._insere_ordenado_branch_and_bound(fila, (self.estadoAtual, nivel_atual + 1))
            
            self.estadoAtual = fila[0][0]
            nivel_atual = fila.pop(0)[1]

        res.append(self.estadoAtual)

        return res

    def _exibe_matriz(self, mat: List[List]):
        for linha in mat:
            for ele in linha:
                print(ele, end=" ")
            print()
        print()

    def resolve_a_estrela(self):
        res = self.a_estrela()

        self._exibe_estado_atual()
        self._exibe_matriz(self.estadoFinal)

        for mat in res:
            self._limpar_tela()
            print("Resolvendo...")

            self._exibe_matriz(mat)

            time.sleep(1.5)

    def resolve_best_first(self):
        res = self.best_first()

        self._exibe_estado_atual()
        self._exibe_matriz(self.estadoFinal)

        for mat in res:
            self._limpar_tela()
            print("Resolvendo...")

            self._exibe_matriz(mat)

            time.sleep(1.5)
