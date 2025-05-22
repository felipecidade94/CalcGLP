import tkinter as tk
from tkinter import Tk, Label, ttk, messagebox, simpledialog, Entry, Button, Toplevel
from central_glp_excel import CentralGLP
from PIL import ImageTk, Image

class central_glp_interface(): # Cálculo de centrais prediais de GLP
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
      ttk.Button(frame, image=self.img_previa, style='TButton', width=25).grid(row=3, column=0, padx=5, pady=5)
      ttk.Button(frame, image=self.img_exportar, style='TButton', width=25).grid(row=4, column=0, padx=5, pady=5)
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
      ttk.Button(frame_add, text='Adionar', style='TButton', width=25).grid(row=1, column=0, padx=5, pady=5)
      label_tipo = Label(janela, text='Tipo de Cilíndro',font=('Arial',15,'bold'))
      label_tipo.pack()
      frame_tipo = ttk.Frame(janela)
      frame_tipo.pack()
      self.combo_tipos = ttk.Combobox(frame_tipo, values=lista_tipos, width=30)
      self.combo_tipos.pack()
      frame_concluir = ttk.Frame(janela)
      frame_concluir.pack()
      ttk.Button(frame_concluir, text='Concluir', style='TButton', width=25).grid(row=2, column=0, padx=5, pady=5)
      frame_voltar = ttk.Frame(janela)
      frame_voltar.pack()
      ttk.Button(frame_voltar, text='Voltar', style='TButton', width=25, command=self.voltar_inicial).grid(row=3, column=0, padx=5, pady=5)

   def voltar_inicial(self):
      self.nova_janela.destroy()
      self.janela_principal.deiconify()
   
   def sair_programa(self):
      sair = messagebox.askyesno(title='Sair', message= 'Tem certeza que deseja sair?')
      if sair:
         self.janela_principal.destroy()

if __name__ == '__main__':
   central_glp_interface()
