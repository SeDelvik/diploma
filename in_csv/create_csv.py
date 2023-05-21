from datetime import datetime
from pathlib import Path
import json


# todo дописать в сборку файла поле "best population"
def create_csv():
    data_list = []
    path_list = Path("../output").glob('*.json')
    for path in path_list:
        with open(path, 'r') as jp:
            data_list.append(json.load(jp))

    with open(f'./output/{datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}.csv', 'w+') as file:
        file.write("Метод,Выбор родителей,Скрещивание,Мутация,Создание новой популяции," +
                   "Вероятность мутации (только бинарная мутация),Кол-во особей в популяции/на одном острове,"
                   "Количество островов (только островной алг),Количество особей участвующих в обмене (только островной алг),"
                   "Время выполнения,Лучшая приспособленность\n")
        for data in data_list:
            tmp_arr_fit = data["fits_in_all_time"][:]
            tmp_arr_fit.sort()
            translated_operators = translate_operators(data["operators"])
            tmp_string = ""
            if data["methode"] == "IslandGenAlg":  # островной
                tmp_string += f"Островной алгоритм,,,,,," + \
                              str(data["population_count"]) + "," + \
                              str(data["island_count"]) + "," + \
                              str(data["count_person_in_swap"]) + "," + \
                              data["execution_time"] + "," + \
                              str(tmp_arr_fit[len(tmp_arr_fit) - 1])
                continue

            if data["methode"] == "SimpleGenAlg":
                tmp_string += f"Стандартный алгоритм,{translated_operators[0]},{translated_operators[1]}," \
                              f"{translated_operators[2]},{translated_operators[3]},"
            elif data["methode"] == "CellGenAlg":
                tmp_string += f"Ячеистый алгоритм,,{translated_operators[1]},{translated_operators[2]},,"

            if data["operators"][2] == 0:  # обычная ли мутация
                tmp_string += str(data["probability"])
            tmp_string += "," + str(data["population_count"]) + ",,," + \
                          str(data["execution_time"]) + "," + \
                          str(tmp_arr_fit[len(tmp_arr_fit) - 1])

            file.write(tmp_string + "\n")


def translate_operators(arr: list[int]) -> list[str]:
    tmp_arr = []
    if arr[0] == 0:
        tmp_arr.append("Панмиксия")
    elif arr[0] == 1:
        tmp_arr.append("Аутбридинг")
    else:
        tmp_arr.append("Селекция")

    if arr[1] == 0:
        tmp_arr.append("Одноточечный кроссинговер")
    elif arr[1] == 1:
        tmp_arr.append("Двухточечный кроссинговер")
    else:
        tmp_arr.append("Триадный кроссинговер")

    if arr[2] == 0:
        tmp_arr.append("Двоичная мутация")
    elif arr[2] == 1:
        tmp_arr.append("Инверсия")
    else:
        tmp_arr.append("Транслокация")

    if arr[3] == 0:
        tmp_arr.append("Замещение")
    elif arr[3] == 1:
        tmp_arr.append("Усечение")
    else:
        tmp_arr.append("Элитарный отбор")
    return tmp_arr


if __name__ == '__main__':
    create_csv()
