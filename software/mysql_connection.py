import mysql.connector

from dotenv import load_dotenv
import os

class DBConnection:
  def __init__(self, host:str):

    load_dotenv()

    user = os.getenv('MYSQL_USER')
    password = os.getenv('MYSQL_PASSWORD')

    self.cnx = mysql.connector.connect(
      user=user,
      password=password,
      host=host,
      database="default"
    )

  def __del__(self):
    self.cnx.close()

  def _get_controlled_property(self, entity_id:str) -> list:

    query = (
      "SELECT attrValue "
      f"FROM {entity_id}_Device "
      "WHERE attrName = 'controlledProperty' "
      "LIMIT 1"
    )

    cursor = self.cnx.cursor()
    cursor.execute(query)

    row = cursor.fetchone()
    cursor.close()

    if row is not None:
      return eval(row[0])

    return []

  def _get_values(self, entity_id:str) -> list:

    query = (
      "SELECT attrValue, recvTime "
      f"FROM {entity_id}_Device "
      "WHERE attrName = 'value' "
      "AND recvTime >= NOW() - INTERVAL 1 DAY "
    )

    cursor = self.cnx.cursor()
    cursor.execute(query)

    values = []
    times = []
    for row in cursor.fetchall():
      if "null" in row[0]: continue
      values.append(row[0])
      times.append(row[1])

    cursor.close()

    return values, times

  def _format_values(self, controlledProperties:list, raw_values:list, times:list) -> list[dict]:
    data = []

    for i, value in enumerate(raw_values):
      values = value.split("&")

      value_object = {
        "dateObserved": times[i]
      }

      for j, controlledProperty in enumerate(controlledProperties):
        value_object[controlledProperty] = values[j]

      data.append(value_object)

    return data

  def get_history(self, entity_id:str) -> list[dict]:
    controlledProperties = self._get_controlled_property(entity_id)
    raw_values, times = self._get_values(entity_id)

    formated_values = self._format_values(controlledProperties, raw_values, times)

    return formated_values

if __name__ == "__main__":
  from common_data import lab_host

  db = DBConnection(lab_host)
  values = db.get_history("tree_sensor_0")

  for value in values:
    print(value)
