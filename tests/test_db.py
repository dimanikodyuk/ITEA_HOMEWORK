import sqlite3

# Проверка на работу БД
def test_my_divisor_func():
    conn = sqlite3.connect("order_service_db.db")
    cursor = conn.cursor()
    sel = "select 1+1"
    res = cursor.execute(sel)
    res_value = res.fetchone()
    assert res_value[0] == 2