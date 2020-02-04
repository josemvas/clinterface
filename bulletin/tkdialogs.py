# -*- coding: utf-8 -*-
import tkinter
from argparse import ArgumentParser

class TkDialogs(object):
    def __init__(self):
        self.font = ('Sans', 8)

    def tkbox(self, prompt, b1, b2, choices):
        root = self.root = tkinter.Tk()
        root.title('Mensaje')
        self.prompt = str(prompt)
        # default values for the buttons to return
        self.b1_return = True
        self.b2_return = False
        # main frame
        frm_1 = tkinter.Frame(root)
        frm_1.pack(ipadx=2, ipady=2)
        # the prompt
        prompt = tkinter.Label(frm_1, text=self.prompt, font=self.font, wraplength=500)
        prompt.pack(padx=8, pady=8)
        # if entry=True create and set focus
        if choices:
            self.b2_return = None
            self.listbox = tkinter.Listbox(frm_1, selectmode=tkinter.BROWSE, font=self.font, background='white', width=40)
            self.listbox.bind('<Double-Button>', self.b1_action)
            self.listbox.pack()
            self.listbox.focus_set()
            for i in choices:
                self.listbox.insert(tkinter.END, i)
        # button frame
        frm_2 = tkinter.Frame(frm_1)
        frm_2.pack(padx=4, pady=4)
        # buttons
        btn_1 = tkinter.Button(frm_2, width=8, text=b1, font=self.font)
        btn_1['command'] = self.b1_action
        btn_1.pack(side='left', padx=3)
        btn_1.bind('<KeyPress-Return>', func=self.b1_action)
        if b2:
            btn_2 = tkinter.Button(frm_2, width=8, text=b2, font=self.font)
            btn_2['command'] = self.b2_action
            btn_2.pack(side='left', padx=3)
            btn_2.bind('<KeyPress-Return>', func=self.b2_action)
        # roughly center the box on screen
        #root.update_idletasks()
        xp = max(root.winfo_pointerx() - root.winfo_rootx() - 200, 0)
        yp = max(root.winfo_pointery() - root.winfo_rooty() - 100, 0)
        root.geometry('+{0}+{1}'.format(xp, yp))
        # call self.close_mod when the close button is pressed
        root.protocol("WM_DELETE_WINDOW", self.close_mod)

    def b1_action(self, event=None):
        try: x = self.listbox.curselection()
        except AttributeError:
            self.returning = self.b1_return
            self.root.quit()
        else:
            if x:
                self.returning = x
                self.root.quit()

    def b2_action(self, event=None):
        self.returning = self.b2_return
        self.root.quit()

    # remove this function and the call to protocol
    # then the close button will act normally
    def close_mod(self):
        pass

    def to_clip(self, event=None):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.prompt)

    def message(self, prompt):
        self.tkbox(prompt, 'OK', None, None)
        self.root.mainloop()
        # the function pauses here until the mainloop is quit
        self.root.destroy()
    
    def yesno(self, prompt, default=None):
        self.tkbox(prompt, 'Si', 'No', None)
        self.root.mainloop()
        # the function pauses here until the mainloop is quit
        self.root.destroy()
        return self.returning
    
    def chooseone(self, prompt, choices, default=None):
        self.tkbox(prompt, 'Continuar', 'Cancelar', choices)
        self.root.mainloop()
        # the function pauses here until the mainloop is quit
        self.root.destroy()
        if self.returning is None:
            return None
        else:
            return choices[self.returning[0]]
    
def optionbox():
    parser = ArgumentParser(description='Crea un cuadro de diálogo con una lista de opciones.')
    parser.add_argument('-o', '--option', metavar=('DESCRIPCIÓN', 'COMANDO'), dest='options', action='append', nargs=2, help='Agregar opción a la lista de opciones')
    parser.add_argument('prompt', metavar='MENSAJE', type=str, help='Mensaje del cuadro de diálogo.')
    arguments = parser.parse_args()
    choice = chooseone(arguments.prompt, choices=[i for i,j in arguments.options])
    if choice is not None:
         print(dict(arguments.options)[choice])

