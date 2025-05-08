-- Create a database --
CREATE DATABASE Hackathon;

-- View data --
SELECT *
FROM datas;

-- How many countries speaks French --
SELECT count(languages) no_of_countries, languages
FROM datas
WHERE languages = 'French'
GROUP BY languages;

-- How many countries speaks english --
SELECT count(languages) no_of_countries, languages
FROM datas
WHERE languages = 'English'
GROUP BY languages;

-- How many country have more than 1 official language -- 
SELECT count(country_name) AS no_of_countries FROM datas 
WHERE languages IS NOT NULL AND Native_language IS NOT NULL;

-- How many country official currency is Euro --
SELECT count(eur_currency_symbol) AS no_of_countries FROM datas;

-- How many country is from West europe --
SELECT subregion, count(subregion) no_of_countries
FROM datas
WHERE subregion = 'Western Europe'
GROUP BY subregion;

-- How many country has not yet gain independence --
SELECT CASE WHEN independence = 1
		THEN 'Gained independence'
		ELSE 'Not gained independence'
		END AS Independence
	,count(independence) no_of_countries
FROM datas
WHERE independence = 0
GROUP BY CASE WHEN independence = 1
		THEN 'Gained independence'
		ELSE 'Not gained independence'
		END;

-- How many distinct continent and how many country from each --
SELECT continents, count(continents) OVER () no_of_distinct, 
count(country_name) no_of_countries
FROM datas
GROUP BY continents;

-- How many country whose start of the week is not Monday --
SELECT count(CASE WHEN startofweek <> 'monday'
			 THEN 1
			 END) no_of_countries
FROM datas;

-- How many countries are not a United Nation member -- 
SELECT CASE WHEN UN_members = 1
	   THEN 'Member'
	   ELSE 'Not a member'
	   END AS un_member
	,count(UN_members) no_of_countries
FROM datas
WHERE UN_members = 0
GROUP BY CASE WHEN UN_members = 1
		 THEN 'Member'
		 ELSE 'Not a member'
		 END;
		 

-- How many countries are United Nation member --
SELECT CASE WHEN UN_members = 1
	   THEN 'Member'
	   ELSE 'Not a member'
	   END AS un_member
	,count(UN_members) no_of_countries
FROM datas
WHERE UN_members = 1
GROUP BY CASE WHEN UN_members = 1
		THEN 'Member'
		ELSE 'Not a member'
		END;

-- Least 2 countries with the lowest population for each continents --
WITH cte AS (
	    SELECT continents, country_name, sum(population) AS no_of_population
		,row_number() OVER (PARTITION BY continents ORDER BY sum(population)) AS rn
	    FROM datas
	    GROUP BY continents, country_name)
SELECT continents, country_name, no_of_population
FROM cte
WHERE rn <= 2;

-- Top 2 countries with the largest Area for each continent -- 
WITH cte AS (
	        SELECT continents, country_name, sum(area) AS no_of_population
			,row_number() OVER (PARTITION BY continents ORDER BY sum(area) DESC) AS rn
		    FROM datas
		    GROUP BY continents, country_name)
SELECT continents, country_name, no_of_population
FROM cte
WHERE rn <= 2;

-- Top 5 countries with the largest Area --
SELECT TOP 5 country_name, sum(area) AS area
FROM datas
GROUP BY country_name
ORDER BY area DESC;

-- Top 5 countries with the lowest Area --
SELECT TOP 5 country_name, sum(area) AS area
FROM datas
GROUP BY country_name
ORDER BY area ASC;



