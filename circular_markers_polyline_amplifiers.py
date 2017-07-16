import folium
import geopy
import pandas
from geopy.geocoders import Nominatim

print("Beginning to map multiple markers...")

###################### GLOBAL VARIABLES ########################################

maps_dataframe = pandas.read_excel("nodes_updated_info_from_to_with_amplifiers.xlsx")
Delhi_location = [12.9791198,77.5912997]

Map_with_delhi_as_default_location = folium.Map(location=Delhi_location, tiles="Mapbox Bright")
feature_group = folium.FeatureGroup(name = "my map")
marker_radius_in_pixel = 6
nom = geopy.Nominatim()
amplifier_link=0

################################################################################

###################### FUNCTION DEFINITIONS ####################################

def get_marker_color(node_type):

	if node_type == "S":
		return "pink"
	elif node_type == "T":
		return "red"
	elif node_type == "M":
		return "lightgreen"
	else:
		return "lightblue"

################################################################################

def plot_amplifiers(coordinates_src,coordinates_dest,amplifiers_string):

#	src_lat = str(coordinates_src[0])
#	src_long = str(coordinates_src[1])
#	dest_lat = str(coordinates_dest[0])
#	dest_long = str(coordinates_dest[1])

#	coordinates_src = [src_lat,src_long]
#	coordinates_dest = [dest_lat,dest_long]

	list_of_amplifiers = amplifiers_string.split(", ")
	amplifier_link = [ coordinates_src ]

	for x in list_of_amplifiers:
		print(x)
		location_string = x +", India"
		raw_location = nom.geocode(location_string)
		coordinates = [str(raw_location.latitude),str(raw_location.longitude)]
		print("C: " + str(raw_location.latitude) + " "+ str(raw_location.longitude ) )
		feature_group.add_child(folium.CircleMarker(location=coordinates,radius=marker_radius_in_pixel, popup=x,fill_color='black',color='black',fill_opacity=0.7))
		amplifier_link =  amplifier_link + [coordinates]

	print(amplifier_link)
	amplifier_link = amplifier_link + [coordinates_dest]
#	print("FINAL:")
#	print(amplifier_link)

	for j in range(1,len(amplifier_link)):
		if j == (len(amplifier_link) + 1):
			print("Reached end of list")
			lat1 = float(amplifier_link[j-2][0])
			long1 = float(amplifier_link[j-2][1])
			lat2 = float(amplifier_link[j-1][0])
			long2 = float(amplifier_link[j-1][1])
			polyline_coordinates = [[lat1,long1],[lat2,long2]]
#			polyline_coordinates = [float(amplifier_link[j-2]),float(amplifier_link[j-1])]
			feature_group.add_child(folium.PolyLine(locations=polyline_coordinates,weight=5))
		else:
#			print("intermediate: ",amplifier_link[j-1])
#			print(amplifier_link[j])
#			print("\n")
			lat1 = float(amplifier_link[j-1][0])
			long1 = float(amplifier_link[j-1][1])
			lat2 = float(amplifier_link[j][0])
			long2 = float(amplifier_link[j][1])
			polyline_coordinates = [[lat1,long1],[lat2,long2]]
			#[["12.9791198", "77.5912997"], ["12.1347988", "78.1589864"]]
			feature_group.add_child(folium.PolyLine(locations=polyline_coordinates,weight=5))

			print("P: ",polyline_coordinates)


#		polyline_coordinates = [[ maps_dataframe.iloc[i,3], maps_dataframe.iloc[i,4] ],[ maps_dataframe.iloc[i,6], maps_dataframe.iloc[i,7] ]]

################################################################################

###################### MAIN LOOP ###############################################

for i in maps_dataframe.index:
	#    print( "-> " + str(i) + "LAT: " + str(maps_dataframe.iloc[i,3]) + " LONG: " + str(maps_dataframe.iloc[i,4]))
	coordinates_src = [ maps_dataframe.iloc[i,3], maps_dataframe.iloc[i,4] ]
	popup_message_src = maps_dataframe.iloc[i,0] + "(" + maps_dataframe.iloc[i,8] + ")"
	marker_color_src = get_marker_color(maps_dataframe.iloc[i,8])
	feature_group.add_child(folium.CircleMarker(location=coordinates_src,radius=marker_radius_in_pixel, popup=popup_message_src,fill_color=marker_color_src,color='grey',fill_opacity=0.7))

	coordinates_dest = [ maps_dataframe.iloc[i,6], maps_dataframe.iloc[i,7] ]
	popup_message_dest = maps_dataframe.iloc[i,1] + "(" + maps_dataframe.iloc[i,9] + ")"
	marker_color_dest = get_marker_color(maps_dataframe.iloc[i,9])
	feature_group.add_child(folium.CircleMarker(location=coordinates_dest,radius=marker_radius_in_pixel, popup=popup_message_dest,fill_color=marker_color_dest,color='grey',fill_opacity=0.7))

	amplifiers_string = maps_dataframe.iloc[i,10]

	if amplifiers_string == "None":
		polyline_coordinates = [[ maps_dataframe.iloc[i,3], maps_dataframe.iloc[i,4] ],[ maps_dataframe.iloc[i,6], maps_dataframe.iloc[i,7] ]]
		feature_group.add_child(folium.PolyLine(locations=polyline_coordinates,weight=5))
	else:
	    plot_amplifiers(coordinates_src,coordinates_dest,amplifiers_string)

################################################################################

###################### SAVE MAPS ###############################################

Map_with_delhi_as_default_location.add_child(feature_group)
Map_with_delhi_as_default_location.save("maps_amplifiers.html")

################################################################################
