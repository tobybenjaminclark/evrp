import requests
import statistics
from keys import RME_API_KEY, RME_APP_ID
import random
import time

def get_avg_speed_limit(coords, depth = 0):
    apikey = RME_API_KEY
    app_id = RME_APP_ID

    # Send over the query to get the road speeds.
    query = f'https://rme.api.here.com/2/matchroute.json?routemode=car&app_id={app_id}&apiKey={apikey}&attributes=SPEED_LIMITS_FCn(*)'
    data = 'latitude,longitude\n' + '\n'.join([f'{lat:.5f},{lon:.5f}' for lat, lon in coords])
    response = requests.post(query, data=data)

    # Hopefully this will be successful - if not, we're screwed :)
    if response.status_code == 429:
        if(depth >= 0):
            return 64

        print(f"Error: {response.status_code} - {response.text}")
        time.sleep(random.randrange(0, 3))
        return get_avg_speed_limit(coords, depth + 1)

    if response.status_code != 200:
        raise Exception(f"Error: {response.status_code} - {response.text}")

    try:
        # Parse the response as JSON, and extract the speed limit data. We're using `max` here as it provides to/from
        # data - which can sometimes be zero - using max averts this and fixes it.
        response_json = response.json()
        speed_limits = [
            max(int(limit['TO_REF_SPEED_LIMIT']), int(limit['FROM_REF_SPEED_LIMIT']))
            for link in response_json.get('RouteLinks', [])
            for limit in link['attributes'].get('SPEED_LIMITS_FCN', [])
        ]
    except Exception as e:
        print(response_json)
        print(e)
        return (64)

    # Return the median speed limit
    return statistics.median(speed_limits) if speed_limits else 64
