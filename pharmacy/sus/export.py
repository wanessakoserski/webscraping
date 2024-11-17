import pandas as pd
from server.database_pharmacy import PharmacyDatabase


db = PharmacyDatabase()

def export_sus_data():
    df = pd.read_csv('./pharmacy/sus/file.csv')
    medicines = df['name'].dropna().tolist()
    
    db.insert_reference_rows(medicines)

def delete_tables():
    db.delete_reference_table()
