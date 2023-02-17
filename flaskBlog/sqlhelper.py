import pymysql
from dbutils.pooled_db import PooledDB

POOL = PooledDB(
    creator=pymysql,
    maxconnections=6,
    mincached=2,
    blocking=True,  # 连接数超过最大数量是否阻塞等待True：等待，False:不等然后报错
    ping=0,
    hosts='127.0.0.1',
    port=3306,
    user='skyrimlight',
    password='skyrimlight',
    database='flask',
    charset='utf8'
)


def fetchall(sql, *args):
    conn = POOL.connection()
    cursor = conn.cursor()
    cursor.execute(sql, args)
    result = cursor.fetchall()
    cursor.close()
    # 将连接放回连接池
    conn.close()
    return result


def fetchone(sql, *args):
    conn = POOL.connection()
    cursor = conn.cursor()
    cursor.execute(sql, args)
    result = cursor.fetchone()
    cursor.close()
    # 将连接放回连接池
    conn.close()
    return result
