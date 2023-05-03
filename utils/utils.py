import math

def get_distance(lat1, lng1, lat2, lng2):
    """
    Calculate the distance between two points on the Earth's surface using the Haversine formula.

    Args:
        lat1 (float): The latitude of the first point.
        lng1 (float): The longitude of the first point.
        lat2 (float): The latitude of the second point.
        lng2 (float): The longitude of the second point.

    Returns:
        The distance (in kilometers) between the two points.
    """
    earth_radius = 6371  # 지구 반지름(km)
    d_lat = math.radians(lat2 - lat1)
    d_lng = math.radians(lng2 - lng1)
    a = math.sin(d_lat/2) * math.sin(d_lat/2) + \
        math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * \
        math.sin(d_lng/2) * math.sin(d_lng/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = earth_radius * c
    return distance
