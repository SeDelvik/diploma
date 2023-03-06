from tkinter import *
from tkinter import filedialog

from run_alg import run_alg

variables = {}


def start_gui():
    def get_file_name():
        file = filedialog.askopenfilename(filetypes=(("JSON", "*.json"), ("all files", "*.*")))
        lbl_src.configure(text=f"{file}")
        variables["src"] = file
        print(variables["src"])

    def start_alg():
        if "src" in variables:
            arr_params = [choice_var.get(), recombination_var.get(), mutation_var.get(), select_var.get()]
            variables["methode"] = alg_var.get()
            variables["operators"] = arr_params
            run_alg(variables)  # запуск основного алгоритма
        else:
            lbl_error.configure(text="Файл НЕ выбран!")

    window = Tk()
    window.title("Добро пожаловать")
    window.geometry('800x550')

    lbl = Label(window, text="Укажите scr-файл")
    lbl.grid(column=0, row=0)
    btn = Button(window, text="Выбрать", command=get_file_name)
    btn.grid(column=1, row=0)
    lbl_src = Label(window, text="")
    lbl_src.grid(column=2, row=0)

    lbl_title1 = Label(window, text="Выберите используемый алгоритм и параметры")
    lbl_title1.grid(column=0, row=1, columnspan=3)

    # алгоритмы
    lbl_algs = Label(window, text="Алгоритм:")
    lbl_algs.grid(column=0, row=2)
    simple = "SimpleGenVal"
    cell = "CellGenAlg"
    island = "IslandGenAlg"

    alg_var = StringVar(value=simple)
    alg_btn1 = Radiobutton(window, text="Простой ген. алг", value=simple, variable=alg_var)
    alg_btn2 = Radiobutton(window, text="Ячеистый ген. алг", value=cell, variable=alg_var)
    alg_btn3 = Radiobutton(window, text="Островной ген. алг", value=island, variable=alg_var)

    alg_btn1.grid(column=0, row=3)
    alg_btn2.grid(column=0, row=4)
    alg_btn3.grid(column=0, row=5)

    # выбор родителей
    lbl_choice_par = Label(window, text="Выбор родителей")
    lbl_choice_par.grid(column=1, row=2)

    panmics = 0
    autbreeding = 1
    selection = 2

    choice_var = IntVar(value=panmics)

    choice_btn1 = Radiobutton(window, text="Панмиксия", value=panmics, variable=choice_var)
    choice_btn2 = Radiobutton(window, text="Аутбридинг", value=autbreeding, variable=choice_var)
    choice_btn3 = Radiobutton(window, text="Селекция", value=selection, variable=choice_var)
    choice_btn1.grid(column=1, row=3)
    choice_btn2.grid(column=1, row=4)
    choice_btn3.grid(column=1, row=5)

    # скрещивание
    lbl_recombination = Label(window, text="Оператор рекомбинации")
    lbl_recombination.grid(column=2, row=2)

    one_point_crossingover = 0
    two_point_crossingover = 1
    wiht_binary_crossingover = 2

    recombination_var = IntVar(value=one_point_crossingover)

    recombination_btn1 = Radiobutton(window, text="Одноточечный кроссинговер", value=one_point_crossingover,
                                     variable=recombination_var)
    recombination_btn2 = Radiobutton(window, text="Двухточечный кроссинговер", value=two_point_crossingover,
                                     variable=recombination_var)
    recombination_btn3 = Radiobutton(window, text="С использованием бинарной маски", value=wiht_binary_crossingover,
                                     variable=recombination_var)
    recombination_btn1.grid(column=2, row=3)
    recombination_btn2.grid(column=2, row=4)
    recombination_btn3.grid(column=2, row=5)

    # мутация
    lbl_mutation = Label(window, text="Оператор мутации")
    lbl_mutation.grid(column=3, row=2)

    binary_mutation = 0
    inversion = 1
    translocation = 2

    mutation_var = IntVar(value=binary_mutation)

    mutation_btn1 = Radiobutton(window, text="Бинарная мутация", value=binary_mutation,
                                variable=mutation_var)
    mutation_btn2 = Radiobutton(window, text="Инверсия", value=inversion,
                                variable=mutation_var)
    mutation_btn3 = Radiobutton(window, text="Транслокация", value=translocation,
                                variable=mutation_var)
    mutation_btn1.grid(column=3, row=3)
    mutation_btn2.grid(column=3, row=4)
    mutation_btn3.grid(column=3, row=5)

    # отбор в новую популяцию
    lbl_select = Label(window, text="Отбор в новое поколение")
    lbl_select.grid(column=4, row=2)

    substitution = 0
    truncation = 1
    elite_selection = 2

    select_var = IntVar(value=substitution)

    select_btn1 = Radiobutton(window, text="Полное замещение", value=substitution,
                              variable=select_var)
    select_btn2 = Radiobutton(window, text="Усечение", value=truncation,
                              variable=select_var)
    select_btn3 = Radiobutton(window, text="Элитарный отбор", value=elite_selection,
                              variable=select_var)
    select_btn1.grid(column=4, row=3)
    select_btn2.grid(column=4, row=4)
    select_btn3.grid(column=4, row=5)

    # кнопка начала

    btn_start = Button(window, text="Запустить", command=start_alg)
    btn_start.grid(column=0, row=6)
    lbl_error = Label(window, text="")
    lbl_error.grid(column=1, row=6)

    window.mainloop()
