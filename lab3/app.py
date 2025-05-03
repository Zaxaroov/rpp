# Импортируем нужные модули
from flask import Flask, request, jsonify
import random
import json

# Создаем приложение Flask
app = Flask(__name__)

# 1. GET эндпоинт /number/
@app.route('/number/', methods=['GET'])
def get_number():
    # Получаем параметр 'param' из запроса
    param = request.args.get('param')
    
    # Пробуем преобразовать в число
    try:
        num = float(param)
    except:
        # Если не получилось, возвращаем ошибку
        return jsonify({'error': 'Invalid parameter'}), 400
    
    # Генерируем случайное число от 1 до 100
    rand_num = random.uniform(1, 100)
    
    # Умножаем на наш параметр
    r = rand_num * num
    
    # Возвращаем результат в JSON
    return jsonify(
        {'result': r,
        'rand_num': rand_num,
         'input': param}
        )

# 2. POST эндпоинт /number/
@app.route('/number/', methods=['POST'])
def post_number():
    # Получаем JSON из тела запроса
    data = request.get_json()
    
    # Проверяем есть ли поле 'jsonParam'
    if 'jsonParam' not in data:
        return jsonify({'error': 'Missing jsonParam'}), 400
    
    # Пробуем преобразовать в число
    try:
        num = float(data['jsonParam'])
    except:
        return jsonify({'error': 'Invalid jsonParam'}), 400
    
    # Генерируем случайное число от 1 до 100
    rand_num = random.uniform(1, 100)
    
    # Выбираем случайную операцию
    oper = random.choice(['+', '-', '*', '/'])
    
    # Выполняем операцию
    if oper == '+':
        r= rand_num + num
    elif oper == '-':
        r= rand_num - num
    elif oper == '*':
        r = rand_num * num
    elif oper == '/':
        r= rand_num / num
    
    # Возвращаем результат
    return jsonify({
        'random_number': rand_num,
        'operation': oper,
        'result': r
    })

# 3. DELETE эндпоинт /number/
@app.route('/number/', methods=['DELETE'])
def delete_number():
    # Генерируем 2 случайных числа
    a = random.uniform(1, 100)
    b = random.uniform(1, 100)
    
    # Выбираем случайную операцию
    oper = random.choice(['+', '-', '*', '/'])
    
    # Выполняем операцию
    if oper == '+':
        r = a + b
    elif oper == '-':
        r = a - b
    elif oper == '*':
        r= a * b
    elif oper == '/':
        r = a / b
    
    # Возвращаем результат
    return jsonify({
        'a': a,
        'b': b,
        'operation': oper,
        'result': r
    })

# Запускаем сервер
if __name__ == '__main__':
    app.run(debug=True)