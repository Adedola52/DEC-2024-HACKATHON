# DEC 2024 HACKATHON
## CASE STUDY
As a data engineer at a travel agency, you have been tasked with integrating data from a public REST API for countries information. This data will be used to recommend travel destinations to our customers based on some different factors like language, continents, regions, currency and many more

## Data Integration Process:

- *Extract:* Extracted global country data from the public REST API https://restcountries.com/v3.1/all using a GET request
- *Transform:* Parsed and normalized the JSON response into a structured DataFrame using Python and the Pandas library. Cleaned and prepared the data for loading.
- *Load:* Loaded the cleaned and transformed DataFrame into SQL Server
  
## Storage:
- Established a connection to a SQL Server database using ODBC driver
- Exported the cleaned and transformed DataFrame directly into a database for storage and querying

## Serve:
Connected the SQL Server database to a BI tool (Power BI) to create interactive dashboards and visualizations that showcase insights from the Country data

## A
![image alt](https://github.com/Adedola52/DEC-2024-HACKATHON/blob/2ec7e58116384189b7bffe6ba9bc8f56f0b4fc39/Architecture%20flow.png)

## Insights
- There are 7 continents, and at least 3 countries are transcontinental Russia, Turkey, and Azerbaijan as they span more than one continent. This overlap leads some to loosely describe the landmass as 8 continental regions,
  though officially, the number of continents remains seven.

- Asia has the largest population, with approximately 4.5 billion people, followed by Africa with about 1.36 billion. Antarctica has the smallest population, with around 1,430 people.
This population distribution explains why China and India, both in Asia, are the most populous countries, each with approximately 1.4 billion people.

- Bouvet Island, along with Heard Island and McDonald Islands, are uninhabited territories with zero population. Though located in or near the Antarctic region, they are not recognized as independent countries.

- There are 250 recognized countries and territories globally, but only 192 are United Nations member states.  Among these, approximately 59 out of 91 English-speaking countries have English as an official language.
- Asia has the largest land area at approximately 31,253,314 sq km, followed by Africa with 30,318,357 sq km. Europe has the smallest continental area at 5,986,055.46 sq km.
At the country level, Russia is the largest in the world with 17,098,242 sq km, spanning both Europe and Asia (EuropeAsia), which explains its massive size. On the other end, the two smallest countries
Vatican City (0.44 sq km) and Monaco (2.02 sq km) are both located in Europe, aligning with the continent's smaller total land area.

- There are 55 countries that are yet to gain full independence.

- Africa has the highest number of countries, with a total of 58.



