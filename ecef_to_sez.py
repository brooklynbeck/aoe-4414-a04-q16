# ecef_to_sez.py
#
# Usage: python3 ecef_to_sez.py o_x_km o_y_km o_z_km x_km y_km z_km
# Takes ecef coordinates and transforms them into sez coordinates
# Parameters:
# o_x_km : x coordinate of the ecef origin of the sez frame
# o_y_km : y coordinate of the ecef origin of the sez frame
# o_z_km : z coordinate of the ecef origin of the sez frame
# x_km : x ecef coordinate of the satellite
# y_km : y ecef coordinate of the satellite
# z_km : z ecef coordinate of the satellite
# Output:
# Prints s, e, and z coordinates in km
#
# Written by Brooklyn Beck
# Other contributors: None
#
# import Python modules
import math # math module
import sys # argv

# "constants"
R_E_KM = 6378.1363
E_E = 0.081819221456

# initialize script arguments
o_x_km = float('nan') #x coordinate of the ecef origin of the sez frame
o_y_km = float('nan') #y coordinate of the ecef origin of the sez frame
o_z_km = float('nan') #z coordinate of the ecef origin of the sez frame
x_km = float('nan') #x ecef coordinate of the satellite
y_km = float('nan') #y ecef coordinate of the satellite
z_km = float('nan') #z ecef coordinate of the satellite

# parse script arguments
if len(sys.argv)==7:
  o_x_km = float(sys.argv[1])
  o_y_km = float(sys.argv[2])
  o_z_km = float(sys.argv[3])
  x_km = float(sys.argv[4])
  y_km = float(sys.argv[5])
  z_km = float(sys.argv[6])
else:
  print(\
  'Usage: '\
  'python3 ecef_to_sez.py o_x_km o_y_km o_z_km x_km y_km z_km'\
  )
  exit()

# main script

#get vector components
x_vec = x_km - o_x_km
y_vec = y_km - o_y_km
z_vec = z_km - z_x_km

#solve for longitude
lon_rad = math.atan2(o_y_km, o_x_km)
lon_deg = lon_rad*180.0/math.pi

# initialize lat_rad, r_lon_km, z_km
lat_rad = math.asin(o_z_km/math.sqrt(o_x_km**2+o_y_km**2+o_z_km**2))
r_lon_km = math.sqrt(o_x_km**2+o_y_km**2)
prev_lat_rad = float('nan')

# iteratively find latitude
c_E = float('nan')
count = 0
while (math.isnan(prev_lat_rad) or abs(lat_rad-prev_lat_rad)>10e-7) and count<5:
  denom = math.sqrt(1.0-E_E**2*math.sin(lat_rad)**2)
  c_E = R_E_KM/denom
  prev_lat_rad = lat_rad
  lat_rad = math.atan((o_z_km+c_E*(E_E**2)*math.sin(lat_rad))/r_lon_km)
  count = count+1

#calculate height above ellipsoid
hae_km = r_lon_km / math.cos(lat_rad) - c_E

#use rotation matrices to get s, e, and z coordinates
s_km = x_vec*math.sin(lat_rad)*math.cos(lon_rad)+y_vec*math.sin(lat_rad)*math.sin(lon_rad)-z_vec*math.cos(lat_rad)
e_km = y_vec*math.cos(lon_rad)-x_vec*math.sin(lon_rad)
z_km = x_vec*math.cos(lat_rad)*math.cos(lon_rad)+y_vec*math.cos(lat_rad)*math.sin(lon_rad)+z_vec*math.sin(lat_rad)

print(s_km)
print(e_km)
print(z_km)
