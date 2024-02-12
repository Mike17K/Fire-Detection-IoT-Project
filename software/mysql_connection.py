import mysql.connector

class DBConnection:
  def __init__(self, host):
    self.cnx = mysql.connector.connect(
      user="root",
      password="root_password",
      host=host,
      database="default",
      ssl_disabled=True
    )

  def _get_controlled_property(self, entity_id) -> list:

    query = f"SELECT attrValue FROM {entity_id}_Device WHERE attrName = 'controlledProperty'"

    cursor = self.cnx.cursor()
    cursor.execute(query)

    row = cursor.fetchone()
    cursor.reset()
    cursor.close()

    if row is not None:
      return eval(row[0])

    return []

  def _get_values(self, entity_id) -> list:

    query = f"SELECT attrValue FROM {entity_id}_Device WHERE attrName='value'"

    cursor = self.cnx.cursor()
    cursor.execute(query)

    values = []
    for row in cursor.fetchall():
      if "null" in row[0]: continue
      values.append(row[0])

    cursor.close()

    return values

  def _format_values(self, controlledProperties:list, raw_values:list) -> list[dict]:
    data = []

    for value in raw_values:
      values = value.split("&")

      value_object = {}
      for i, controlledProperty in enumerate(controlledProperties):
        value_object[controlledProperty] = values[i]

      data.append(value_object)

    return data

  def get_history(self, entity_id) -> list[dict]:
    controlledProperties = self._get_controlled_property(entity_id)
    raw_values = self._get_values(entity_id)

    formated_values = self._format_values(controlledProperties, raw_values)

    return formated_values

if __name__ == "__main__":
  db = DBConnection("150.140.186.118")
  values = db.get_history("tree_sensor_0")

  for value in values:
    print(value)
