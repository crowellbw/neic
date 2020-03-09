#!/home/crowellb/anaconda3/bin/python3
import numpy
import datetime
import calendar
import math
#####################################################################################
#Constants
c = 299792458.0 #speed of light
fL1 = 1575.42e6 #L1 frequency
fL2 = 1227.60e6 #L2 frequency


def month_converter(month):
    months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
    return months.index(month) + 1

def doy_calc(year,month,day):
    isleap = calendar.isleap(year)
    if str(isleap) == 'True':
        dom = [31,29,31,30,31,30,31,31,30,31,30,31]
    else:
        dom = [31,28,31,30,31,30,31,31,30,31,30,31]
    doy = int(numpy.sum(dom[:(month-1)])+day)
    return(doy)

def gpsweekdow(year,doy):
    date = datetime.datetime(year, 1, 1) + datetime.timedelta(doy - 1)
    gpstime = (numpy.datetime64(date) - numpy.datetime64('1980-01-06T00:00:00'))/ numpy.timedelta64(1, 's')
    gpsweek = int(gpstime/604800)
    gpsdow = math.floor((gpstime-gpsweek*604800)/86400)                   
    return(gpsweek, gpsdow)

def gpstimeconvert(gpstime):
    gpsweek = int(gpstime/604800)
    gpsdow = math.floor((gpstime-gpsweek*604800)/86400) 
    gpssow = gpstime-gpsweek*604800                 
    return(gpsweek, gpsdow, gpssow)

def lla2ecef(lat,lon,alt):
    lat = lat*math.pi/180
    lon = lon*math.pi/180
    a = 6378137
    e = 8.1819190842622e-2

    N = a/numpy.sqrt(1-numpy.power(e,2)*numpy.power(numpy.sin(lat),2))

    x = (N+alt)*numpy.cos(lat)*numpy.cos(lon)
    y = (N+alt)*numpy.cos(lat)*numpy.sin(lon)
    z = ((1-numpy.power(e,2))*N+alt)*numpy.sin(lat)
	
    return (x, y, z)

def ecef2lla(x,y,z):
    a = 6378137
    e = 8.1819190842622e-2
    b = math.sqrt(math.pow(a,2)*(1-math.pow(e,2)))
    ep = math.sqrt((math.pow(a,2)-math.pow(b,2))/math.pow(b,2))
    p = math.sqrt(math.pow(x,2)+math.pow(y,2))
    th = math.atan2(a*z,b*p)
    lon = math.atan2(y,x)
    lat = math.atan2((z+math.pow(ep,2)*b*math.pow(math.sin(th),3)),(p-math.pow(e,2)*a*math.pow(math.cos(th),3)))
    N = a/math.sqrt(1-math.pow(e,2)*math.pow(math.sin(lat),2))
    alt = p/math.cos(lat)-N
    return (lat,lon,alt)


def azi_elev(xsta,ysta,zsta,xsat,ysat,zsat):
    [latsta,lonsta,altsta]=ecef2lla(xsta,ysta,zsta)
    [latsat,lonsat,altsat]=ecef2lla(xsat,ysat,zsat)
    re = math.sqrt(math.pow(xsta,2)+math.pow(ysta,2)+math.pow(zsta,2))
    rs = math.sqrt(math.pow(xsat,2)+math.pow(ysat,2)+math.pow(zsat,2))
    gamma = math.acos(math.cos(latsta)*math.cos(latsat)*math.cos(lonsat-lonsta) + math.sin(latsta)*math.sin(latsat))
    elev = math.acos(math.sin(gamma)/math.sqrt(1 + math.pow(re/rs,2) - 2*re/rs*math.cos(gamma)))

    deltalon = lonsat-lonsta

    azi = math.atan2(math.sin(deltalon)*math.cos(latsat),math.cos(latsta)*math.sin(latsat)-math.sin(latsta)*math.cos(latsat)*math.cos(deltalon))

    azi = azi*180/math.pi

    if (azi < 0):
        azi = azi+360
    elev = elev*180/math.pi
    return(azi,elev)


#This takes displacements in x, y, z and converts them to north, east up

def dxyz2dneu(dx,dy,dz,lat,lon):
    lat = lat*math.pi/180
    lon = lon*math.pi/180
    dn = -numpy.sin(lat)*numpy.cos(lon)*dx-numpy.sin(lat)*numpy.sin(lon)*dy+numpy.cos(lat)*dz
    de = -numpy.sin(lon)*dx+numpy.cos(lon)*dy
    du = numpy.cos(lat)*numpy.cos(lon)*dx+numpy.cos(lat)*numpy.sin(lon)*dy+numpy.sin(lat)*dz
    return (dn, de, du)


#This takes covariances in x, y, z and converts them to north, east up

def covrot(cx,cy,cz,cxy,cxz,cyz,lat,lon):       
    lat = lat*math.pi/180
    lon = lon*math.pi/180
    slat = numpy.sin(lat)
    slon = numpy.sin(lon)
    clat = numpy.cos(lat)
    clon = numpy.cos(lon)
    cn = numpy.sqrt(numpy.absolute(-slat*clon*cx*cx+clat*cxz-slat*slon*cxy))
    ce = numpy.sqrt(numpy.absolute(clon*cy*cy-cxy*slon))
    cu = numpy.sqrt(numpy.absolute(slat*cz*cz+clat*clon*cxz+clat*slon*cyz))
    return (cn,ce,cu)
    
    

