import tkinter as tk
from tkinter import Tk, Label, ttk, messagebox, simpledialog, Entry, Button, Toplevel
from central_glp_excel import CentralGLP
from PIL import ImageTk, Image

class CalcGLP(): # Cálculo de centrais prediais de GLP
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

   def interface_principal(self):
      style = ttk.Style()
      style.configure('TButton',  padding=1, font=("Arial", 15), foreground="black", background='#add8e6')
      style.configure('TLabel',  padding=10, font=('Arial', 20, 'bold'))
      self.janela_principal.title('CalcGLP')
      self.janela_principal.geometry('400x400')
      img_calcular = Image.open('./img/calcular.png')
      img_calcular = img_calcular.resize((120,60))
      self.img_calcular = ImageTk.PhotoImage(img_calcular)
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
      ttk.Button(frame, image=self.img_calcular, style = 'TButton', command=self.interface_secundaria).grid(row = 1, column = 0, columnspan = 1, padx =0, pady = 0)
      ttk.Button(frame, image= self.img_sair, style='TButton', command=self.sair_programa).grid(row = 2, column = 0, columnspan = 1, padx =0, pady = 0)

   def interface_secundaria(self):
      self.janela_principal.withdraw()
      self.janela_secundaria = Toplevel(self.janela_principal)
      self.janela_secundaria.title('Dados')
      self.janela_secundaria.geometry('400x350')
      style = ttk.Style()
      style.configure('TButton', padding=1, font=("Arial", 15), foreground="black", background='#add8e6')
      style.configure('TLabel', padding=10, font=('Arial', 20, 'bold'))
      frame = ttk.Frame(self.janela_secundaria)
      frame.pack(padx=20, pady=20)
      ttk.Button(frame, text='Adionar equipamento', style='TButton', width=25, command=self.abrir_add_eqpto).grid(row=1, column=0, padx=5, pady=5)
      ttk.Button(frame, text='Listar equipamentos', style='TButton', width=25).grid(row=2, column=0, padx=5, pady=5)
      ttk.Button(frame, text='Editar dados', style='TButton', width=25).grid(row=3, column=0, padx=5, pady=5)
      ttk.Button(frame, text='Ecolher tamanho do cilindro', style='TButton', width=25).grid(row=4, column=0, padx=5, pady=5)
      ttk.Button(frame, text='Visualizar prévia do memorial', style='TButton', width=25).grid(row=5, column=0, padx=5, pady=5)      
      ttk.Button(frame, text='Exportar memorial', style='TButton', width=25).grid(row=6, column=0, padx=5, pady=5)
      ttk.Button(frame, text='Voltar a página inicial', style='TButton', width=25, command=self.voltar_inicial).grid(row=7, column=0, padx=5, pady=5)

   def voltar_inicial(self):
      self.janela_secundaria.destroy()
      self.janela_principal.deiconify()

   def abrir_add_eqpto(self):
      self.nova_janela = Toplevel(self.janela_secundaria)
      self.nova_janela.title('Adicionar Equipamentos')
      self.nova_janela.geometry('400x300')
      self.widgets_add_eqpto(self.nova_janela)
      
   def voltar_secundaria(self):
      self.nova_janela.destroy()
      self.janela_secundaria.deiconify()
   
   def widgets_add_eqpto(self, janela):
      self.janela_secundaria.withdraw()
      style = ttk.Style()
      style.configure(style='TButton',  padding=1, font=("Arial", 15), foreground="black", background='#add8e6')
      style.configure(style='TLabel',  padding=10, font=('Arial', 20, 'bold'))
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
      frame = ttk.Frame(janela)
      frame.pack(padx=20, pady=20)
      ttk.Button(frame, text='Adionar', style='TButton', width=25).grid(row=1, column=0, padx=5, pady=5)
      ttk.Button(frame, text='Voltar', style='TButton', width=25, command=self.voltar_secundaria).grid(row=2, column=0, padx=5, pady=5)

   def sair_programa(self):
      sair = messagebox.askyesno(title='Sair', message= 'Tem certeza que deseja sair?')
      if sair:
         self.janela_principal.destroy()

if __name__ == '__main__':
   CalcGLP()
