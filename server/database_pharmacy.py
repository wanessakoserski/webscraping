from server.connection import ServerConnection


class PharmacyDatabase:
    def __init__(self):
        self.server = ServerConnection('Pharmacy')

    def insert_reference_rows(self, values):
        if not self.server.check_table_exists("REFERENCE_MEDICINE"):
            self.server.create_table("REFERENCE_MEDICINE", "id INT IDENTITY(1,1) PRIMARY KEY, name NVARCHAR(255)")

        for value in values:
            self.server.insert("REFERENCE_MEDICINE", "name", f"'{value}'")

    def delete_reference_table(self):
        if self.server.check_table_exists("REFERENCE_MEDICINE"):
            self.server.drop_table("REFERENCE_MEDICINE")

    def select_referece_table(self):
        results = self.server.select("REFERENCE_MEDICINE")

        medicines = []
        for result in results:
            medicines.append({'id': result[0], 'name': result[1]})

        return medicines

    def insert_record_rows(self, values):
        if not self.server.check_table_exists("RECORD_MEDICINE"):
            columns = """
                id INT IDENTITY(1,1) PRIMARY KEY,
                pharmacy NVARCHAR(255),
                reference NVARCHAR(255),
                name NVARCHAR(255),
                brand NVARCHAR(100),
                ingredient NVARCHAR(255),
                price DECIMAL(10, 2)
            """
            self.server.create_table("RECORD_MEDICINE", columns)

        for value in values:
            self.server.insert("RECORD_MEDICINE", "pharmacy, reference, name, brand, ingredient, price", value)

    def delete_record_table(self):
        if self.server.check_table_exists("RECORD_MEDICINE"):
            self.server.drop_table("RECORD_MEDICINE")

    def select_record_table(self):
        results = self.server.select("RECORD_MEDICINE")

        records = []
        for result in results:
            records.append({'id': result[0], 
                            'pharmacy': result[1],
                            'reference': result[2],
                            'name': result[3], 
                            'brand': result[4],
                            'ingredient': result[5],
                            'price': result[6]})

        return records
