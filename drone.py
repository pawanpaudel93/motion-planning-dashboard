import requests
from udacidrone import Drone

endpoints = {
    "sessions": "/api/v1/sessions/",
    "movements": "/api/v1/movements/",
    "drone_data": "/api/v1/drones-data/"
}


class Session:
    session_id = None

    def __init__(self, target_altitude, safety_distance, base_url=None):
        self.target_altitude = target_altitude
        self.safety_distance = safety_distance
        self.base_url = base_url if base_url else "http://localhost:8000"

    def get_session(self):
        data = {
            "target_altitude": self.target_altitude,
            "safety_distance": self.safety_distance
        }
        url = f"{self.base_url}{endpoints['sessions']}"
        response = requests.post(url, json=data)
        response.raise_for_status()
        response_data = response.json()
        self.session_id = response_data.get('id')

    def update_session(self, start, goal):
        data = {
            "start": start,
            "goal": goal
        }
        url = f"{self.base_url}{endpoints['sessions']}{self.session_id}/"
        _ = requests.patch(url, json=data)
    
    def end_session(self):
        data = {
            "is_finished": True
        }
        url = f"{self.base_url}{endpoints['sessions']}{self.session_id}/"
        _ = requests.patch(url, json=data)

    def send_movement(self, movement):
        data = {
            "session": self.session_id,
            "value": movement
        }
        url = f"{self.base_url}{endpoints['movements']}"
        _ = requests.post(url, json=data)
    
    def send_values(self, *args):
        timestamp, global_position, global_home, local_position, local_velocity = args
        data = {
            "session": self.session_id,
            "timestamp": timestamp,
            "global_position": global_position,
            "global_home": global_home,
            "local_position": local_position,
            "local_velocity": local_velocity
        }
        url = f"{self.base_url}{endpoints['drone_data']}"
        _ = requests.post(url, json=data)

class MyDrone(Drone):
    def __init__(self, connection, target_altitude, safety_distance):
        super().__init__(connection)
        self.session = Session(target_altitude=target_altitude, safety_distance=safety_distance)
        self.session.get_session()
        self.north_offset = 0
        self.east_offset = 0


    def log_telemetry(self, msg_name, msg):
        """Save the msg information to the telemetry log"""
        if self.tlog.open:
            data = [msg_name, msg.time]
            for k in msg.__dict__.keys():
                if k != '_time':
                    data.append(msg.__dict__[k])
            if msg_name.name == "LOCAL_POSITION":
                global_position = [self._longitude, self._latitude, self._altitude]
                global_home = [ self._home_longitude, self._home_latitude, self._home_altitude]
                local_position = [self._north, self._east, self._down]
                local_velocity = [self._velocity_north, self._velocity_east, self._velocity_down]
                self.session.send_values(msg.time, global_position, global_home, local_position, local_velocity)
            try:
                self.tlog.log_telemetry_data(data)
            except AttributeError:
                self.tlog.log_telemetry_msg(msg_name, msg)
