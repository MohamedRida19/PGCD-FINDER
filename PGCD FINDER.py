import sympy as sp
import customtkinter as ctk
from PIL import Image
import re

clear_icon_noir = Image.open(r'C:\\Users\\MSI\\Downloads\\retirer.png')
clear_icon_blanc = Image.open(r'C:\\Users\\MSI\\Downloads\\retirer(1).png')
clear_icon_tk = ctk.CTkImage(light_image=clear_icon_noir, dark_image=clear_icon_blanc, size = (20,20))

delete_icon_noir = Image.open(r'C:\\Users\\MSI\\Downloads\\clear.png')
delete_icon_blanc = Image.open(r'C:\\Users\\MSI\\Downloads\\clear(1).png')
delete_icon_tk = ctk.CTkImage(light_image=delete_icon_noir, dark_image=delete_icon_blanc, size = (40, 40))

exposant_icon_blanc = Image.open(r"C:\\Users\\MSI\\Downloads\\exposant_n(2).png")
exposant_icon_noir = Image.open(r"C:\\Users\\MSI\\Downloads\\exposant_n(3).png")
exposant_icon_tk = ctk.CTkImage(light_image= exposant_icon_noir, dark_image= exposant_icon_blanc, size= (30, 30))

guid_icon = Image.open(r'C:\\Users\\MSI\\Downloads\\user-guide.png')
guid_icon_tk = ctk.CTkImage(light_image= guid_icon, dark_image=guid_icon, size = (70, 70))

root = ctk.CTk()

frame_top = ctk.CTkFrame(root)

math_img = Image.open(r"C:\\Users\\MSI\\Downloads\\math-book.png")
math_img_tk = ctk.CTkImage(light_image=math_img, dark_image=math_img, size = (50, 50))
calc_img = Image.open(r"C:\\Users\\MSI\\Downloads\\calculating.png")
calc_img_tk = ctk.CTkImage(light_image= calc_img, dark_image= calc_img, size = (50, 50))

math_label_icon = ctk.CTkLabel(frame_top, image=math_img_tk, compound="top", text = "")
math_label_icon.pack(pady = 30, padx = 20, side = 'left', anchor = 'n')

calc_label_icon = ctk.CTkLabel(frame_top, text = '', image=calc_img_tk, compound="top")
calc_label_icon.pack(pady = 30, padx = 20, side = 'right', anchor = 'n')

title = ctk.CTkLabel(frame_top, text='PGCD FINDER', font=('Arial', 50))
title.pack(pady=10, side = 'top')
root.after(100, lambda: root.state('zoomed'))

frame_top.pack(fill = 'x', padx = 10, pady = 10)

def replace_exponents(text):
    '''Remplace X**n par Xⁿ en utilisant des caractères Unicode pour les exposants.'''
    def replace(match):
        base = match.group(1)
        exponent = match.group(2)
        superscript_map = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
        return base + exponent.translate(superscript_map)

    return re.sub(r'(X)\*\*([0-9]+)', replace, text)


def formatted_entry(prefix, str_var, entry, event=None):
    current_text = str_var.get()
    # Remplacer 'x' par 'X'
    if 'x' in current_text:
        str_var.set(str_var.get().replace('x', "X"))

    # Remplacer les exposants
    current_text = replace_exponents(str_var.get())   

    str_var.set(current_text)
    # Extraire l'entrée utilisateur après le signe '='
    if '=' in str_var.get():
        index = str_var.get().index('=')
        user_input = current_text[index + 1:]
    else:
        if prefix in str_var.get():
            user_input = str_var.get().replace(f'{prefix}', "")
        else:
            user_input = str_var.get()
    # Ajouter le préfixe si nécessaire
    if not str_var.get().startswith(f"{prefix} ="):
        entry.delete(0, ctk.END)
        replace_with = f"{prefix} =" + user_input
        entry.insert(0, replace_with)
    # Ajuster le curseur
    if event:
        entry.icursor(event.widget.index(ctk.INSERT) + 1)

def pgcd_finder():
    #Extraire les polynômes des entrées
    index_1 = polynome_1_str_var.get().index('=')
    index_2 = polynome_2_str_var.get().index('=')
    polynome_1 = polynome_1_str_var.get()[index_1 + 1:]
    polynome_2 = polynome_2_str_var.get()[index_2 + 1:]

    #Transformer les exposant a la forme convonable pour sympy
    exposants = "⁰¹²³⁴⁵⁶⁷⁸⁹"
    for exposant in exposants:
        if exposant in polynome_1 :
            polynome_1 = polynome_1.replace(exposant, f"**{exposants.index(exposant)}")
        elif exposant in polynome_2:
            polynome_2 = polynome_2.replace(exposant, f"**{exposants.index(exposant)}")

    X, n = sp.symbols('X n')
    
    #Convertire l'objet str on objet Poly pour evaluee les calculs
    A = sp.Poly(polynome_1)
    B = sp.Poly(polynome_2)
    
    # Calculer le PGCD
    pgcd = sp.gcd(A, B)
    
    # Calculer le quotient et le reste
    Q, R = sp.div(A, B)
    
    # Mettre à jour les étiquettes avec les résultats
    Q_label.configure(text=f"Quotient: {Q.as_expr()}")
    R_label.configure(text=f"Rest: {R.as_expr()}")
    PGCD_label.configure(text=f"Pgcd: {pgcd.as_expr()}")
    result_label.pack(pady=10, anchor='center')
    for widget in filter(lambda x: x != result_label, frame_result.winfo_children()):
        widget.pack(pady=10, anchor='center')
    frame_result.pack(fill='x', pady=10, padx=10)

def exemple_polynome():
    #Définir le symbole X
    X = sp.symbols('X')
    root.focus()
    #Créer les polynomes
    A = 'X² + 2*X + 1'
    B = 'X + 1'

    #Remplacer les polynomes dans les entrées
    entry_polynome_1.delete(0, ctk.END)
    entry_polynome_2.delete(0, ctk.END)
    entry_polynome_1.insert(0, "A(X) ="+ A)
    entry_polynome_2.insert(0, "B(X) ="+ B)
    
    #Afficher le resultat
    pgcd_finder()

def instraction_window():
    #Creer une nouvelle fenetre
    root_1 = ctk.CTkToplevel(root)    #Définir une fenêtre secondaire
    root_1.geometry("1300x600")    #pour saisire les dimensions de la fenêtre
    root_1.title("Instraction Window")    #pour saisire le titre de la fenêtre
    root_1.lift()    #pour placer la fenêtre au premier plan par rapport aux autres fenêtres
    root_1.focus_force()    #pour assurer que les événements de clavier seront dirigés vers cette fenêtre
    root_1.grab_set()    #pour arrêter le fonctionnement des autres fenêtres sauf cette fenêtre
    root_1.resizable(False, False)    #pour arrêter le redimensionnement du fenêtre

    frame_instraction = ctk.CTkFrame(root_1)
    instraction_label_title = ctk.CTkLabel(frame_instraction, text = "Guide d'utilisation", image= guid_icon_tk, compound = 'left', font = ("Arial", 50), text_color= ('#3C1AB5','#2BDBEA'))
    tip_1_label = ctk.CTkLabel(frame_instraction, text = "1-Pour définir correctement un polynôme, entrez les puissances sous la forme X**n.", font = ("Arial", 30))
    tip_2_label = ctk.CTkLabel(frame_instraction, text = "2-La puissance n doit être un entier entre 0 et 9.", font = ("Arial", 30))
    tip_3_label = ctk.CTkLabel(frame_instraction, text = "3-Les coefficients doivent être écrits sous la forme a*X.", font = ("Arial", 30))
    tip_4_label = ctk.CTkLabel(frame_instraction, text = "4-Pour éviter les ambiguïtés dans les expressions complexes, utilisez des parenthèses.", font = ("Arial", 30))
    tip_5_label = ctk.CTkLabel(frame_instraction, text = "5-Assurez-vous que chaque terme est bien formé.", font = ("Arial", 30))
    tip_6_label = ctk.CTkLabel(frame_instraction, text = "6-Utilisez des polynômes simples pour commencer et vérifiez les résultats obtenus\nSi vous rencontrez une erreur, vérifiez la syntaxe de votre entrée.", font = ("Arial", 30))

    
    for widget in frame_instraction.winfo_children():
        widget.pack(pady = 10, padx =10)
    
    frame_instraction.pack(pady = 40, padx = 40, fill = 'both')
    root_1.mainloop()

def get_str_var():
    return root.focus_get()

keyboard_state = False

def keyboard_show_hide():
    global keyboard_state
    btns = [(btn_9, 0, 2), (btn_8, 0, 1), (btn_7, 0, 0), (btn_6, 1, 2), (btn_5, 1, 1), (btn_4, 1, 0), (btn_3, 2, 2), (btn_2, 2, 1), (btn_1, 2, 0), (btn_0, 3, 0), (btn_point, 3, 1), (btn_exposant, 3, 2), (btn_plus, 0, 3), (btn_sustraction, 1, 3), (btn_mult, 2, 3), (btn_division, 3, 3)]
    delete_clear = [(btn_delete, 0, 4), (btn_clear, 2, 4)]
    if not keyboard_state:
        for (i, l, k )in btns+delete_clear :
            i.configure(height = 50, font = ("Arial", 25))
        
        for (btn, row, column) in btns:
            btn.grid(row= row, column = column, sticky = 'ew')
        for (b, r, c) in delete_clear:
            b.grid(row = r, column = c, rowspan = 2, sticky = 'nwes')

        frame_keyboard.pack(padx= 10, pady = 10, fill = 'x', side= 'bottom')
        keyboard_state = True
    else:
        frame_keyboard.pack_forget()
        keyboard_state = False


div_img = Image.open(r"C:\\Users\\MSI\\Downloads\\diviser.png")
div_img_tk = ctk.CTkImage(light_image=div_img, dark_image=div_img, size = (30, 30))


frame_parent = ctk.CTkFrame(root)
frame_parent.columnconfigure(0, weight=1)
frame_parent.columnconfigure(1, weight=1)
frame_parent.columnconfigure(2, weight=1)

polynome_1_str_var = ctk.StringVar(value='A(X) =')
entry_polynome_1 = ctk.CTkEntry(frame_parent, width=200, height=40, textvariable=polynome_1_str_var, font=("Arial", 20), text_color=("#0303BD", '#30AEE5'))
entry_polynome_1.grid(row=0, column=0, pady=10)
entry_polynome_1.bind("<KeyRelease>", lambda x: formatted_entry('A(X)', polynome_1_str_var, entry_polynome_1))


polynome_2_str_var = ctk.StringVar(value='B(X) =')
entry_polynome_2 = ctk.CTkEntry(frame_parent, width=200, height=40, textvariable=polynome_2_str_var, font=("Arial", 20), text_color = ("#0303BD", '#30AEE5'))
entry_polynome_2.grid(row=0, column=2, pady=10)
entry_polynome_2.bind("<KeyRelease>", lambda x: formatted_entry('B(X)', polynome_2_str_var, entry_polynome_2))


pgcd_button = ctk.CTkButton(frame_parent, text='', font=("Arial", 25), image=div_img_tk, command=pgcd_finder, compound='top', fg_color='transparent')
pgcd_button.grid(row=0, column=1, pady=10)

frame_parent.pack(fill='x', padx=10, pady=10)

frame_result = ctk.CTkFrame(root)

result_label = ctk.CTkLabel(frame_result, text="Resultat", font=("Arial", 50), text_color=("#C31307","#EF8729"))
Q_label = ctk.CTkLabel(frame_result, text='Quotient: ', font=("Arial", 30), text_color=("#248F0A","#5AF63F"))
R_label = ctk.CTkLabel(frame_result, text='Rest: ', font=("Arial", 30), text_color= ("#248F0A", "#5AF63F"))
PGCD_label = ctk.CTkLabel(frame_result, text="PGCD: ", font=("Arial", 30), text_color= ("#248F0A", "#5AF63F"))

frame_keyboard = ctk.CTkFrame(root, fg_color= 'transparent')
for i in range(5):
    frame_keyboard.columnconfigure(i, weight=1)


btn_9 = ctk.CTkButton(frame_keyboard, text = '9', font = ("Arial", 15))

btn_8 = ctk.CTkButton(frame_keyboard, text = '8', font = ("Arial", 15))

btn_7 = ctk.CTkButton(frame_keyboard, text = '7', font = ("Arial", 15))

btn_6 = ctk.CTkButton(frame_keyboard, text = '6', font = ("Arial", 15))

btn_5 = ctk.CTkButton(frame_keyboard, text = '5', font = ("Arial", 15))

btn_4 = ctk.CTkButton(frame_keyboard, text = '4', font = ("Arial", 15))

btn_3 = ctk.CTkButton(frame_keyboard, text = '3', font = ("Arial", 15))

btn_2 = ctk.CTkButton(frame_keyboard, text = '2', font = ("Arial", 15))

btn_1 = ctk.CTkButton(frame_keyboard, text = '1', font = ("Arial", 15))

btn_exposant = ctk.CTkButton(frame_keyboard, text = '', image = exposant_icon_tk, compound= 'top', fg_color='#313131')

btn_point = ctk.CTkButton(frame_keyboard, text = '.', font = ("Arial", 15))

btn_0 = ctk.CTkButton(frame_keyboard, text = '0', font = ("Arial", 15))

btn_plus = ctk.CTkButton(frame_keyboard, text = '+', font = ("Arial", 15), fg_color='#313131')

btn_sustraction = ctk.CTkButton(frame_keyboard, text = '-', font = ("Arial", 15), fg_color='#313131')

btn_mult = ctk.CTkButton(frame_keyboard, text = '*', font = ("Arial", 15), fg_color='#313131')

btn_division = ctk.CTkButton(frame_keyboard, text = '/', font = ("Arial", 15), fg_color='#313131')

btn_delete = ctk.CTkButton(frame_keyboard, text = '', fg_color='#313131', image = delete_icon_tk, compound='top')

btn_clear = ctk.CTkButton(frame_keyboard, text = 'CLS', fg_color='#313131', font = ("Arial", 40, 'bold'))


frame_bottom = ctk.CTkFrame(root)
frame_bottom.columnconfigure(0, weight=1)
frame_bottom.columnconfigure(1, weight=1)
frame_bottom.columnconfigure(2, weight=1)

question_icon = Image.open(r"C:\\Users\\MSI\\Downloads\\request.png")
question_icon_tk = ctk.CTkImage(light_image= question_icon, dark_image= question_icon, size = (50, 50))
instruction_button = ctk.CTkButton(frame_bottom, text = "tips", image = question_icon_tk, compound= 'left', command = instraction_window, fg_color='transparent', width = 50, height = 50, font = ("Arial", 35))
instruction_button.grid( column = 0, row = 0, sticky = 'sw', padx = 20)

exemple_icon = Image.open(r'C:\\Users\\MSI\\Downloads\\book.png')
exemple_icon_tk = ctk.CTkImage(light_image= exemple_icon, dark_image=exemple_icon, size=(50, 50))
exemple_button = ctk.CTkButton(frame_bottom, text= "Exemple", width = 50, height = 50, image=exemple_icon_tk, compound='right', command = exemple_polynome, fg_color='transparent', font = ("Arial", 35))
exemple_button.grid(column = 2, row = 0, sticky = 'se', padx = 20)



clavier_icon = Image.open(r'C:\\USers\\MSI\\Downloads\\technology.png')
clavier_icon_tk = ctk.CTkImage(light_image=clavier_icon, dark_image= clavier_icon, size = (50, 50))
clavier_button = ctk.CTkButton(frame_bottom, text = '', image = clavier_icon_tk, compound= 'top', width = 50, height = 50, fg_color= 'transparent', command=keyboard_show_hide)
clavier_button.grid(column = 1, row = 0, padx = 20)


frame_bottom.pack(fill = 'x', side = 'bottom', padx=10, pady=10, anchor = 'center')
root.mainloop()