from sqlalchemy import create_engine
from sqlalchemy.engine import URL
import pypyodbc
import pandas as pd
from variables import SERVER_NAME, DATABASE_NAME, USERNAME, PASSWORD

table_column_mapping = {
    # '<SQLtablename>' :{'<csv file>':['<Column names>'] }   
    'StgActivityLog':{'User_logs_cleaned.csv':['ActivityID','UserID','date','login_time','logout_time']},
    'StgJobTitle':{'cleaned.csv':['JobID','job_title']},
    'StgLocation':{'cleaned.csv':['LocationID','city','country']},
    'StgPaymentCard':{'cleaned.csv':['card_type','subscription', 'card_number']},
    'StgUser':{'cleaned.csv':['UserID','username','first_name','last_name','email','gender','password','phone_number','birth_date','account_creation_date','profile_picture_URL','ip_address']},
}

def load_data_to_sql():
    connection_string = f"""
        DRIVER={{SQL Server}};
        SERVER={SERVER_NAME};
        DATABASE={DATABASE_NAME};
        UID={USERNAME};
        PWD={PASSWORD};
    """
    connection_url = URL.create('mssql+pyodbc', query={'odbc_connect': connection_string})
    engine = create_engine(connection_url, module=pypyodbc)


    for table_name, csv_column_mapping in table_column_mapping.items():
        for csv_name, columns in csv_column_mapping.items():
            df_data = pd.read_csv(csv_name)
            selected_columns = [col for col in columns if col in df_data.columns]
            if selected_columns and table_name == "StgPaymentCard":
                df_selected = df_data[selected_columns]
                # Card number cant be null in sql table
                df_selected = df_selected.dropna(subset=["card_number"])
                df_selected.to_sql(table_name, engine, if_exists='append', index=False)
                print(f'Data loaded into table {table_name} from csv {csv_name}')
            elif selected_columns:
                df_selected = df_data[selected_columns]
                df_selected.to_sql(table_name, engine, if_exists='append', index=False)
                print(f'Data loaded into table {table_name} from csv {csv_name}')
            else:
                print(f'No columns specified for table {table_name} in csv {csv_name}')

if __name__ =="__main__":
    load_data_to_sql()
