import pyproj
from nautical_calculations.basic import rhumb_line, get_bearing

def decdeg2dms(dd):
    mnt,sec = divmod(dd*3600,60)
    deg,mnt = divmod(mnt,60)
    return deg,mnt,sec

def hms2float(hms):
    hms = hms.split(' : ')
    return int(hms[0]) + int(hms[1])/60 + int(hms[2])/3600

def route_points_creator(context):
    route = []
    route.append(context.get('object').departure_apt_id)
    for item in context.get('waypoints_list'):
        route.append(item)
    route.append(context.get('object').arrival_apt_id)
    route[0].distance = 0
    route[0].total_distance = 0
    return route

def distances_list_creator(context):
    route = route_points_creator(context)
    distances = []
    for ind in range(1, len(route)):
        route[ind].distance = rhumb_line(route[ind].lat, route[ind].lon, route[ind-1].lat, route[ind-1].lon)
        distances.append(route[ind].distance)
    return sum(distances)

def total_distance_creator(context):
    route = route_points_creator(context)
    total_distance = 0
    for ind in range(1, len(route)):
        route[ind].total_distance = total_distance + rhumb_line(route[ind].lat, route[ind].lon, route[ind-1].lat, route[ind-1].lon)
        total_distance = route[ind].total_distance
    return total_distance

def dechour2hms(dechour):
    hours = int(dechour)
    minutes = (dechour * 60) % 60
    seconds = (dechour * 3600) % 60
    if minutes < 10 and seconds < 10:
        output = f'{hours} : 0{int(minutes)} : 0{int(seconds)}'
        return output
    if minutes < 10:
        output = f'{hours} : 0{int(minutes)} : {int(seconds)}'
        return output
    if seconds < 10:
        output = f'{hours} : {int(minutes)} : 0{int(seconds)}'
        return output

    output = f'{hours} : {int(minutes)} : {int(seconds)}'
    return output



def ete_calculator(context):
    route = route_points_creator(context)
    avg_speed = context.get('object').aircraft_id.avg_speed
    for ind in range(1, len(route)):
        route[ind].ete = dechour2hms(route[ind].distance / avg_speed)

def total_time_calculator(context):
    route = route_points_creator(context)
    avg_speed = context.get('object').aircraft_id.avg_speed
    total_time = 0
    for ind in range(1, len(route)):
        route[ind].tte = dechour2hms(total_time + route[ind].distance / avg_speed)
        total_time += route[ind].distance / avg_speed


def hdg_calculator(context):
    geodesic = pyproj.Geod(ellps='WGS84')
    route = route_points_creator(context)
    for ind in range(1, len(route)):
        # fwd_azimuth= Geodesic.WGS84.Inverse(route[ind-1].lat, route[ind-1].lon, route[ind].lat, route[ind].lon)['azi2']
        fwd_azimuth = get_bearing(route[ind-1].lat, route[ind-1].lon, route[ind].lat, route[ind].lon)
        route[ind].hdg = round(fwd_azimuth,1)

def range_calculaor(context):
    flight_plan = context.get('object')
    flight_plan.fob_range = dechour2hms(flight_plan.fob / flight_plan.aircraft_id.fuel_consumption)

def is_fp_to_be_achived(context):
    if hms2float(context.get('object').arrival_apt_id.tte) > hms2float(context.get('object').fob_range):
        context.get('object').achivable = False
    elif hms2float(context.get('object').arrival_apt_id.tte) <= hms2float(context.get('object').fob_range):
        context.get('object').achivable = True

