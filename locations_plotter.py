import geopy
import pandas
import openpyxl
import math
import time
from openpyxl import load_workbook
from geopy.geocoders import Nominatim

print("Plotting locations...")

###################### GLOBAL VARIABLES ########################################
all_locations = pandas.read_excel("all_locations_temp.xlsx",sheetname="FROM_TO_COMBINED")
all_locations_metadata = pandas.read_excel("all_locations_temp.xlsx",sheetname="metadata")
nom = geopy.Nominatim()

###################### FUNCTION DEFINITIONS ####################################

def update_metadata_to_excel(dataframe, sheetname):
	book = load_workbook("all_locations_temp.xlsx")
	writer = pandas.ExcelWriter("all_locations_temp.xlsx", engine="openpyxl")
	writer.book = book
	writer.sheets = dict((ws.title, ws) for ws in book.worksheets)
	dataframe.to_excel(writer, sheetname)
	writer.save()

# ------------------------------------------------------------------------------

def update_node_location_in_excel():

	all_locations_metadata["SEARCH_LOCATION"] = all_locations["STN NAME"] + ", India"
	update_metadata_to_excel(all_locations_metadata, "metadata")

	starting_index = input("Enter starting index: ")
	ending_index = input("Enter ending index: ")

	for i in range(int(starting_index),int(ending_index)):
		print("I: "+str(i)+" plotting for " + all_locations_metadata.loc[i,"SEARCH_LOCATION"])
		raw_location = nom.geocode(all_locations_metadata.loc[i,"SEARCH_LOCATION"])
		if raw_location != None:
			all_locations_metadata.loc[i,"LAT"] = raw_location.latitude
			all_locations_metadata.loc[i,"LONG"] = raw_location.longitude
		else:
			all_locations_metadata.loc[i,"LAT"] = "XXX"
			all_locations_metadata.loc[i,"LONG"] = "XXX"
		
		update_metadata_to_excel(all_locations_metadata, "metadata")

#	print("plotting location, it may take some time...")

#	all_locations["RAW_LOCATION"] = all_locations["SEARCH_LOCATION"].apply(nom.geocode)
#	all_locations["LAT"] = all_locations["RAW_LOCATION"].apply(lambda x: x.latitude if x != None else None)
#	all_locations["LONG"] = all_locations["RAW_LOCATION"].apply(lambda x: x.longitude if x != None else None)


# ------------------------------------------------------------------------------

###################### MAIN ####################################################
#A = nom.geocode("Bengaluru, India")
#print("Bengaluru location: ")
#print(A)

#print("plotting locations..")
update_node_location_in_excel()

# TODO
#feature_group.add_child(folium.LatLngPopup())
