from database.DB_connect import DBConnect
from model.States import State
from model.Sighting import Sighting


class DAO:

    def __init__(self):
        pass

    @staticmethod
    def getAllStates():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT * 
                   FROM state s  """

        cursor.execute(query)

        for row in cursor:
            result.append(State(row["id"],
                                row["Name"],
                                row["Capital"],
                                row["Lat"],
                                row["Lng"],
                                row["Area"],
                                row["Population"],
                                row["Neighbors"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllSighting():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT * 
                   FROM sighting s 
                   ORDER BY `datetime` ASC"""

        cursor.execute(query)

        for row in cursor:
            result.append(Sighting(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllNeighbors(year, shape):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT n.state1, n.state2 , count(*) as N
                   FROM sighting s , neighbor n 
                   WHERE year(s.`datetime`) = %s
                   AND s.shape = %s
                   AND (s.state = n.state1 or s.state = n.state2 )
                   AND n.state1 < n.state2
                   GROUP BY n.state1 , n.state2 """

        cursor.execute(query, (year, shape))

        for row in cursor:
            result.append((row['state1'], row['state2'], row["N"]))

        cursor.close()
        conn.close()
        return result
