import requests
import random

# 1. GET запрос
a = random.randint(1, 10)
g = requests.get(f'http://127.0.0.1:5000/number/?param={a}').json() 
n1 = g['result']
print(f'GET: {n1}')

# 2. POST запрос
b = random.randint(1, 10)
p = requests.post('http://127.0.0.1:5000/number/',
                 json={'jsonParam': b},
                 headers={'Content-Type': 'application/json'}).json()
n2 = p['result']
op2 = p['operation']
print(f'POST: {n2} {op2} {b}')

# 3. DELETE запрос
d = requests.delete('http://127.0.0.1:5000/number/').json()
n3 = d['result']
op3 = d['operation']
a_d = d['a']
b_d = d['b']
print(f'DELETE: {a_d} {op3} {b_d} = {n3}')

# 4. Вычисление результата
r = n1          # начальное значение
r = r + n2      # добавляем POST результат
r = r + n3      # добавляем DELETE результат

# Итоговый результат как целое число
final = int(r)
print(f'Final: {final}')