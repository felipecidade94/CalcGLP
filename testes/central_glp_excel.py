import pandas as pd
from datetime import datetime
import openpyxl

class CentralGLP: # Cálculo de centrais prediais de GLP
   def __init__(self):
      # Potencia computada é o somatório das potencias unitarias de cada equipento multiplicada pela quantidade de cada um
      # Ou seja, a potência computada é o nome que damos para a potência total
      self.__cilindros_tv = {'P-13': 0.6, 'P-45': 1, 'P-190': 3.5, 'P-500': 7, 'P-1000': 11, 'P-2000': 26, 'P-4000': 26}
      self.__poder_calorifico = 24000
      self.__desidade_relativa = 1.8
      self._pot_equipamentos = {}

   def quantidade_equipamento(self):
      return self._pot_equipamentos.values()[1]

   def pot_equipamento(self):
      return self._pot_equipamentos.values()[0]

   # Mostra os tipos de cilindros disponíveis para centrais de GLP
   def listar_cilindros(self):
      return list(self.__cilindros_tv.keys())

   def mostrar_cilindros(self): # Mostra os tipos de cilindros disponíveis para centrais de GLP
      for i in range (len(self.listar_cilindros())):
         print(f'{i+1} - {self.listar_cilindros()[i]}')

   # Adiciona um equipamento presente na edificação, com sua potência potência unitária e número de unidades presentes
   def add_equipamento(self,equipamento,potencia,quantidade):
      self._pot_equipamentos[equipamento] = [potencia,quantidade]
      return self._pot_equipamentos

   # Calcula a potência computada, ou seja, a potência total de todos os equipamentos instalados na edificação
   def pot_computada(self):
      pot_total = 0
      for equipamento in self._pot_equipamentos:
         pot_total += self._pot_equipamentos[equipamento][0] * self._pot_equipamentos[equipamento][1]
      return pot_total

   # Calcula o fator de simultaneidade
   def fator_simultaneidade(self):
      if self.pot_computada() <= 350:
         f = 1
      elif 350 < self.pot_computada() < 9612:
         f = 100/(1 + (0.001*((self.pot_computada() - 349))**(0.8712)))
      elif 9612 <= self.pot_computada() < 20000:
         f = 100/(1 + (0.4705*(self.pot_computada() - 1055)**(0.19931)))
      else:
         f = 23
      return f

   # Calcula a potência adotada
   def calcular_pot_adotada(self):
      pot_adotada = self.pot_computada() * 60 * self.fator_simultaneidade()/100
      return pot_adotada

   # Calcula a vazão
   def calcular_vazao(self):
      vazao = self.calcular_pot_adotada() / self.__poder_calorifico
      return vazao

   # Calcula a quantidade de cilindros necessários
   def num_cilindros(self, tipo_cilindro):
      num_cilindros = self.calcular_vazao() * self.__desidade_relativa / self.__cilindros_tv[tipo_cilindro]
      return f'{round(num_cilindros)} {tipo_cilindro}'

   # Mostra os equipamentos adicionados
   def mostrar_equipamentos(self):
      print(f'{"Nº":<3} {"Equipamento":<25} {"Potência unitária (kcal/min)":<30} {"Quantidade (unid)":<20} {"Potência total (kcal/min)":<30}')
      print('-' * 115)
      for i in range(len(self._pot_equipamentos)):
         nome = list(self._pot_equipamentos.keys())[i]
         pot_unit = list(self._pot_equipamentos.values())[i][0]
         qtd = list(self._pot_equipamentos.values())[i][1]
         pot_total = pot_unit * qtd
         print(f'{i+1:<3} {nome:<25} {pot_unit:<30.2f} {qtd:<20} {pot_total:<30.2f}')
         #print(f'{i+1} - {list(self._pot_equipamentos.keys())[i]} - Potência unitária: {self._pot_equipamentos.values()[i][0]} kcal/min - {self.quantidade_equipamento()} unidade(s) - Potência total: {list(self._pot_equipamentos.values())[i][0] * list(self._pot_equipamentos.values())[i][1]} kcal/min')

   # Limpa os dados
   def limpa_dados(self):
      self._pot_equipamentos.clear()
      
   def gerar_memorial_de_calculo(self, tipo_cilindro): # Precisa de Reparo
      print('Gerando memorial de cálculo...\n')

      # Seção: Equipamentos
      print('Equipamentos:')
      print(f'{"Nº":<3} {"Equipamento":<25} {"Potência unitária (kcal/min)":<30} {"Quantidade (unid)":<20} {"Potência total (kcal/min)":<30}')
      print('-' * 115)
      for i in range(len(self._pot_equipamentos)):
         nome = list(self._pot_equipamentos.keys())[i]
         pot_unit = list(self._pot_equipamentos.values())[i][0]
         qtd = list(self._pot_equipamentos.values())[i][1]
         pot_total = pot_unit * qtd
         print(f'{i+1:<3} {nome:<25} {pot_unit:<30.2f} {qtd:<20} {pot_total:<30.2f}')
      # Seção: Resumo do Cálculo
      print('\nResumo do cálculo:')
      print(f'{"Potência total (Kcal/h):":40}{self.pot_computada() * 60:.2f}')
      print(f'{"Fator de simultaneidade:":40}{self.fator_simultaneidade():.2f}')
      print(f'{"Potência adotada (Kcal/h):":40}{self.calcular_pot_adotada():.2f}')
      print(f'{"Vazão (m³/h):":40}{self.calcular_vazao():.2f}')
      print(f'{"Cilindro (unidade(s)):":40}{self.num_cilindros(tipo_cilindro)}')

   def exportar_para_excel(self, tipo_cilindro):
      # Criar um DataFrame para os equipamentos
      equipamentos_data = []
      for i in range(len(self._pot_equipamentos)):
         nome = list(self._pot_equipamentos.keys())[i]
         pot_unit = list(self._pot_equipamentos.values())[i][0]
         qtd = list(self._pot_equipamentos.values())[i][1]
         pot_total = pot_unit * qtd
         equipamentos_data.append({
            'Nº': i+1,
            'Equipamento': nome,
            'Potência unitária (kcal/min)': pot_unit,
            'Quantidade (unid)': qtd,
            'Potência total (kcal/min)': pot_total
         })
      
      df_equipamentos = pd.DataFrame(equipamentos_data)

      # Calcular o número de cilindros
      num_cilindros = self.calcular_vazao() * self.__desidade_relativa / self.__cilindros_tv[tipo_cilindro]
      num_cilindros_arredondado = round(num_cilindros)

      # Criar um DataFrame para o resumo
      resumo_data = {
         'Item': [
            'Potência total (Kcal/h)',
            'Fator de simultaneidade',
            'Potência adotada (Kcal/h)',
            'Vazão (m³/h)',
            'Tipo de Cilindro',
            'Capacidade do Cilindro (kg/h)',
            'Número de Cilindros (calculado)',
            'Número de Cilindros (adotado)',
         ],
         'Valor': [
            self.pot_computada() * 60,
            self.fator_simultaneidade(),
            self.calcular_pot_adotada(),
            self.calcular_vazao(),
            tipo_cilindro,
            self.__cilindros_tv[tipo_cilindro],
            num_cilindros,
            num_cilindros_arredondado,
         ]
      }
      df_resumo = pd.DataFrame(resumo_data)

      # Criar o nome do arquivo com timestamp
      timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
      nome_arquivo = input('Digite o nome do arquivo: ')

      filename = f'{nome_arquivo}_{timestamp}.xlsx'

      # Criar o arquivo Excel com múltiplas abas
      with pd.ExcelWriter(filename, engine='openpyxl') as writer:
         df_equipamentos.to_excel(writer, sheet_name='Equipamentos', index=False)
         df_resumo.to_excel(writer, sheet_name='Resumo', index=False)

      print(f'\nArquivo Excel gerado com sucesso: {filename}')

   # Função principal
   def main(self):
      while True:
         cont = 0
         print('Adione os equipamentos presentes na edificação:')
         while True:
            equipamento = input(f'Adione o {cont+1}º equipamento: ')
            potencia = float(input(f'Adione a potência de {cont + 1}º equipamento: [Kcal/min] '))
            quantidade = int(input(f'Adione a quantidade do {cont + 1}º equipamento: '))
            self.add_equipamento(equipamento,potencia,quantidade)
            cont += 1
            opc = input('Deseja adicionar mais equipamentos? [S/N] ')
            if opc in 'Nn':
               self.mostrar_equipamentos()
               check = input('Confirmar? [S/N] ')
               if check in 'Ss':
                  break
               else:
                  self.limpa_dados()
                  return self.main()
         print(f'Potência total: {self.pot_computada()*60} Kcal/h')
         print(f'Vazão: {self.calcular_vazao():.2f} m³/h')
         self.mostrar_cilindros()
         cilindro = int(input('Escolha o tipo de cilindro: '))
         if cilindro <= (len(self.listar_cilindros()) - 1):
            self.listar_cilindros()[cilindro - 1]
            self.num_cilindros(self.listar_cilindros()[cilindro - 1])
         else:
            print('Cilindro inválido')
         opc = input('Deseja calcular novamente? [S/N]')
         if opc in 'Nn':
            opc = input('Deseja exportar para excel? [S/N]')
            self.gerar_memorial_de_calculo(self.listar_cilindros()[cilindro - 1])
            if opc in 'Ss':
               self.exportar_para_excel(self.listar_cilindros()[cilindro - 1])
            self.limpa_dados()
            break
         else:
            return self.main()


if __name__ == '__main__':
   central = CentralGLP()
   central.main() 