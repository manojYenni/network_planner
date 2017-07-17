import folium
import geopy
import pandas
import openpyxl
import math
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
popup_width = 150
popup_height = 60
iframe_max_width = 500
metadata_sheetname = "Nodes_metadata"
nom = geopy.Nominatim()

###################### FUNCTION DEFINITIONS ####################################
def get_marker_color(node_type):
	if node_type == "S":
		return "purple"
	elif node_type == "T":
		return "red"
	elif node_type == "M":
		return "green"
	elif node_type == "R":
		return "orange"
	elif node_type == "L":
		return "blue"
	else:
		return "gray"

# ------------------------------------------------------------------------------

def update_metadata_to_excel(dataframe, sheetname):
	book = load_workbook('master_nodes.xlsx')
	writer = pandas.ExcelWriter('master_nodes.xlsx', engine='openpyxl')
	writer.book = book
	writer.sheets = dict((ws.title, ws) for ws in book.worksheets)
	dataframe.to_excel(writer, sheetname)
	writer.save()

# ------------------------------------------------------------------------------

def update_node_location_in_excel():
	maps_metadata_df["FROM_EDITED"] = maps_data_df["FROM"] + ", India"
	maps_metadata_df["FROM_COORDINATES"]= maps_metadata_df["FROM_EDITED"].apply(nom.geocode)
	maps_metadata_df["FROM_COORDINATES"] = maps_metadata_df["FROM_COORDINATES"].apply(lambda x:str(x.latitude) + "," + str(x.longitude) if x != None else None )

	maps_metadata_df["TO_EDITED"] = maps_data_df["TO"] + ", India"
	maps_metadata_df["TO_COORDINATES"]= maps_metadata_df["TO_EDITED"].apply(nom.geocode)
	maps_metadata_df["TO_COORDINATES"] = maps_metadata_df["TO_COORDINATES"].apply(lambda x:str(x.latitude) + "," + str(x.longitude) if x != None else None )
	update_metadata_to_excel(maps_metadata_df, metadata_sheetname)
	print("flattening")
	column_header = list(maps_data_df.head(0))
	cropped_header = column_header[0:9]

# ------------------------------------------------------------------------------

def flatten_data():
	column_header = list(maps_data_df.head(0))
	cropped_header = column_header[0:9]

	for header in column_header:
		maps_data_df[header] = pandas.Series(maps_data_df[header]).fillna(value="padding")

# ------------------------------------------------------------------------------

def plot_amplifiers(offset):
	number_of_amplifiers = maps_data_df.loc[offset,"AMPLIFIERS"] + 1
	for i in range(0, number_of_amplifiers):
		maps_metadata_df.loc[offset+i, "FROM_EDITED"] = maps_data_df.loc[offset+i, "AMPLIFIER FROM"] + " ,India"
		raw_location = nom.geocode(maps_metadata_df.loc[offset+i, "FROM_EDITED"])
		maps_metadata_df.loc[offset+i,"FROM_COORDINATES"] =  str(raw_location.latitude) + "," + str(raw_location.longitude)

		maps_metadata_df.loc[offset+i, "TO_EDITED"] = maps_data_df.loc[offset+i, "AMPLIFIER TO"] + " ,India"
		raw_location = nom.geocode(maps_metadata_df.loc[offset+i, "TO_EDITED"])
		maps_metadata_df.loc[offset+i,"TO_COORDINATES"] =  str(raw_location.latitude) + "," + str(raw_location.longitude)
		# if i != 0:
		# 	feature_group.add_child(folium.RegularPolygonMarker([raw_location.latitude, raw_location.longitude],popup=from_original, fill_color='#132b5e', number_of_sides=3, radius=10))
		# else:
		# 		marker_color = get_marker_color(maps_data_amp.loc[i,"FROM NODE TYPE"])
		# 		feature_group.add_child(folium.Marker(location=[raw_location.latitude, raw_location.longitude],popup=from_original,icon=folium.Icon(color=marker_color)))

		# maps_data_amp.loc[offset+i,"AMPLIFIER_TO_COORDINATES"] = nom.geocode(maps_data_amp.loc[offset+i, "AMPLIFIER TO"])

	update_metadata_to_excel(maps_metadata_df, "Nodes_metadata")

# ------------------------------------------------------------------------------

def plot_node_markers():

	flatten_data()

	for i in maps_data_df.index:
		if ((maps_data_df.loc[i,"AMPLIFIERS"] == "None") and (maps_data_df.loc[i,"AMPLIFIERS"] != "padding")):

			print("Plotting nodes for "+ maps_data_df.loc[i,"FROM"] )
			from_coordinates = maps_metadata_df.loc[i,"FROM_COORDINATES"]
			from_coordinates = from_coordinates.split(",")

			marker_color = get_marker_color(maps_data_df.loc[i,"FROM NODE TYPE"])
			popup_html = """<b>""" + maps_data_df.loc[i,"FROM"] + """(""" + maps_data_df.loc[i,"FROM NODE TYPE"] + """)""" + """</b><br>NODE ID: """ + str(maps_data_df.loc[i,"FROM NODE ID"])
			iframe = folium.IFrame(html=popup_html, width=popup_width, height=popup_height)
			popup_object = folium.Popup(iframe, max_width=iframe_max_width)
			feature_group.add_child(folium.Marker(location=from_coordinates,popup=popup_object,icon=folium.Icon(color=marker_color)))

			to_coordinates = maps_metadata_df.loc[i,"TO_COORDINATES"]
			to_coordinates = to_coordinates.split(",")

			marker_color = get_marker_color(maps_data_df.loc[i,"TO NODE TYPE"])
			popup_html = """<b>""" + maps_data_df.loc[i,"TO"] + """(""" + maps_data_df.loc[i,"TO NODE TYPE"] + """)""" + """</b><br>NODE ID: """ + str(maps_data_df.loc[i,"TO NODE ID"])
			iframe = folium.IFrame(html=popup_html, width=popup_width, height=popup_height)
			popup_object = folium.Popup(iframe, max_width=iframe_max_width)
			feature_group.add_child(folium.Marker(location=to_coordinates,popup=popup_object,icon=folium.Icon(color=marker_color)))

			#Plotting PolyLines
			coordinates_temp = from_coordinates + to_coordinates
			coordinates_float = list(map(lambda x: float(x), coordinates_temp))
			polyline_coordinates = [ coordinates_float[0:2], coordinates_float[2:4]]
			popup_html = """D: """ + str(maps_data_df.loc[i,"DISTANCE"]) + """ km""" + """<br>LINK ID: """ + str(maps_data_df.loc[i,"LINK ID"])
			iframe = folium.IFrame(html=popup_html, width=popup_width, height=popup_height)
			popup_object = folium.Popup(iframe, max_width=iframe_max_width)
			feature_group.add_child(folium.PolyLine(locations=polyline_coordinates,weight=5,popup=popup_object))

		elif maps_data_df.loc[i,"AMPLIFIERS"] != "padding":
			print("Plotting amplifiers for "+ maps_data_df.loc[i,"FROM"] )

			from_coordinates = maps_metadata_df.loc[i,"FROM_COORDINATES"]
			from_coordinates = from_coordinates.split(",")

			marker_color = get_marker_color(maps_data_df.loc[i,"FROM NODE TYPE"])
			popup_html = """<b>""" + maps_data_df.loc[i,"FROM"] + """(""" + maps_data_df.loc[i,"FROM NODE TYPE"] + """)""" + """</b><br>NODE ID: """ + str(maps_data_df.loc[i,"FROM NODE ID"])
			iframe = folium.IFrame(html=popup_html, width=popup_width, height=popup_height)
			popup_object = folium.Popup(iframe, max_width=iframe_max_width)
			feature_group.add_child(folium.Marker(location=from_coordinates,popup=popup_object,icon=folium.Icon(color=marker_color)))

			number_of_amplifiers = maps_data_df.loc[i,"AMPLIFIERS"]
			to_coordinates = maps_metadata_df.loc[i+number_of_amplifiers,"TO_COORDINATES"]
			to_coordinates = to_coordinates.split(",")

			marker_color = get_marker_color(maps_data_df.loc[i,"TO NODE TYPE"])
			popup_html = """<b>""" + maps_data_df.loc[i,"TO"] + """(""" + maps_data_df.loc[i,"TO NODE TYPE"] + """)""" + """</b><br>NODE ID: """ + str(maps_data_df.loc[i,"TO NODE ID"])
			iframe = folium.IFrame(html=popup_html, width=popup_width, height=popup_height)
			popup_object = folium.Popup(iframe, max_width=iframe_max_width)
			feature_group.add_child(folium.Marker(location=to_coordinates,popup=popup_object,icon=folium.Icon(color=marker_color)))

			plot_amplifiers(i)

		else:
			print("Ignoring dummy data at " + str(i))

# ------------------------------------------------------------------------------

###################### MAIN ####################################################
choice = input("Do you want to re-plot the coordinates?[y/n]: ")

if choice == "y":
	print("Updating location details..")
	update_node_location_in_excel()
	print("plotting markers..")
	plot_node_markers()
elif choice == "n":
	print("plotting markers..")
	plot_node_markers()
else:
	print("invalid choice")

# TODO
#feature_group.add_child(folium.LatLngPopup())

Main_map_object.add_child(feature_group)
Main_map_object.save("maps1.html")
