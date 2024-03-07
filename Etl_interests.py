from sqlalchemy import create_engine
from sqlalchemy.engine import URL
import pypyodbc
import pandas as pd

SERVER_NAME = '' #Add you specifi MSSMS Server Name
DATABASE_NAME = '' #add your MSSMS database name
USERNAME = '' # add your MSSMS username 
PASSWORD = '' # Add your MSSMS password 

def load_data_to_sql():
    connection_string = f"""
        DRIVER={{SQL Server}};
        SERVER={SERVER_NAME};
        DATABASE={DATABASE_NAME};
        UID={USERNAME};
        PWD={PASSWORD};
    """
    # Creating the connection to the Database using OBDC
    connection_url = URL.create('mssql+pyodbc', query={'odbc_connect': connection_string})
    engine = create_engine(connection_url, module=pypyodbc)
    df_data = pd.read_csv('dm14_project/cleaned.csv')

    # Split the 'combined_interests' column into a list of interests
    df_data['combined_interests'] = df_data['combined_interests'].str.strip("[]").str.strip("'").str.strip(".").str.split(',')

    # Explode the combined interests column to have one interest per row
    df_interests = df_data.explode('combined_interests')

    # Remove leading and trailing spaces from interests
    df_interests['combined_interests'] = df_interests['combined_interests'].str.strip()

    #Creating a new DF with the required columns
    df_interests_new = df_interests[['combined_interests','username']]

    # Pivot the interests into columns
    df_pivot = df_interests_new.pivot_table(index='username', columns='combined_interests', aggfunc=lambda x: 1, fill_value=0)
    
    # Rename column to allow data to be ingested properly
    df_pivot.rename(columns={'TV and Film': 'TV_and_Film'}, inplace=True)

    # Write the pivoted data to SQL
    df_pivot.to_sql('DimUserInterest_manual', engine, if_exists='append')
    print('Data loaded into table UserInterests')

if __name__ =="__main__":
    load_data_to_sql()
