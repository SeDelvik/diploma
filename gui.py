from tkinter import *
from tkinter import filedialog

from run_alg import run_alg

variables = {}


# todo написать скрытие ненужных полей при выборе определенных параметров
def start_gui():
    def get_file_name():
        file = filedialog.askopenfilename(filetypes=(("JSON", "*.json"), ("all files", "*.*")))
        lbl_src.configure(text=f"{file}")
        variables["src"] = file
        print(variables["src"])

    def start_alg():
        """
        Валидация нескольких параметров, запихивание параметров в словарь и запуск основного алгоритма.
        :return:
        """
        if "src" not in variables:
            lbl_error.configure(text="Файл НЕ выбран!")
            return
        if not is_probability(txt_probability.get()):
            lbl_error.configure(text="Неправильно указана вероятность")
            return
        if spin_count.get() < spin_count_person_in_swap.get():
            lbl_error.configure(text="Количество особей для обменя превышает количество особей в популяции")
            return
        arr_params = [choice_var.get(), recombination_var.get(), mutation_var.get(), select_var.get()]
        variables["methode"] = alg_var.get()
        variables["operators"] = arr_params
        variables["population_count"] = int(spin_count.get())
        variables["probability"] = float(txt_probability.get())
        variables["island_count"] = int(spin_island_count.get())
        variables["count_generations"] = int(spin_count_generation.get())
        variables["count_person_in_swap"] = int(spin_count_person_in_swap.get())
        print(variables)
        run_alg(variables)  # запуск основного алгоритма

    def is_probability(string: str) -> bool:
        """
        Валидация для вероятности.
        :param string: Предполагаемая строка с вероятностью.
        :return:
        """
        try:
            num = float(string)
            if 0 <= num <= 1:
                return True
            else:
                return False
        except ValueError:
            return False

    window = Tk()
    window.title("Добро пожаловать")
    window.geometry('950x550')

    lbl = Label(window, text="Укажите scr-файл")
    lbl.grid(column=0, row=0)
    btn = Button(window, text="Выбрать", command=get_file_name)
    btn.grid(column=1, row=0)
    lbl_src = Label(window, text="")
    lbl_src.grid(column=2, row=0)

    lbl_title1 = Label(window, text="Выберите используемый алгоритм и параметры")
    lbl_title1.grid(column=0, row=1, columnspan=5)

    # алгоритмы
    lbl_algs = Label(window, text="Алгоритм:")
    lbl_algs.grid(column=0, row=2)
    simple = "SimpleGenAlg"
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
    with_binary_crossingover = 2

    recombination_var = IntVar(value=one_point_crossingover)

    recombination_btn1 = Radiobutton(window, text="Одноточечный кроссинговер", value=one_point_crossingover,
                                     variable=recombination_var)
    recombination_btn2 = Radiobutton(window, text="Двухточечный кроссинговер", value=two_point_crossingover,
                                     variable=recombination_var)
    recombination_btn3 = Radiobutton(window, text="С использованием бинарной маски", value=with_binary_crossingover,
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

    # дополнительно
    lbl_count = Label(window, text="Количество особей в поколении")
    spin_count_var = IntVar()
    spin_count_var.set(100)
    spin_count = Spinbox(window, from_=10, to=1000, textvariable=spin_count_var)
    lbl_count.grid(column=0, row=6)
    spin_count.grid(column=1, row=6)

    lbl_probability = Label(window, text="Вероятность для бинарной мутации")
    txt_probability = Entry(window)
    txt_probability.insert(0, "0")
    lbl_probability.grid(column=0, row=7)
    txt_probability.grid(column=1, row=7)

    lbl_island_count = Label(window, text="Количество \"островов\"")
    spin_island_count = Spinbox(window, from_=2, to=10)  # я не думаю что эта тварь справится если выставить больше
    lbl_island_count.grid(column=0, row=8)
    spin_island_count.grid(column=1, row=8)

    lbl_count_generation = Label(window, text="Количество поколений до обменя")
    spin_count_generation = Spinbox(window, from_=1, to=100)
    lbl_count_generation.grid(column=0, row=9)
    spin_count_generation.grid(column=1, row=9)

    lbl_count_person_in_swap = Label(window, text="Количество особей в обмене между островами")
    spin_count_person_in_swap = Spinbox(window, from_=1, to=1000)
    lbl_count_person_in_swap.grid(column=0, row=10)
    spin_count_person_in_swap.grid(column=1, row=10)

    # кнопка начала

    btn_start = Button(window, text="Запустить", command=start_alg)
    btn_start.grid(column=0, row=11, columnspan=5)
    lbl_error = Label(window, text="", fg="red")
    lbl_error.grid(column=0, row=12, columnspan=5)

    window.mainloop()
