# import libraries
import pandas as pd 
from sqlalchemy import create_engine
import pyodbc as odbc
import json
import os 
import requests 

# Retrieve the value stored in the environment variable
data_folder = os.getenv("data_folder") 
file_path = f"{data_folder}/data_frame.csv" 

#  Define a function that either loads data from a CSV file if it exists
# or makes an API call to fetch the data and saves it to a CSV file 
def api_call():
    if os.path.exists("data_frame.csv"):
        print("Data loaded")
        country_data = pd.read_csv("data_frame.csv")

    else:
        try:
            request_call = requests.get("https://restcountries.com/v3.1/all", timeout=10)
            request_call.raise_for_status() 
            flat_table = request_call.json()
            normalized_table = pd.json_normalize(flat_table)
            country_data = pd.DataFrame(normalized_table)
            country_data.to_csv(file_path, index=False) 
            print("Country_data saved")
        except  requests.exceptions.HTTPError as errh:
            print("HTTP Error:")

        except requests.exceptions.ConnectionError as errc:
            print("Connection Error:")

        except requests.exceptions.Timeout as errt:
            print("Timeout Error:")

        except requests.exceptions.RequestException as errr:
            print("Something went wrong:")
    return country_data

country_data = api_call()

# check for null values
country_data.isnull().sum()

# select neccesary columns
country_data=country_data[['name.common','independent','unMember','startOfWeek','name.official','name.nativeName.tsn.official',
         'currencies.EUR.symbol','currencies.EUR.name','currencies.USD.symbol','currencies.USD.name',
         'idd.root','idd.suffixes','capital','region','subregion',
         'languages.eng','languages.tsn','area','population',
         'continents']]

# rename columns
country_data=country_data.rename(columns={'name.common':'Country_name','independent':'Independence','unMember':'UN_members',
                      'name.official':'Official_country_name','name.nativeName.tsn.official':'Common_native_name',
         'currencies.EUR.symbol':'eur_currency_symbol','currencies.EUR.name':'eur_currency_name',
         'currencies.USD.symbol':'usd_currency_symbol','currencies.USD.name':'usd_currency_name',
         'languages.eng':'languages', 'languages.tsn':'Native_language'})


# check for datatypes
country_data.dtypes

# print 5 rows of the dataframe
print(country_data.head())

# convert list columns to values
country_data[['continents','idd.suffixes','capital']]=country_data[['continents','idd.suffixes','capital']].astype('str').replace(r'\W', '', regex=True) 

# print 5 rows of the dataframe
print(country_data.head())


# concatenate idd.root and idd.suffixes to make country codes
country_data["idd.root"]= "+" + country_data["idd.root"].astype('str').replace('.0', '', regex=True)
country_data['Country_code']=country_data['idd.root'] + country_data['idd.suffixes']

pd.set_option("display.max_columns", None)

print(country_data.head())

# drop idd.root and idd.suffixes columns 
country_data=country_data.drop(['idd.root','idd.suffixes'], axis=1)

# Retrieve the value stored in the environment variables
DB_HOST = os.getenv("DB_HOST") 
DB_NAME = os.getenv("DB_NAME") 

# Connect to SQL Server database using the ODBC driver
connection_string = f"mssql+pyodbc://{DB_HOST}/{DB_NAME}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes" 
engine = create_engine(connection_string)

# exporting dataframe to database
country_data.to_sql(name='country_data', con=engine ,if_exists='replace', index=False)
