from sqlalchemy import create_engine
from sqlalchemy.engine import URL
import pypyodbc
import pandas as pd
from variables import SERVER_NAME, DATABASE_NAME, USERNAME, PASSWORD


excel_file = '' # Add you cleaned excel file location 

table_sheet_column_mapping = {
    # '<SQLtablename>' :{'<Excel sheet name>':['<Column names>'] }   
    # 'StgActivityLog':{'Usage Logs':['ActivityID','UserID','date','login_time','logout_time']},
    # 'StgInterest':{'List of Interest Topics':['InterestID','Topic']},
    'StgJobTitle':{'Accounts':['JobID','job_title']},
    'StgLocation':{'Accounts':['LocationID','city','country']},
    'StgPaymentCard':{'Accounts':['card_number','card_type','subscription']},
    'StgUser':{'Accounts':['CardNumber','username','first_name','last_name','email','gender','password','phone_number','birth_date','account_creation_date','profile_picture_URL','ip_address']},
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


    for table_name, sheet_column_mapping in table_sheet_column_mapping.items():
        for sheet_name, columns in sheet_column_mapping.items():
            df_data = pd.read_excel(excel_file, sheet_name=sheet_name)
            selected_columns = [col for col in columns if col in df_data.columns]
            if selected_columns:
                df_selected = df_data[selected_columns]
                df_selected.to_sql(table_name, engine, if_exists='append', index=False)
                print(f'Data loaded into table {table_name} from sheet {sheet_name}')
            else:
                print(f'No columns specified for table {table_name} in sheet {sheet_name}')

if __name__ =="__main__":
    load_data_to_sql()
