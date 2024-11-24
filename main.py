import pharmacy.sus.export as sus

# sus.delete_tables()
# sus.export_sus_data()

from server.database_pharmacy import PharmacyDatabase

db = PharmacyDatabase()
db.select_referece_table()