import requests
import json
import statistics
from constants import RME_API_KEY, RME_APP_ID

def get_avg_speed_limit(coords):
    apikey = RME_API_KEY
    app_id = RME_APP_ID

    # Construct the query URL
    query = f'https://rme.api.here.com/2/matchroute.json?routemode=car&app_id={app_id}&apiKey={apikey}&attributes=SPEED_LIMITS_FCn(*)'

    # Format the coordinates into the required string format
    coord_strings = ['{:.5f},{:.5f}'.format(coord[0], coord[1]) for coord in coords]
    data = 'latitude,longitude\n' + '\n'.join(coord_strings)

    # Send the POST request
    result = requests.post(query, data=data)

    # Check if the request was successful
    if result.status_code == 200:
        # Parse the response as JSON
        response = result.json()
    else:
        print(f"Error: {result.status_code} - {result.text}")


    # Extract the speed limits along the route
    speed_limits = []

    # TODO: Rewrite
    for link in response['RouteLinks']:
        speed_limit_info = link['attributes'].get('SPEED_LIMITS_FCN', [])
        if speed_limit_info:
            for limit in speed_limit_info:
                speed_limits.append({
                    "linkId": link['linkId'],
                    "from_speed_limit": limit['FROM_REF_SPEED_LIMIT'],
                    "to_speed_limit": limit['TO_REF_SPEED_LIMIT'],
                    "unit": limit['SPEED_LIMIT_UNIT'],
                    "shape": link['shape']
                })

    _speed_limits2 = []

    # Print the extracted speed limits
    for limit in speed_limits:
        _speed_limits2.append(max(int(limit['to_speed_limit']), int(limit['from_speed_limit'])))

    return statistics.median(_speed_limits2)