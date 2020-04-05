# encoding: utf-8
'''
cd /home/joan/projectes/OSM/fusionar_geojson/python/
PS1="$ "
$ python fusionar_geojson_master.py fitxerjson geojson1 geojson2 [radi]
Ex:
$ python fusionar_geojson_master.py masterA.json 0 1
$ python fusionar_geojson_master.py masterA.json 0 1 200
Recordar que podem intercanviar l'ordre:
$ python fusionar_geojson_master.py masterA.json 1 0

El fitxer json espera el format de ../data/masterA.json

'''
import sys
import json #parsejar JSON
from math import sin, cos, sqrt, atan2, radians #per calcular la distància entre dos punts amb coordenades GPS
import codecs

def iguals(coord1,coord2,radi):
	if radi==0:
		if coord1==coord2: return True
	else:
		if distancia(coord1,coord2) < radi: return True
	return False

def distancia(coord1,coord2):
	R = 6373000.0 #metres (és el radi de la Terra)
	lat1 = radians(float(coord1[1]))
	lon1 = radians(float(coord1[0]))
	lat2 = radians(float(coord2[1]))
	lon2 = radians(float(coord2[0]))
	dlon = lon2 - lon1
	dlat = lat2 - lat1
	a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
	c = 2 * atan2(sqrt(a), sqrt(1 - a))
	distance = R * c
	return distance

if (len(sys.argv)!=4 and len(sys.argv)!=5):
	print ("HELP:")
	print ("$ python fusionar_geojson_v5a.py fitxerjson geojson1 geojson2 [radi]")
	print ("$ python fusionar_geojson_v5a.py terres_ebre.json 0 1")
	print ("$ python fusionar_geojson_v5a.py terres_ebre.json 0 1 200")
	print ("El fitxer json espera el format de ../data/terres_ebre.json")
	print ("També podem intercanviar l'ordre: 1 0 en comptes de 1 0")
	exit(0)

fitxerjson = sys.argv[1]
geojson1 = int(sys.argv[2])
geojson2 = int(sys.argv[3])
if len(sys.argv)==5:
	radi = int(sys.argv[4])
else:
	radi=0

with open(fitxerjson, 'r') as f:
    comarques_dict = json.load(f)

#print(len(comarques_dict))

#comprovació de les coincidències entre dues comarques
# Depèn de l'origen de les dades, la coincidència de les fronteres pot ser exacta o aproximada
num_coinc = 0

for coordenades1 in comarques_dict[geojson1]['geometry']['coordinates']:
	for coordenades2 in comarques_dict[geojson2]['geometry']['coordinates']:
		#print(str(coordenades1) + " " + str(coordenades2))
		if (radi==0):
			if coordenades1 == coordenades2: num_coinc = num_coinc + 1
		else:
			if distancia(coordenades1,coordenades2) < radi: num_coinc = num_coinc + 1

print (num_coinc)
print

lon_com1 = len(comarques_dict[geojson1]['geometry']['coordinates'])
lon_com2 = len(comarques_dict[geojson2]['geometry']['coordinates'])
lon_com1b = lon_com1 - 1
lon_com2b = lon_com2 - 1


f = codecs.open("solucio.txt", "w", "utf-8")

# =============================================================================
f.write(u"====== MÀSTER A =======\n")

punt_coincidencia_com1_1 = -1
punt_coincidencia_com1_2 = -1
punt_coincidencia_com2_1 = -1
punt_coincidencia_com2_2 = -1

# cap endavant
punt_com1 = 0
for coordenades1 in comarques_dict[geojson1]['geometry']['coordinates']:
	punt_com2 = 0
	for coordenades2 in comarques_dict[geojson2]['geometry']['coordinates']:
		if iguals(coordenades1,coordenades2,radi) and punt_coincidencia_com1_1 == -1:
			print "entro a la frontera 1"
			punt_coincidencia_com1_1 = punt_com1
			punt_coincidencia_com2_1 = punt_com2
			break
		punt_com2 = punt_com2 + 1
	if punt_coincidencia_com1_1 != -1:
		break
	punt_com1 = punt_com1 + 1

# cap endarrere
punt_com1 = 0
for coordenades1 in comarques_dict[geojson1]['geometry']['coordinates'][::-1]:
	punt_com2 = 0
	for coordenades2 in comarques_dict[geojson2]['geometry']['coordinates'][::-1]:
		if iguals(coordenades1,coordenades2,radi) and punt_coincidencia_com1_2 == -1:
			print "entro a la frontera 2"
			punt_coincidencia_com1_2 = punt_com1
			punt_coincidencia_com2_2 = punt_com2
			break
		punt_com2 = punt_com2 + 1
	if punt_coincidencia_com1_2 != -1:
		break
	punt_com1 = punt_com1 + 1

print

print(punt_coincidencia_com1_1)
print(punt_coincidencia_com1_2)
print(punt_coincidencia_com2_1)
print(punt_coincidencia_com2_2)

#print lon_com1 #compte! que l'últim punt és el mateix que el primer. No hi ha 20 punts, sinó 21
#print lon_com2
#recordar que l'últim punt és el mateix que el primer
nova_comarca = comarques_dict[geojson1]['geometry']['coordinates'][0:punt_coincidencia_com1_1]
nova_comarca = nova_comarca + comarques_dict[geojson2]['geometry']['coordinates'][punt_coincidencia_com2_1:lon_com2b]
nova_comarca = nova_comarca + comarques_dict[geojson2]['geometry']['coordinates'][0:lon_com2b-punt_coincidencia_com2_2]
nova_comarca = nova_comarca + comarques_dict[geojson1]['geometry']['coordinates'][lon_com1b-punt_coincidencia_com1_2:lon_com1b]
nova_comarca = nova_comarca + comarques_dict[geojson1]['geometry']['coordinates'][0:1]
print "longitud de la nova comarca: " + str(len(nova_comarca))

#f.write(str(len(nova_comarca)) + "\n")
#f.write(str(num_coinc) + "\n")
#f.write(str(lon_com1 + lon_com2 - 2*num_coinc + 1) + "\n")
#f.write(str(abs(lon_com1 + lon_com2 - 2*num_coinc + 1 - len(nova_comarca))) + "\n")

if (abs(lon_com1 + lon_com2 - 2*num_coinc + 1 - len(nova_comarca))) > 4:
	f.write(u"NO ÉS SOLUCIÓ")
elif (lon_com1==len(nova_comarca) or lon_com2==len(nova_comarca)):
	f.write(u"NO ÉS SOLUCIÓ")
else:
	f.write(str(nova_comarca))
f.write("\n\n")

# =============================================================================
f.write(u"====== MÀSTER B =======\n")

punt_coincidencia_com1_1 = -1
punt_coincidencia_com1_2 = -1
punt_coincidencia_com2_1 = -1
punt_coincidencia_com2_2 = -1

# cap endavant
punt_prov = -1
punt_com1 = 0
for coordenades1 in comarques_dict[geojson1]['geometry']['coordinates']:
	punt_com2 = 0
	for coordenades2 in comarques_dict[geojson2]['geometry']['coordinates']:
		if iguals(coordenades1,coordenades2,radi) and punt_coincidencia_com1_1 == -1:
			punt_prov = punt_com2
			break
		punt_com2 = punt_com2 + 1

	if punt_com2 == lon_com2:
		print "surto de la frontera 1"
		punt_coincidencia_com1_1 = punt_com1 - 1
		punt_coincidencia_com2_1 = punt_prov
		break
	punt_com1 = punt_com1 + 1


# cap endarrere
punt_prov = -1
punt_com1 = 0
for coordenades1 in comarques_dict[geojson1]['geometry']['coordinates'][::-1]:
	punt_com2 = 0
	for coordenades2 in comarques_dict[geojson2]['geometry']['coordinates'][::-1]:
		if iguals(coordenades1,coordenades2,radi) and punt_coincidencia_com1_2 == -1:
			punt_prov = punt_com2
			break
		punt_com2 = punt_com2 + 1

	if punt_com2 == lon_com2:
		print "surto de la frontera 1"
		punt_coincidencia_com1_2 = punt_com1 - 1
		punt_coincidencia_com2_2 = punt_prov
		break
	punt_com1 = punt_com1 + 1

print

print(punt_coincidencia_com1_1)
print(punt_coincidencia_com1_2)
print(punt_coincidencia_com2_1)
print(punt_coincidencia_com2_2)

#recordar que l'últim punt és el mateix que el primer
nova_comarca = comarques_dict[geojson1]['geometry']['coordinates'][punt_coincidencia_com1_1:lon_com1b-punt_coincidencia_com1_2]
nova_comarca = nova_comarca + comarques_dict[geojson2]['geometry']['coordinates'][lon_com2b-punt_coincidencia_com2_2:lon_com2b]
nova_comarca = nova_comarca + comarques_dict[geojson2]['geometry']['coordinates'][0:punt_coincidencia_com2_1]
nova_comarca = nova_comarca + comarques_dict[geojson1]['geometry']['coordinates'][punt_coincidencia_com1_1:punt_coincidencia_com1_1+1]
print "longitud de la nova comarca: " + str(len(nova_comarca))

if (abs(lon_com1 + lon_com2 - 2*num_coinc + 1 - len(nova_comarca))) > 4:
	f.write(u"NO ÉS SOLUCIÓ")
elif (lon_com1==len(nova_comarca) or lon_com2==len(nova_comarca)):
	f.write(u"NO ÉS SOLUCIÓ")
else:
	f.write(str(nova_comarca))
f.write("\n\n")

# =============================================================================
f.write(u"====== MÀSTER C =======\n")

punt_coincidencia_com1_1 = -1
punt_coincidencia_com1_2 = -1
punt_coincidencia_com2_1 = -1
punt_coincidencia_com2_2 = -1

# cap endavant
punt_com1 = 0
for coordenades1 in comarques_dict[geojson1]['geometry']['coordinates']:
	punt_com2 = 0
	for coordenades2 in comarques_dict[geojson2]['geometry']['coordinates']:
		if iguals(coordenades1,coordenades2,radi) and punt_coincidencia_com1_1 == -1:
			print "entro a la frontera 1"
			punt_coincidencia_com1_1 = punt_com1
			punt_coincidencia_com2_1 = punt_com2
			break
		punt_com2 = punt_com2 + 1
	if punt_coincidencia_com1_1 != -1:
		break
	punt_com1 = punt_com1 + 1

# cap endarrere
punt_com1 = 0
for coordenades1 in comarques_dict[geojson1]['geometry']['coordinates'][::-1]:
	punt_com2 = 0
	for coordenades2 in comarques_dict[geojson2]['geometry']['coordinates'][::-1]:
		if iguals(coordenades1,coordenades2,radi) and punt_coincidencia_com1_2 == -1:
			print "entro a la frontera 2"
			punt_coincidencia_com1_2 = punt_com1
			punt_coincidencia_com2_2 = punt_com2
			break
		punt_com2 = punt_com2 + 1
	if punt_coincidencia_com1_2 != -1:
		break
	punt_com1 = punt_com1 + 1

print

print(punt_coincidencia_com1_1)
print(punt_coincidencia_com1_2)
print(punt_coincidencia_com2_1)
print(punt_coincidencia_com2_2)

#print lon_com1 #compte! que l'últim punt és el mateix que el primer. No hi ha 20 punts, sinó 21
#print lon_com2
#recordar que l'últim punt és el mateix que el primer
nova_comarca = comarques_dict[geojson1]['geometry']['coordinates'][0:punt_coincidencia_com1_1]
nova_comarca = nova_comarca + comarques_dict[geojson2]['geometry']['coordinates'][punt_coincidencia_com2_1:lon_com2b-punt_coincidencia_com2_2]
nova_comarca = nova_comarca + comarques_dict[geojson1]['geometry']['coordinates'][lon_com1b-punt_coincidencia_com1_2:lon_com1b]
nova_comarca = nova_comarca + comarques_dict[geojson1]['geometry']['coordinates'][0:1]
print "longitud de la nova comarca: " + str(len(nova_comarca))

if (abs(lon_com1 + lon_com2 - 2*num_coinc + 1 - len(nova_comarca))) > 4:
	f.write(u"NO ÉS SOLUCIÓ")
elif (lon_com1==len(nova_comarca) or lon_com2==len(nova_comarca)):
	f.write(u"NO ÉS SOLUCIÓ")
else:
	f.write(str(nova_comarca))
f.write("\n\n")

# =============================================================================
f.write(u"====== MÀSTER D =======\n")

punt_coincidencia_com1_1 = -1
punt_coincidencia_com1_2 = -1
punt_coincidencia_com2_1 = -1
punt_coincidencia_com2_2 = -1

# 1
punt_prov = -1
punt_com1 = 0
for coordenades1 in comarques_dict[geojson1]['geometry']['coordinates'][::-1]:
	punt_com2 = 0
	for coordenades2 in comarques_dict[geojson2]['geometry']['coordinates']:
		if iguals(coordenades1,coordenades2,radi) and punt_coincidencia_com1_1 == -1:
			punt_prov = punt_com2
			break
		punt_com2 = punt_com2 + 1

	if punt_com2 == lon_com2:
		print "surto de la frontera 1"
		punt_coincidencia_com1_1 = punt_com1 - 1
		punt_coincidencia_com2_1 = punt_prov
		break
	punt_com1 = punt_com1 + 1


# cap endarrere

punt_prov = -1
punt_com1 = 0
for coordenades1 in comarques_dict[geojson1]['geometry']['coordinates']:
	punt_com2 = 0
	for coordenades2 in comarques_dict[geojson2]['geometry']['coordinates'][::-1]:
		if iguals(coordenades1,coordenades2,radi) and punt_coincidencia_com1_2 == -1:
			punt_prov = punt_com2
			break
		punt_com2 = punt_com2 + 1

	if punt_com2 == lon_com2:
		print "surto de la frontera 1"
		punt_coincidencia_com1_2 = punt_com1 - 1
		punt_coincidencia_com2_2 = punt_prov
		break
	punt_com1 = punt_com1 + 1

print


print(punt_coincidencia_com1_1)
print(punt_coincidencia_com1_2)
print(punt_coincidencia_com2_1)
print(punt_coincidencia_com2_2)

#recordar que l'últim punt és el mateix que el primer
nova_comarca = comarques_dict[geojson2]['geometry']['coordinates'][punt_coincidencia_com2_1:lon_com1b-punt_coincidencia_com2_2]
nova_comarca = nova_comarca + comarques_dict[geojson1]['geometry']['coordinates'][punt_coincidencia_com1_2:lon_com1b-punt_coincidencia_com1_1]
nova_comarca = nova_comarca + comarques_dict[geojson1]['geometry']['coordinates'][lon_com1b-punt_coincidencia_com1_1:lon_com1b-punt_coincidencia_com1_1+1]
print "longitud de la nova comarca: " + str(len(nova_comarca))

if (abs(lon_com1 + lon_com2 - 2*num_coinc + 1 - len(nova_comarca))) > 4:
	f.write(u"NO ÉS SOLUCIÓ")
elif (lon_com1==len(nova_comarca) or lon_com2==len(nova_comarca)):
	f.write(u"NO ÉS SOLUCIÓ")
else:
	f.write(str(nova_comarca))
f.write("\n\n")

# =============================================================================

f.close()
print("s'ha generat solucio.txt")