import geopy
import pandas
import openpyxl
import math
from openpyxl import load_workbook
from geopy.geocoders import Nominatim

print("Plotting locations...")

###################### GLOBAL VARIABLES ########################################
all_locations = pandas.read_excel("all_locations.xlsx",sheetname="FROM_TO_COMBINED")
nom = geopy.Nominatim()

###################### FUNCTION DEFINITIONS ####################################

def update_metadata_to_excel(dataframe, sheetname):
	book = load_workbook('all_locations.xlsx')
	writer = pandas.ExcelWriter('all_locations.xlsx', engine='openpyxl')
	writer.book = book
	writer.sheets = dict((ws.title, ws) for ws in book.worksheets)
	dataframe.to_excel(writer, sheetname)
	writer.save()

# ------------------------------------------------------------------------------

def update_node_location_in_excel():

	all_locations["SEARCH_LOCATION"] = all_locations["STN NAME"] + ", India"
	print("plotting location, it may take some time...")

	all_locations["RAW_LOCATION"] = all_locations["SEARCH_LOCATION"].apply(nom.geocode)
	all_locations["LAT"] = all_locations["RAW_LOCATION"].apply(lambda x: x.latitude if x != None else None)
	all_locations["LONG"] = all_locations["RAW_LOCATION"].apply(lambda x: x.longitude if x != None else None)

	update_metadata_to_excel(all_locations, "metadata")

# ------------------------------------------------------------------------------

###################### MAIN ####################################################
A = nom.geocode("Bengaluru, India")
print("Bengaluru location: ")
print(A)

print("plotting locations..")
update_node_location_in_excel()

# TODO
#feature_group.add_child(folium.LatLngPopup())
