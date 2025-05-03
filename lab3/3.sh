#!/bin/bash

# 1. GET запрос с random param от 1 до 10
a=$((1 + RANDOM % 10))
echo "GET запрос с param=$a"
response_get=$(curl -s "http://localhost:5000/number/?param=$a")
n1=$(echo $response_get | jq -r '.result')
echo "GET результат: $n1"

# 2. POST запрос с random jsonParam от 1 до 10
b=$((1 + RANDOM % 10))
echo "POST запрос с jsonParam=$b"
response_post=$(curl -s -X POST -H "Content-Type: application/json" -d "{\"jsonParam\": $b}" http://localhost:5000/number/)
n2=$(echo $response_post | jq -r '.result')
op2=$(echo $response_post | jq -r '.operation')
echo "POST результат: $n2 (операция: $op2)"

# 3. DELETE запрос
echo  "DELETE запрос"
response_delete=$(curl -s -X DELETE http://localhost:5000/number/)
n3=$(echo $response_delete | jq -r '.result')
a_d=$(echo $response_delete | jq -r '.a')
b_d=$(echo $response_delete | jq -r '.b')
op3=$(echo $response_delete | jq -r '.operation')
echo "DELETE: $a_d $op3 $b_d = $n3"

# 4. Вычисление результата
r=$((a - b))
final=$(printf "%.0f" $r)  # Приводим к целому числу
echo -e "Финальный результат: $final"