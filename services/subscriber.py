from database import connection
import pymysql

def add_subscriber(phone: str):
    cursor = connection.cursor()

    try:
        sql = """
        INSERT INTO students(phone)
        VALUES(%s)
        """

        cursor.execute(sql, (phone,))
        connection.commit()

        return True

    except pymysql.err.IntegrityError:
        return False

    finally:
        cursor.close()


def remove_subscriber(phone: str):
    cursor = connection.cursor()

    try:
        sql = """
        DELETE FROM students
        WHERE phone = %s
        """

        cursor.execute(sql, (phone,))
        connection.commit()

        return cursor.rowcount > 0

    finally:
        cursor.close()


def get_all_subscribers():
    cursor = connection.cursor()

    try:
        sql = """
        SELECT * FROM students
        """

        cursor.execute(sql)

        rows = cursor.fetchall()

        subscribers = []

        for row in rows:
            subscribers.append({
                "id": row[0],
                "phone": row[1]
            })

        return subscribers

    finally:
        cursor.close()


