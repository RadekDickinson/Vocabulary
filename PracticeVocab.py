#%%
import os
try:
    os.chdir(os.path.join(os.getcwd(), "Data"))
except FileNotFoundError:
    os.chdir(os.path.join(os.getcwd(), "Data"))
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox as tmb
import random as r
import re

class Login:
    
    def showlog(*args):
        log_root = tk.Tk()
        log_root.title('Login')
        
        tk.Label(log_root, text = 'Username').grid(row = 0, column = 0, padx = 10, pady = 10)
        tk.Label(log_root, text = 'Password').grid(row = 1, column = 0, padx = 10, pady = 10)
        
        user_ent = tk.Entry(log_root)
        user_ent.insert(0, 'Marek')
        user_ent.grid(row = 0, column = 1, padx = 10, pady = 10)
        
        psw_ent = tk.Entry(log_root, show = '*')
        psw_ent.insert(0, 'Soukup')
        psw_ent.grid(row = 1, column = 1, padx = 10, pady = 10)
        
        def confirm(*args):
            if user_ent.get() == 'Radek' and psw_ent.get() == 'Dickinson':
                log_root.destroy()
                words_inst = Slovka()
            else:
                tmb.showwarning(message = 'Incorrect username or password')
        
        log_in_but = tk.Button(log_root, text = 'Log in', command = confirm)
        log_in_but.grid(row = 2, column = 1, padx = 10, pady = 10)


class OtherMixin:
    
    def show_help(*args):
        Slovka.big_win.insert(tk.END, 'Proste otevri a jed')
    
    
class Slovka(Login, OtherMixin):
    
    data = {}
    stats = {}
    czech = []
    foreign = []
    
    def __init__(self):
        
        Slovka.czech_win = tk.Text(root, height = 1.5, width = 50, font=("Arial", 12))
        Slovka.czech_win.grid(row = 0, column = 2, padx = 10, pady = 10, columnspan = 2)
        
        Slovka.foreign_win = tk.Text(root, height = 1.5, width = 50, font=("Arial", 12))
        Slovka.foreign_win.grid(row = 1, column = 2, padx = 10, pady = 10, columnspan = 2)
        
        Slovka.next_word_but = tk.Button(root, text = 'Next word', command = self.next_word)
        Slovka.next_word_but.configure(cursor='heart')
        Slovka.next_word_but.grid(row = 2, column = 2, padx = 10, pady = 10, sticky = tk.W)
        
        Slovka.hint_but = tk.Button(root, text = 'Hint', command = Slovka.hint)
        Slovka.hint_but.grid(row = 3, column = 2, padx = 10, pady = 10, sticky = tk.W)
        
        Slovka.big_win = tk.Text(root, height = 15, width = 50, background='#101010', foreground="#D6D6D6", font=("Helvetica", 14), borderwidth=18, relief='sunken')
        Slovka.big_win.grid(row = 0, column = 5, rowspan = 4, padx = 10, pady = 10)
        
        root.bind_all('<F1>', OtherMixin.show_help)

    def open_data(*args):
        Slovka.czech_win.delete(1.0, tk.END)
        
        filename = filedialog.askopenfilename()
        split_filename = filename.split('/')
        Slovka.language = split_filename[-2]

        root.title(os.path.basename(filename))
        
        with open(filename, 'r', newline = '\n', encoding = 'utf-8') as inpt:
            
            for i in inpt:
                try:
                    c, f = i.split('\t')
                except ValueError:
                    print('Chyba radek: ' + i)
                c = re.sub('[\n\r]', '', c)
                f = re.sub('[\n\r]', '', f)
                Slovka.czech.append(c)
                Slovka.foreign.append(f)
            
        Slovka.data = dict(zip(Slovka.czech, Slovka.foreign))
        vals = [[0,0] for i in range(len(Slovka.foreign))]
        
        Slovka.stats = dict(zip(Slovka.foreign, vals))
        Slovka.czech_win.insert(tk.END, r.choice(Slovka.czech))
        
    def next_word(*args):
        key = re.sub('\n', '', Slovka.czech_win.get('1.0', tk.END))
        value = re.sub('\n', '', Slovka.data[key])
        entry = re.sub('\n', '', Slovka.foreign_win.get('1.0', tk.END))
        
        if entry == value:
            Slovka.big_win.delete(1.0, tk.END)
            Slovka.big_win.insert(tk.END, 'Correct!\n{0} = {1} in {2}'.format(key, entry, Slovka.language))
            Slovka.czech.remove(key)
            Slovka.stats[value][0] += 1
            
        else:
            Slovka.big_win.delete(1.0, tk.END)
            Slovka.big_win.insert(tk.END, 'Incorrect!\n{0} <> {1} in {2}'.format(key, entry, Slovka.language))
            
        Slovka.czech_win.delete(1.0, tk.END)
        Slovka.stats[value][1] += 1
        
        try:
            Slovka.czech_win.insert(tk.END, r.choice(Slovka.czech))
        except IndexError:
            Slovka.big_win.delete(1.0, tk.END)
            Slovka.big_win.insert(tk.END, 'End of test. Results:\n')
            Slovka.foreign = []
            
            for key, value in Slovka.stats.items():
                score = value[0]/value[1]
                if score != 1:
                    Slovka.big_win.insert(tk.END, "{}: {}%\n".format(key, round(score*100)))
            Slovka.big_win.insert(tk.END, '100% otherwise')
            
        Slovka.foreign_win.delete(1.0, tk.END)
        
    def hint(*args):
        key = re.sub('[\n\r]', '', Slovka.czech_win.get('1.0', tk.END))
        value = re.sub('[\n\r]', '', Slovka.data[key])
        
        Slovka.big_win.delete(1.0, tk.END)
        Slovka.big_win.insert(tk.END, '{0} is {1} in {2}'.format(key, value, Slovka.language))
        
#%%

root = tk.Tk()
root.configure(background = 'green')
root.title('')

words_inst = Slovka()

# Uncomment the following line to switch on login
# Login.showlog()

menu_bar = tk.Menu(root)
file_menu = tk.Menu(menu_bar, tearoff = 0)
about_menu = tk.Menu(menu_bar, tearoff = 0)
menu_bar.add_cascade(label='File', menu=file_menu)
menu_bar.add_cascade(label = 'About', menu=about_menu)
root.config(menu=menu_bar)

file_menu.add_command(label="Open data", accelerator='Ctrl+O', compound='left'
#                      , image = 'open_icon.png'
                      , underline=0
                      , command = Slovka.open_data)


root.mainloop()