import time
import copy
import csv
import simplejson as json

def rounders(d,r):
	if (d == "NA"):
		return "null"
	else:
		return round(float(d), r) 

def floater(d):
	if (d == "NA"):
		return "null"
	else:
		return float(d) 		

# load the overarching csv
with open('cardTest.csv', 'rb') as f:
    reader = csv.reader(f)
    rows = list(reader)

with open('stickers.csv', 'rb') as ff:
    reader = csv.reader(ff)
    stickers = list(reader)

# Load the templates
with open('pre.json') as pre_data:
    pre = json.load(pre_data)

output = copy.deepcopy(pre)
index = {}

timeNow = time.strftime("%H:%M:%S")
print timeNow
output["metadata"]["name"] = "Marathon @ " + timeNow
# # print groupTemplate
# # print tempGroupTemplate
# # tempGroupTemplate["lead"] = "Group Lead Test"
# # print groupTemplate
# # print tempGroupTemplate
# print groupTemplate
# tempGroupTemplate = groupTemplate.copy()

for i in range(1, len(rows)):
	cardNum = rows[i][0]
	if cardNum not in index:
		index[cardNum] = {}			
		# declare the variables for the group

		with open('JSONtemplates/groupTemplate.json') as groupTemplate_data:
		    groupTemplate = json.load(groupTemplate_data)    

		groupTemplate["metadata"]["name"] = rows[i][6]
		groupTemplate["title"] = "Group title Test"
		groupTemplate["lead"] = "Group Lead Test"
		groupTemplate["text"] = rows[i][10]
		groupTemplate["id"] = cardNum

		# Make the group
		output["groups"].append(groupTemplate)
		# print output

# for every group, create polygons inside that group/card if they have the correct ID
for j in range(0, len(output["groups"])):
	for i in range(1,len(rows)):	
		if rows[i][0] == output["groups"][j]["id"]:
		
			url = "editedshps/finished/json/" + rows[i][1]
			# Open GeoJSON from the csv row
			with open(url) as json_data:
			    d = json.load(json_data)

			# for each item of MultiPolygon, create a polygon in eartheos

			if d["features"][0]["geometry"]["type"] == "MultiPolygon":
				for k in range(0, len(d["features"][0]["geometry"]["coordinates"])):

					with open('JSONtemplates/polygonTemplate.json') as polygonTemplate_data:
						polygonTemplate = json.load(polygonTemplate_data)

					polygonTemplate["title"] = rows[i][3]
					polygonTemplate["lead"] = rows[i][4]
					polygonTemplate["text"] = rows[i][5]					
					polygonTemplate["style"]["color"] = rows[i][2]
					polygonTemplate["camera"]["lat"] = float(rows[i][7])
					polygonTemplate["camera"]["lon"] = float(rows[i][8])
					polygonTemplate["camera"]["height"] = float(rows[i][9])
					polygonTemplate["camera"]["duration"] = float(rows[i][12])

					# custom part vv
					if j == 9:					
						polygonTemplate["youtube"] = "F-eMt3SrfFU"

					bounds = []

					for x in range(0,len((d["features"][0]["geometry"]["coordinates"][k][0]))):
						longitude = d["features"][0]["geometry"]["coordinates"][k][0][x][0]
						latitude = d["features"][0]["geometry"]["coordinates"][k][0][x][1]
						bounds.append([latitude,longitude])

					polygonTemplate["bounds"] = bounds

					# print pre["groups"][0]["layers"][0]["polygons"][0]["bounds"]
					# If its in the header, put it in the header else put it in the regular spot
					if output["groups"][j]["id"] == "0":		
						output["layers"][0]["polygons"].append(polygonTemplate)
					else: 
						output["groups"][j]["layers"][1]["polygons"].append(polygonTemplate)
			elif d["features"][0]["geometry"]["type"] == "Polygon":
				with open('JSONtemplates/polygonTemplate.json') as polygonTemplate_data:
					polygonTemplate = json.load(polygonTemplate_data)

				polygonTemplate["title"] = rows[i][3]
				polygonTemplate["lead"] = rows[i][4]
				polygonTemplate["text"] = rows[i][5]
				polygonTemplate["style"]["color"] = rows[i][2]
				polygonTemplate["camera"]["lat"] = float(rows[i][7])
				polygonTemplate["camera"]["lon"] = float(rows[i][8])
				polygonTemplate["camera"]["height"] = float(rows[i][9])

				bounds = []

				for x in range(0,len((d["features"][0]["geometry"]["coordinates"][0]))):
					longitude = d["features"][0]["geometry"]["coordinates"][0][x][0]
					latitude = d["features"][0]["geometry"]["coordinates"][0][x][1]
					bounds.append([latitude,longitude])

				polygonTemplate["bounds"] = bounds

				# print pre["groups"][0]["layers"][0]["polygons"][0]["bounds"]

				output["groups"][j]["layers"][1]["polygons"].append(polygonTemplate)
			else:	
				print "error in coords and polygon type"

output["groups"][0]["layers"][1]["polygons"][0]["audioURL"] = "https://github.com/DanielJWood/dunkirk/blob/master/guns.mp3?raw=true"

# Add in stickers

# for every group, create stickers inside that group/card if they have the correct ID
for j in range(0, len(output["groups"])):
	for i in range(1,len(stickers)):	
		if stickers[i][0] == output["groups"][j]["id"]:
			# url = "editedshps/finished/json/" + rows[i][1]
			# Open GeoJSON from the csv row
			# with open(url) as json_data:
			#     d = json.load(json_data)

			# for each item of MultiPolygon, create a polygon in eartheos

			# if d["features"][0]["geometry"]["type"] == "MultiPolygon":
			# 	for k in range(0, len(d["features"][0]["geometry"]["coordinates"])):

			with open('JSONtemplates/stickerTemplate.json') as stickerTemplate_data:
				stickerTemplate = json.load(stickerTemplate_data)

			# print stickers[i][1]


			stickerTemplate["title"] = stickers[i][1]
			stickerTemplate["stickerImage"] = stickers[i][2]
			stickerTemplate["ll"]["lat"] = float(stickers[i][3])
			stickerTemplate["ll"]["lon"] = float(stickers[i][4])
			
			ratio = float(stickers[i][5])
			width = float(stickers[i][6])
			stickerTemplate["ur"]["lat"] = stickerTemplate["ll"]["lat"] + (width/ratio)
			stickerTemplate["ur"]["lon"] = stickerTemplate["ll"]["lon"] + width

			print stickerTemplate
			# Works to get the stickers into the "layers" item but it doesn't show up on the map along iwht the polygons
			# Can there only be polygons OR lines OR points OR stickers per group
			output["groups"][j]["layers"][0]["stickers"].append(stickerTemplate)


# output["layers"][0]["polygons"][0]["audioURL"] = "https://github.com/DanielJWood/dunkirk/blob/master/guns.mp3?raw=true"
# output["layers"][0]["polygons"][0]["title"] = "Prewar boundaries"

# print output["layers"][0]["polygons"][0]["audioURL"]

# print May10["features"][0]["geometry"]["type"]
# print len(May10["features"][0]["geometry"]["coordinates"]) #Number of polygons
# print len(May10["features"][0]["geometry"]["coordinates"][i]) #Index at polygon
# print len(May10["features"][0]["geometry"]["coordinates"][i][0]) #number of coord-pairs on that polygon
# print len(May10["features"][0]["geometry"]["coordinates"][i][0][j]) #Pair of coordinates
# print len(May10["features"][0]["geometry"]["coordinates"][i][0][j][0]) #Longitude
# print len(May10["features"][0]["geometry"]["coordinates"][i][0][j][1]) #latitude

# print output

with open('dunkirk.json', 'w') as f:
    json.dump(output, f)    

