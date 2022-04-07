import folium
import pyproj
from nautical_calculations.basic import rhumb_line, get_bearing

def add_all_airports_to_map(context):
    apt_list = context.get('airport_list')
    m = folium.Map(
        width='100%', height=500, zoom_start=1
    )
    for apt in apt_list:
        folium.Marker(
            [apt.lat, apt.lon],
            popup=apt,
            icon=folium.Icon(color="grey", icon="fa fa-suitcase", prefix="fa"),
        ).add_to(m)
    m = m._repr_html_()
    return m

def point_map_view(context):
    lat = context.get('object').lat
    lon = context.get('object').lon
    m = folium.Map(
            width='100%', height=500, location=(lat, lon), zoom_start=10
        )
    folium.Marker(
        [lat, lon],
        popup=f'{context["object"]}',
        icon=folium.Icon(color="grey"),
    ).add_to(m)
    m = m._repr_html_()
    return m

def zoom_calc(context):
    distance = context["object"].arrival_apt_id.total_distance
    return 7 - distance / 30000 * 8


def center_coordinates(context):
    context.get("object").center_coordinates = [
        (context["object"].departure_apt_id.lat + context["object"].arrival_apt_id.lat) / 2,
        (context["object"].departure_apt_id.lon + context["object"].arrival_apt_id.lon) / 2,
    ]


def add_fp_markers(context):
    wpt_list = context.get("waypoints_list")
    dep_lat = context["object"].departure_apt_id.lat
    dep_lon = context["object"].departure_apt_id.lon
    arr_lat = context["object"].arrival_apt_id.lat
    arr_lon = context["object"].arrival_apt_id.lon
    m = folium.Map(
        width='100%', height=500, location=context.get("object").center_coordinates, zoom_start=zoom_calc(context)
    )
    folium.Marker(
        [dep_lat, dep_lon],
        popup=f'{context["object"].departure_apt_id}',
        icon=folium.Icon(color="red", icon="plane", prefix="fa"),
    ).add_to(m)
    folium.Marker(
        [arr_lat, arr_lon],
        popup=f'{context["object"].arrival_apt_id}',
        icon=folium.Icon(color="green", icon="plane", prefix="fa", angle=180),
    ).add_to(m)
    if wpt_list:
        m.add_child(
            folium.PolyLine(
                locations=[(dep_lat, dep_lon), (wpt_list[0].lat, wpt_list[0].lon)],
                weight=2,
                color="red",
                tooltip=f'Stage 1 {context["object"].departure_apt_id.ICAO} - {wpt_list[0]}',
            )
        )

        for waypoint_ind in range(len(wpt_list)):
            folium.Marker(
                [wpt_list[waypoint_ind].lat, wpt_list[waypoint_ind].lon],
                popup=wpt_list[waypoint_ind].name,
                icon=folium.Icon(color="blue", icon="arrows-h", prefix="fa"),
            ).add_to(m)
            if waypoint_ind != 0:
                m.add_child(
                    folium.PolyLine(
                        locations=[
                            (wpt_list[waypoint_ind - 1].lat, wpt_list[waypoint_ind - 1].lon),
                            (wpt_list[waypoint_ind].lat, wpt_list[waypoint_ind].lon),
                        ],
                        weight=2,
                        color="blue",
                        tooltip=f"Stage {waypoint_ind+1} {wpt_list[waypoint_ind-1]} - {wpt_list[waypoint_ind]}",
                    )
                )
        m.add_child(
            folium.PolyLine(
                locations=[(wpt_list[len(wpt_list) - 1].lat, wpt_list[len(wpt_list) - 1].lon), (arr_lat, arr_lon)],
                weight=2,
                color="green",
                tooltip=f'Stage {len(wpt_list)+1} {wpt_list[len(wpt_list)-1]} - {context["object"].arrival_apt_id.ICAO}',
            )
        )
    else:
        m.add_child(
            folium.PolyLine(
                locations=[(dep_lat, dep_lon), (arr_lat, arr_lon)],
                weight=2,
                color="green",
                tooltip=f'Stage 1 {context["object"].departure_apt_id} - {context["object"].arrival_apt_id}',
            )
        )
    m = m._repr_html_()
    return m


def decdeg2dms(dd):
    mnt, sec = divmod(dd * 3600, 60)
    deg, mnt = divmod(mnt, 60)
    return deg, mnt, sec


def hms2float(hms):
    hms = hms.split(" : ")
    return int(hms[0]) + int(hms[1]) / 60 + int(hms[2]) / 3600


def route_points_creator(context):
    route = []
    route.append(context.get("object").departure_apt_id)
    for item in context.get("waypoints_list"):
        route.append(item)
    route.append(context.get("object").arrival_apt_id)
    route[0].distance = 0
    route[0].total_distance = 0
    return route


def distances_list_creator(context):
    route = route_points_creator(context)
    distances = []
    for ind in range(1, len(route)):
        route[ind].distance = rhumb_line(route[ind].lat, route[ind].lon, route[ind - 1].lat, route[ind - 1].lon)
        distances.append(route[ind].distance)
    return sum(distances)


def total_distance_creator(context):
    route = route_points_creator(context)
    total_distance = 0
    for ind in range(1, len(route)):
        route[ind].total_distance = total_distance + rhumb_line(
            route[ind].lat, route[ind].lon, route[ind - 1].lat, route[ind - 1].lon
        )
        total_distance = route[ind].total_distance
    return total_distance


def dechour2hms(dechour):
    hours = int(dechour)
    minutes = (dechour * 60) % 60
    seconds = (dechour * 3600) % 60
    if minutes < 10 and seconds < 10:
        output = f"{hours} : 0{int(minutes)} : 0{int(seconds)}"
        return output
    if minutes < 10:
        output = f"{hours} : 0{int(minutes)} : {int(seconds)}"
        return output
    if seconds < 10:
        output = f"{hours} : {int(minutes)} : 0{int(seconds)}"
        return output

    output = f"{hours} : {int(minutes)} : {int(seconds)}"
    return output


def ete_calculator(context):
    route = route_points_creator(context)
    avg_speed = context.get("object").aircraft_id.avg_speed
    for ind in range(1, len(route)):
        route[ind].ete = dechour2hms(route[ind].distance / avg_speed)


def total_time_calculator(context):
    route = route_points_creator(context)
    avg_speed = context.get("object").aircraft_id.avg_speed
    total_time = 0
    for ind in range(1, len(route)):
        route[ind].tte = dechour2hms(total_time + route[ind].distance / avg_speed)
        total_time += route[ind].distance / avg_speed


def hdg_calculator(context):
    geodesic = pyproj.Geod(ellps="WGS84")
    route = route_points_creator(context)
    for ind in range(1, len(route)):
        # fwd_azimuth= Geodesic.WGS84.Inverse(route[ind-1].lat, route[ind-1].lon, route[ind].lat, route[ind].lon)['azi2']
        fwd_azimuth = get_bearing(route[ind - 1].lat, route[ind - 1].lon, route[ind].lat, route[ind].lon)
        route[ind].hdg = round(fwd_azimuth, 1)


def range_calculaor(context):
    flight_plan = context.get("object")
    flight_plan.fob_range = dechour2hms(flight_plan.fob / flight_plan.aircraft_id.fuel_consumption)


def is_fp_to_be_achived(context):
    if hms2float(context.get("object").arrival_apt_id.tte) > hms2float(context.get("object").fob_range):
        context.get("object").achivable = False
    else:
        context.get("object").achivable = True
