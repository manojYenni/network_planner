import folium
import geopy
import pandas
import openpyxl
from openpyxl import load_workbook
from geopy.geocoders import Nominatim

print("Plotting nodes and amplifiers...")

###################### GLOBAL VARIABLES ########################################
maps_data_df = pandas.read_excel("master_nodes.xlsx",sheetname="Nodes")
maps_metadata_df = pandas.read_excel("master_nodes.xlsx",sheetname="Nodes_metadata")
Bengaluru_location = [12.9791198,77.5912997]
Default_location = Bengaluru_location

Main_map_object = folium.Map(location=Default_location, tiles="Mapbox Bright")
feature_group = folium.FeatureGroup(name = "my map")
circular_marker_radius_in_pixel = 6
nom = geopy.Nominatim()

###################### FUNCTION DEFINITIONS ####################################
def get_marker_color(node_type):
	if node_type == "S":
		return "purple"
	elif node_type == "T":
		return "red"
	elif node_type == "M":
		return "green"
	else:
		return "blue"

def update_metadata_to_excel(dataframe):
    book = load_workbook('master_nodes.xlsx')
    writer = pandas.ExcelWriter('master_nodes.xlsx', engine='openpyxl')
    writer.book = book
    writer.sheets = dict((ws.title, ws) for ws in book.worksheets)
    dataframe.to_excel(writer, "Nodes_metadata")
    writer.save()

def update_node_location_in_excel():
    maps_metadata_df["FROM_EDITED"] = maps_data_df["FROM"] + ", India"
    maps_metadata_df["FROM_COORDINATES"]= maps_metadata_df["FROM_EDITED"].apply(nom.geocode)
    maps_metadata_df["FROM_COORDINATES"] = maps_metadata_df["FROM_COORDINATES"].apply(lambda x:str(x.latitude) + "," + str(x.longitude) if x != None else None )

    maps_metadata_df["TO_EDITED"] = maps_data_df["TO"] + ", India"
    maps_metadata_df["TO_COORDINATES"]= maps_metadata_df["TO_EDITED"].apply(nom.geocode)
    maps_metadata_df["TO_COORDINATES"] = maps_metadata_df["TO_COORDINATES"].apply(lambda x:str(x.latitude) + "," + str(x.longitude) if x != None else None )
    update_metadata_to_excel(maps_metadata_df)

def plot_node_markers():

    for i in maps_data_df.index:
        coordinates = maps_metadata_df.loc[i,"FROM_COORDINATES"]
        coordinates = coordinates.split(",")
        marker_color = get_marker_color(maps_data_df.loc[i,"FROM NODE TYPE"])
        popup_message = maps_data_df.loc[i,"FROM"] + "(" + maps_data_df.loc[i,"FROM NODE TYPE"] + ")"
        feature_group.add_child(folium.Marker(location=coordinates,popup=maps_data_df.loc[i,"FROM"],icon=folium.Icon(color=marker_color)))

###################### MAIN ####################################################
# update_node_location_in_excel()

plot_node_markers()
Main_map_object.add_child(feature_group)
Main_map_object.save("maps1.html")