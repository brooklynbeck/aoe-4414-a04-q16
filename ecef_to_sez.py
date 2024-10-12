# ecef_to_eci.py
#
# Usage: python3 ecef_to_eci.py year month day hour minute second ecef_x_km ecef_y_km ecef_z_km
# Takes ecef coordinates and transforms them into sez coordinates
# Parameters:
# year
# month
# day
# hour
# minute
# second
# ecef_x_km
# ecef_y_km
# ecef_z_km
# Output:
# Prints eci x, y, and z coordinates
#
# Written by Brooklyn Beck
# Other contributors: None
# Updated with corrections

# import Python modules
import math # math module
import sys # argv
# "constants"
W_E = 7.292115*10**(-5)

# initialize script arguments
year = float('nan')
month = float('nan')
day = float('nan')
hour = float('nan')
minute = float('nan')
second = float('nan')
ecef_x_km = float('nan')
ecef_y_km = float('nan')
ecef_z_km = float('nan')

# parse script arguments
if len(sys.argv)==10:
  year = float(sys.argv[1])
  month = float(sys.argv[2])
  day = float(sys.argv[3])
  hour = float(sys.argv[4])
  minute = float(sys.argv[5])
  second = float(sys.argv[6])
  ecef_x_km = float(sys.argv[7])
  ecef_y_km = float(sys.argv[8])
  ecef_z_km = float(sys.argv[9])
else:
  print(\
  'Usage: '\
  'python3 ecef_to_eci.py year month day hour minute second ecef_x_km ecef_y_km ecef_z_km'\
  )
  exit()

# main script

#calculate fractional julian date
jd = day - 32075 + 1461*(year+4800-(14-month)//12)//4 + 367*(month-2+(14-month)//12*12)//12 - 3*((year+4900-(14-month)//12)//100)//4
d_frac = (second + 60*(minute+60*hour))/86400
jd_frac = jd-0.5 + d_frac

#calculate gmst angle
t_ut1 = (jd_frac - 2451545.0)/36525
gmst_sec = 67310.54841 + (876600*60*60+8640184.812866)*t_ut1 + 0.093104*t_ut1**2 - 6.2*10**(-6)*t_ut1**3
gmst_rad = math.fmod(math.fmod(gmst_sec, 86400)*W_E+2*math.pi, 2*math.pi)

#calculate eci components
eci_x_km = ecef_x_km*math.cos(-gmst_rad) + ecef_y_km*math.sin(-gmst_rad)
eci_y_km = -ecef_x_km*math.sin(-gmst_rad) + ecef_y_km*math.cos(-gmst_rad)
eci_z_km = ecef_z_km

#print output
print(eci_x_km)
print(eci_y_km)
print(eci_z_km)
