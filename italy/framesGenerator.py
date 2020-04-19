import pandas
import math
import numpy as np
import datetime
from datetime import datetime as inner_datetime
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plot
import matplotlib.patches as patches

DATAPATH = "./data/"
FILENAMES = ["confirmed.csv", "deaths.csv", "recovered.csv"]
FRAMESPATH = "./frames/"

FPS = 30
SECONDS_PER_DAY = 1.5
FRAMES_PER_DAY = int(FPS * SECONDS_PER_DAY)

# DATASET LOAD
confirmed = pandas.read_csv(DATAPATH + FILENAMES[0], sep=",")
deaths = pandas.read_csv(DATAPATH + FILENAMES[1], sep=",")
recovered = pandas.read_csv(DATAPATH + FILENAMES[2], sep=",")


# FIGURE INITIALIZATION
fig = plot.figure(dpi=600, frameon=False)


# MAP INITIALIZATION
world_map = Basemap(projection='cyl', lat_0=0, lon_0=0, resolution='c')
world_map.fillcontinents(color='black', lake_color='#404040')
world_map.drawcountries(linewidth=0.25, color="grey")
world_map.drawcoastlines(linewidth=0.25, color="grey")
world_map.drawmapboundary(fill_color='#404040', linewidth=0)


keys = [key for key in confirmed]

# PREPARING THE DATE INDICATOR
first_date = inner_datetime.strptime(keys[4], '%m/%d/%y').date()
last_date = inner_datetime.strptime(keys[-1], '%m/%d/%y').date()


days_range = datetime.timedelta(days=8)

starting_date = first_date - days_range
ending_date = last_date + days_range

date_range = ending_date - starting_date

dates_string = ""

for i in range(date_range.days + 1):
	current_date = starting_date + datetime.timedelta(days=i)
	dates_string += (current_date.strftime("%d/%m/%y") + "  ")

dates_string = dates_string[:-2]
# print(dates_string)

dates_string_position = 0
#dates_string_position = -1064.073


date_indicator = plot.text(0, -90, "△", ha='left', va='bottom', size=5, color='red', weight="extra bold")

# PREPARING THE DAILY ARRAYS
confirmed_per_day = confirmed.sum(axis=0, skipna=True)
deaths_per_day = deaths.sum(axis=0, skipna=True)
recovered_per_day = recovered.sum(axis=0, skipna=True)

# SAVING THE FRAMES
frame_number = 0
for index in range(4, len(keys) - 1):
	confirmed_variation_matrix = confirmed[keys[index + 1]] - confirmed[keys[index]]
	confirmed_increment_matrix = confirmed_variation_matrix / FRAMES_PER_DAY
	current_day_confirmed_matrix = confirmed[keys[index]]

	confirmed_variation = confirmed_per_day[keys[index + 1]] - confirmed_per_day[keys[index]]
	confirmed_increment = confirmed_variation / FRAMES_PER_DAY
	current_day_confirmed = confirmed_per_day[keys[index]]

	deaths_variation = deaths_per_day[keys[index + 1]] - deaths_per_day[keys[index]]
	deaths_increment = deaths_variation / FRAMES_PER_DAY
	current_day_deaths = deaths_per_day[keys[index]]

	recovered_variation = recovered_per_day[keys[index + 1]] - recovered_per_day[keys[index]]
	recovered_increment = recovered_variation / FRAMES_PER_DAY
	current_day_recovered = recovered_per_day[keys[index]]

	for frame in range(FRAMES_PER_DAY):
		scatter = world_map.scatter(confirmed['Long'], confirmed['Lat'], s=np.sqrt(current_day_confirmed_matrix * 80), alpha=0.6, c='#ff0000', zorder=4)

		confirmed_text = plot.text(-175, -30, "Confirmed: " + str(current_day_confirmed), ha='left', va='bottom', size=8, color='white', family="monospace", in_layout=False)
		deaths_text = plot.text(-175, -40, "Deaths: " + str(current_day_deaths), ha='left', va='bottom', size=8, color='white', family="monospace", in_layout=False)
		recovered_text = plot.text(-175, -50, "Recovered: " + str(current_day_recovered), ha='left', va='bottom', size=8, color='white', family="monospace", in_layout=False)

		#dates_text = plot.text(dates_string_position, -85, dates_string, ha='center', va='bottom', size=4, color='white', family="monospace", in_layout=False, snap=True)

		plot.savefig(FRAMESPATH + str(frame_number) + '.png', bbox_inches='tight')

		scatter.remove()
		confirmed_text.remove()
		deaths_text.remove()
		recovered_text.remove()
		# dates_text.remove()

		frame_number += 1
		#dates_string_position -= 24 / FRAMES_PER_DAY
		current_day_confirmed_matrix += confirmed_increment_matrix
		current_day_confirmed = int(current_day_confirmed + confirmed_increment)
		current_day_deaths = int(current_day_deaths + deaths_increment)
		current_day_recovered = int(current_day_recovered + recovered_increment)
