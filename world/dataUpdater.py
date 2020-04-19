import requests
FILEPATH = "./data/"
URLS = [
	"https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv",
	"https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv",
	"https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv"
]
FILENAMES = ["confirmed.csv", "deaths.csv", "recovered.csv"]

for index in range(3):
	tmp_content = requests.get(URLS[index])
	tmp_file = open(FILEPATH + FILENAMES[index], 'wt')
	tmp_text = tmp_content.text.replace('\n', '')
	tmp_file.write(tmp_text)
	tmp_file.close()
