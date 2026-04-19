from dataclasses import dataclass


@dataclass
class Parede:
    comprimento: float
    altura: float
    espessura: float

    def area(self):
        return self.comprimento * self.altura

    def volume(self):
        return self.area() * self.espessura


class MotorCalculo:
    def __init__(self):
        self.regras = []

    def adicionar_regra(self, regra):
        self.regras.append(regra)

    def executar(self, entidades):
        resultados = []
        for entidade in entidades:
            for regra in self.regras:
                if regra.aplica(entidade):
                    resultados.append(regra.calcular(entidade))
        return resultados


class Calculadora:

    def calcular_area_parede(self, parede: Parede):
        return parede.comprimento * parede.altura

    def calcular_volume_concreto(self, parede: Parede):
        return parede.volume()


class RegraCalculo:
    def calcular(self, entidade):
        raise NotImplementedError


class CalculoAreaParede(RegraCalculo):
    def calcular(self, entidade: Parede):
        return entidade.comprimento * entidade.altura
