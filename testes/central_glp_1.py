

# dimensionamento de uma central de glp

# LÓGICA DO PROGRAMA
# potência computada vai ser um dicionário
# Equipamentos vão ser as chaves
# Um lista com 2 elementos será a potência e a quantidade desse equipamento
# potecia_computada = {equipamento1:[potencia,quantidade]}
class central_glp:
   def __init__(self):
      self.pot_computada = {}
      self.pot_qtde = []
      self.cilindros_tv = {'P-13': 0.6, 'P-45': 1, 'P-190': 3.5, 'P-500': 7, 'P-1000': 11, 'P-2000': 26, 'P-4000': 26}
      self.poder_calorifico = 24000
   def calcular_pot(self,equipamento,potencia,quantidade):
      self.pot_qtde = [potencia,quantidade]
      self.pot_computada[equipamento] = self.pot_qtde
      return self.pot_computada

   def pot_total(self):
      pot_total = 0
      for equipamento in self.pot_computada:
         pot_total += self.pot_computada[equipamento][0] * self.pot_computada[equipamento][1]
      return pot_total

   def fator_simultaneidade(self):
      if self.pot_total() <= 350:
         f = 1
      elif 350 < self.pot_total() > 350 < 9612:
         f = 100/(1 + 0.001*((self.pot_total() - 349))**(0.8712))
      elif 9612 <= self.pot_total() < 20000:
         f = 100/(1 + 0.4705*(self.pot_total() - 1055)**(0.19931))
      else:
         f = 23
      return f

   def vazao(self):
      vazao = self.calcular_pot() / self.poder_calorifico
      return vazao
   
   def tipo_cilindro(self):
      for cilindro in self.cilindros_tv:
         if self.vazao() <= self.cilindros_tv[cilindro]:
            return cilindro
      return 'Cilindro inválido'
   
   def num_cilindros(self):
      num_cilindros = self.vazao() * self.poder_calorifico / self.cilindros_tv[self.tipo_cilindro()]
      return num_cilindros

   def main(self):
      while True:
         while True:
            equipamento = input('Equipamento: ')
            potencia = float(input('Potência: '))
            quantidade = int(input('Quantidade: '))
            central.calcular_pot(equipamento,potencia,quantidade)
            opc = input('Deseja adicionar mais equipamentos? [S/N]')
            if opc in 'Nn':
               break
         print(central.pot_computada())
         print(f'Potência total: {central.pot_total()} W')
         print(f'Fator de simultaneidade: {central.fator_simultaneidade()}')
         print(f'Vazão: {central.vazao()} m3/h')
         tipo_cilindro = input('Tipo de cilindro: ')
         num_cilindros = central.num_cilindros()
         print(f'Quantidade de cilindros: {num_cilindros}')
         print('Deseja calcular novamente? [S/N]')
         if input() == 'N':
            break
if __name__ == '__main__':
   central = central_glp()
   central.main()