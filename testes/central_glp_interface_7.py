import tkinter as tk
from tkinter import Tk, Label, ttk, messagebox, simpledialog, Entry, Button, Toplevel
from PIL import ImageTk, Image
import openpyxl
import pandas as pd
from datetime import datetime
import os

class CentralGLP(): # Cálculo de centrais prediais de GLP
   def __init__(self):
      # Potencia computada é o somatório das potencias unitarias de cada equipento multiplicada pela quantidade de cada um
      # Ou seja, a potência computada é o nome que damos para a potência total
      self.__cilindros_tv = {'P-13': 0.6, 'P-45': 1, 'P-190': 3.5, 'P-500': 7, 'P-1000': 11, 'P-2000': 26, 'P-4000': 26}
      self.__poder_calorifico = 24000
      self.__desidade_relativa = 1.8
      self._pot_equipamentos = {}
      self.janela_principal = Tk()
      self.interface_principal()
      self.janela_principal.mainloop()

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
      return f'{round(num_cilindros)} cilindros tipo {tipo_cilindro}'

   def mostrar_equipamentos(self):
      print(f'{"Nº":<3} {"Equipamento":<25} {"Potência unitária (kcal/min)":<30} {"Quantidade (unid)":<20} {"Potência total (kcal/min)":<30}')
      print('-' * 115)
      for i in range(len(self._pot_equipamentos)):
         nome = list(self._pot_equipamentos.keys())[i]
         pot_unit = list(self._pot_equipamentos.values())[i][0]
         qtd = list(self._pot_equipamentos.values())[i][1]
         pot_total = pot_unit * qtd
         print(f'{i+1:<3} {nome:<25} {pot_unit:<30.2f} {qtd:<20} {pot_total:<30.2f}')

   def previa_memorial(self):
      tipo_cilindro = self.combo_tipos.get()
      resumo = f'''
   Resumo do Cálculo
   Potência total: {self.pot_computada() * 60:.2f} Kcal/h
   Fator de simultaneidade: {self.fator_simultaneidade():.2f}
   Potência adotada: {self.calcular_pot_adotada():.2f} Kcal/h
   Vazão: {self.calcular_vazao():.2f} m³/h
   Cilindros: {self.num_cilindros(tipo_cilindro)}
   '''
      messagebox.showinfo('Prévia do Memorial', resumo)

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
   
   def interface_principal(self):
      style = ttk.Style()
      style.configure('TButton',  padding=1, font=("Arial", 15), foreground="black", background='#add8e6')
      style.configure('TLabel',  padding=10, font=('Arial', 20, 'bold'))
      self.janela_principal.title('CalcGLP')
      self.janela_principal.geometry('400x600')
      img_calcular = Image.open('./img/calcular.png')
      img_calcular = img_calcular.resize((120,60))
      self.img_calcular = ImageTk.PhotoImage(img_calcular)
      img_previa = Image.open('./img/previa.png')
      img_previa = img_previa.resize((120,60))
      self.img_previa = ImageTk.PhotoImage(img_previa)
      img_exportar = Image.open('./img/exportar.png')
      img_exportar = img_exportar.resize((120,60))
      self.img_exportar = ImageTk.PhotoImage(img_exportar)      
      img_editar = Image.open('./img/editar.png')
      img_editar = img_editar.resize((120,60))
      self.img_editar = ImageTk.PhotoImage(img_editar)      
      img_sair = Image.open('./img/sair.png')      
      img_sair = img_sair.resize((120,60))
      self.img_sair = ImageTk.PhotoImage(img_sair)
      logo = Image.open('./img/logo.png')
      logo = logo.resize((200,200))
      self.logo_imagem = ImageTk.PhotoImage(logo)
      logo_label = Label(self.janela_principal, image=self.logo_imagem)
      logo_label.pack()
      frame = ttk.Frame(self.janela_principal)
      frame.pack(padx=0, pady=0)
      ttk.Button(frame, image=self.img_calcular, style = 'TButton', command=self.abrir_calcular).grid(row = 1, column = 0, columnspan = 1, padx =0, pady = 0)
      ttk.Button(frame, image=self.img_editar, style='TButton', width=25).grid(row=2, column=0, padx=5, pady=5)
      ttk.Button(frame, image=self.img_previa, style='TButton', width=25, command=self.previa_memorial).grid(row=3, column=0, padx=5, pady=5)
      ttk.Button(frame, image=self.img_exportar, style='TButton', width=25, command=self.abrir_exportar).grid(row=4, column=0, padx=5, pady=5)
      ttk.Button(frame, image= self.img_sair, style='TButton', command=self.sair_programa).grid(row = 5, column = 0, columnspan = 1, padx =0, pady = 0)

   def abrir_calcular(self):
      self.janela_principal.withdraw()
      self.nova_janela = Toplevel(self.janela_principal)
      self.nova_janela.geometry('400x400')
      self.widgets_calcular(self.nova_janela)
      
   def widgets_calcular(self, janela):
      lista_tipos = [tipo for tipo in self.__cilindros_tv.keys()]
      style = ttk.Style()
      style.configure(style='TButton',  padding=1, font=("Arial", 15), foreground="black", background='#add8e6')
      style.configure(style='TLabel',  padding=10, font=('Arial', 20, 'bold'))
      label_add = Label(janela, text='Adicionar Equipamentos', font=('Arial',15,'bold'))
      label_add.pack()
      label_eqpto = Label(janela, text='Equipamento', font=('Arial',10,'bold'))
      label_eqpto.pack()
      self.entry_add_eqto = Entry(janela)
      self.entry_add_eqto.pack(padx=5, pady=5, fill=tk.X)
      label_pot = Label(janela, text='Potência unitária [kcal/min]', font=('Arial',10,'bold'))
      label_pot.pack()
      self.entry_pot = Entry(janela)
      self.entry_pot.pack(padx=5, pady=5, fill=tk.X)
      label_qtde = Label(janela, text='Quantidade', font=('Arial',10,'bold'))
      label_qtde.pack()
      self.entry_qtde = Entry(janela)
      self.entry_qtde.pack(padx=5, pady=5, fill=tk.X)
      frame_add = ttk.Frame(janela)
      frame_add.pack()
      ttk.Button(frame_add, text='Adionar', style='TButton', width=12, command=self.adcionar).grid(row=1, column=0, padx=0, pady=5)
      ttk.Button(frame_add, text='Limpar', style='TButton', width=12, command=self.limpar).grid(row=1, column=1, padx=0, pady=5)
      label_tipo = Label(janela, text='Tipo de Cilíndro',font=('Arial',15,'bold'))
      label_tipo.pack()
      frame_tipo = ttk.Frame(janela)
      frame_tipo.pack()
      self.combo_tipos = ttk.Combobox(frame_tipo, values=lista_tipos, width=30)
      self.combo_tipos.pack()
      frame_concluir = ttk.Frame(janela)
      frame_concluir.pack()
      ttk.Button(frame_concluir, text='Calcular', style='TButton', width=25, command=self.calcular).grid(row=2, column=0, padx=5, pady=5)
      frame_voltar = ttk.Frame(janela)
      frame_voltar.pack()
      ttk.Button(frame_voltar, text='Voltar', style='TButton', width=25, command=self.voltar_inicial).grid(row=3, column=0, padx=5, pady=5)

   def adcionar(self):
      eqpto = self.entry_add_eqto.get()
      pot = self.entry_pot.get().replace(',','.')
      qtde = self.entry_qtde.get()
      if not (eqpto and pot and qtde):
         msg = 'Todos os campos devem ser preenchidos'
         messagebox.showerror('ERRO!',msg)
      else:
         try:
            self.add_equipamento(eqpto, float(pot), int(qtde))
         except ValueError:
            msg = 'Valores inválidos!'
            messagebox.showerror('ERRO!',msg)
         else:
            self.mostrar_equipamentos()
            self.entry_add_eqto.delete(0, tk.END)
            self.entry_pot.delete(0, tk.END)
            self.entry_qtde.delete(0, tk.END)

   def limpar(self):
      self.entry_add_eqto.delete(0, tk.END)
      self.entry_pot.delete(0, tk.END)
      self.entry_qtde.delete(0, tk.END)

   def calcular(self):
      tipo = self.combo_tipos.get()
      if not tipo:
         msg = 'Todos os campos devem ser preenchidos'
         messagebox.showerror('ERRO!',msg)
         return
      self.num_cilindros(tipo)
      self.gerar_memorial_de_calculo(tipo)
   
   def voltar_inicial(self):
      self.nova_janela.withdraw()
      self.janela_principal.deiconify()
   
   def voltar_calcular(self):
      self.janela_principal.withdraw()
      self.nova_janela = Toplevel(self.janela_principal)
      self.nova_janela.geometry('400x400')
      self.widgets_calcular(self.nova_janela)
   
   def abrir_exportar(self):
      self.janela_principal.withdraw()
      self.nova_janela = Toplevel(self.janela_principal)
      self.nova_janela.geometry('400x400')
      self.widgets_exportar(self.nova_janela)
   
   def widgets_exportar(self, janela):
      style = ttk.Style()
      style.configure('TButton',  padding=1, font=("Arial", 15), foreground="black", background='#add8e6')
      label_nome_arquivo = Label(janela, text='Informe o nome do arquivo', font=('Arial',15,'bold'))
      label_nome_arquivo.pack()
      self.entry_nome_arquivo = Entry(janela)
      self.entry_nome_arquivo.pack(padx=5, pady=5, fill=tk.X)
      frame_exportar = ttk.Frame(janela)
      frame_exportar.pack()
      ttk.Button(frame_exportar, text='Exportar', style='TButton', width=25, command=self.exportar_para_excel).grid(row=2, column=0, padx=5, pady=5)
      ttk.Button(frame_exportar, text='Voltar para tela de cálculo', style='TButton', width=25, command=self.voltar_calcular).grid(row=3, column=0, padx=5, pady=5)
      ttk.Button(frame_exportar, text='Voltar para tela incial', style='TButton', width=25, command=self.voltar_inicial).grid(row=4, column=0, padx=5, pady=5)

   def exportar_para_excel(self):
      # Criar um DataFrame para os equipamentos
      tipo_cilindro = self.combo_tipos.get()
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
      nome_arquivo = self.entry_nome_arquivo.get()
      if not nome_arquivo:
         messagebox.showerror('ERRO!', 'Nome do arquivo não pode ser vazio!')
         return
      filename = f'{nome_arquivo}_{timestamp}.xlsx'

      # Criar o arquivo Excel com múltiplas abas
      with pd.ExcelWriter(filename, engine='openpyxl') as writer:
         df_equipamentos.to_excel(writer, sheet_name='Equipamentos', index=False)
         df_resumo.to_excel(writer, sheet_name='Resumo', index=False)

      messagebox.showinfo('SUCESSO!', f'Arquivo {filename} gerado com sucesso!')
      # Exibir mensagem de sucesso
         
   def sair_programa(self):
      sair = messagebox.askyesno(title='Sair', message= 'Tem certeza que deseja sair?')
      if sair:
         self.janela_principal.destroy()

if __name__ == '__main__':
   CentralGLP()