# import libraries
import pandas as pd 
from sqlalchemy import create_engine
import pyodbc as odbc
import json
import os 
import requests
import logging  

logging.basicConfig(filename='Api.log',
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s')

def api_call():
    """
      Makes an API call to get country data, turns it into a DataFrame, and saves it as a CSV file.
      If the file already exists, it reads the data from there to avoid repeated API requests.
      Handles common request errors.
    """

    data_folder = os.getenv("data_folder") 
    file_path = f"{data_folder}/data_frame.csv"
    url = "https://restcountries.com/v3.1/all"

    if os.path.exists("data_frame.csv"):
        country_data = pd.read_csv("data_frame.csv")
        logging.info("Data loaded from csv")

    else:
        try:
            request_call = requests.get(url, timeout=10)
            request_call.raise_for_status() 
            flat_table = request_call.json()
            normalized_table = pd.json_normalize(flat_table)
            country_data = pd.DataFrame(normalized_table)
            country_data.to_csv(file_path, index=False) 
            logging.info("Country_data saved")
        except  requests.exceptions.HTTPError as errh:
            logging.error(f"HTTP Error: {errh}")

        except requests.exceptions.ConnectionError as errc:
            logging.error(f"Connection Error:{errc}")

        except requests.exceptions.Timeout as errt:
            logging.error(f"Timeout Error: {errt}")

        except requests.exceptions.RequestException as errr:
            logging.error(f"Something went wrong:{errr}")
    return country_data


def country_data_columns():
    """ 
       Loads the DataFrame from an API request or a local CSV file. Raises an error if the data is empty.
       Performs data cleaning by selecting relevant columns, renaming them, extracting values from lists,
       standardizing country codes, and handling missing or invalid values where necessary.

      """
    country_data = api_call()
    if country_data.empty:
        logging.error("DataFrame is empty")
        return country_data
    selected_column=['name.common','independent','unMember','startOfWeek','name.official','name.nativeName.tsn.official',
         'currencies.EUR.symbol','currencies.EUR.name','currencies.USD.symbol','currencies.USD.name',
         'idd.root','idd.suffixes','capital','region','subregion',
         'languages.eng','languages.tsn','area','population',
         'continents']
    country_data = country_data[selected_column]

    column_rename = {'name.common':'Country_name','independent':'Independence','unMember':'UN_members',
                      'name.official':'Official_country_name','name.nativeName.tsn.official':'Common_native_name',
         'currencies.EUR.symbol':'eur_currency_symbol','currencies.EUR.name':'eur_currency_name',
         'currencies.USD.symbol':'usd_currency_symbol','currencies.USD.name':'usd_currency_name',
         'languages.eng':'languages', 'languages.tsn':'Native_language'}
    country_data=country_data.rename(columns= column_rename)
    
    for columns in ['continents','idd.suffixes','capital']:
        country_data[columns] = country_data[columns].astype('str').replace(r'\W', '', regex=True)


    country_data["idd.root"]= "+" + country_data["idd.root"].astype('str').replace('.0', '', regex=True)
    country_data['Country_code'] = country_data['idd.root'] + country_data['idd.suffixes']
    country_data['Country_code'] = country_data['Country_code'].astype('str').replace('+nannan', None).str[:4]
    country_data['capital'] = country_data['capital'].astype('str').replace('nan', None)
    country_data=country_data.drop(['idd.root','idd.suffixes'], axis=1)
    logging.info("Data cleaning successful!")
    return country_data
    


def db_connection():
    """
      Connects to a SQL Server database using credentials stored in environment variables.
      Uses the ODBC driver to establish the connection and exports the cleaned country data
      to specified database

    """

    try:
        country_data = country_data_columns()

        DB_HOST = os.getenv("DB_HOST") 
        DB_NAME = os.getenv("DB_NAME")

        connection_string = f"mssql+pyodbc://{DB_HOST}/{DB_NAME}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes" 
        engine = create_engine(connection_string)

        country_data.to_sql(name='country_data', con=engine ,if_exists='replace', index=False)
        logging.info("Country data exported to database successfully")
    except Exception as e:
        logging.error(f'An unexpected error occurred: {e}')


db_connection()


