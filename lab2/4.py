# Инициализация переменных
sum = 0  
count = 0      

print("Введите последовательность целых чисел:")

while True:
    user_input = input("Введите число: ")
    
    if user_input == "":
        break
    
    # Преобразуем ввод в целое число
    try:
        number = int(user_input)
    except ValueError:
        print("Ошибка: введите целое число.")
        continue  
    
    # Обновляем сумму и количество чисел
    sum += number
    count += 1

# Выводим результаты
print(f"Сумма всех чисел: {sum}")
print(f"Количество всех чисел: {count}")