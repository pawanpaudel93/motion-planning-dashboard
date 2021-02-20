from rest_framework.viewsets import ViewSet, ModelViewSet
from django.views.generic import TemplateView
from rest_framework.response import Response
from django.views.decorators.cache import never_cache
from django.shortcuts import _get_queryset, get_object_or_404
from rest_framework.views import APIView
from django.http import Http404
from bresenham import bresenham
from scipy.spatial import Voronoi
from django.conf import settings
import asyncio
import time
import numpy as np

from .serializers import *
from .models import *

index_view = never_cache(TemplateView.as_view(template_name='api/index.html'))


def __run_until_completed(coros):
    futures = [asyncio.ensure_future(c) for c in coros]

    async def first_to_finish():
        while True:
            await asyncio.sleep(0)
            for f in futures:
                if f.done():
                    futures.remove(f)
                    return f.result()

    while len(futures) > 0:
        yield first_to_finish()

async def run_until_completed(tasks):
    for res in __run_until_completed(tasks):
        _ = await res

def get_event_loop():
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop

def wait_for_event_loop(loop):
    loop.run_until_complete(asyncio.sleep(0))
    while loop.is_running():
        time.sleep(0.3)
        if not loop.is_running():
            loop.close()
            break


def generate_obstacles(grid, data, safety_distance, drone_altitude, north_min, north_size, east_min, east_size):
    points = []
    async def generate(i):
        north, east, alt, d_north, d_east, d_alt = data[i, :]
        if alt + d_alt + safety_distance > drone_altitude:
            obstacle = [
                int(np.clip(north - d_north - safety_distance - north_min, 0, north_size - 1)),
                int(np.clip(north + d_north + safety_distance - north_min, 0, north_size - 1)),
                int(np.clip(east - d_east - safety_distance - east_min, 0, east_size - 1)),
                int(np.clip(east + d_east + safety_distance - east_min, 0, east_size - 1)),
            ]
            grid[obstacle[0]:obstacle[1] + 1, obstacle[2]:obstacle[3] + 1] = 1
            # add center of obstacles to points list
            points.append([north - north_min, east - east_min])
    loop = get_event_loop()
    coros = (generate(i) for i in range(data.shape[0]))
    loop.run_until_complete(run_until_completed(coros))
    wait_for_event_loop(loop)
    return grid, points

def generate_edges(grid, graph):
    edges = []
    async def generate(v):
        p1 = graph.vertices[v[0]]
        p2 = graph.vertices[v[1]]
        cells = list(bresenham(int(p1[0]), int(p1[1]), int(p2[0]), int(p2[1])))
        hit = False

        for c in cells:
            # First check if we're off the map
            if np.amin(c) < 0 or c[0] >= grid.shape[0] or c[1] >= grid.shape[1] or grid[c[0], c[1]] == 1:
                hit = True
                break

        # If the edge does not hit on obstacle
        # add it to the list
        if not hit:
            # array to tuple for future graph creation step)
            p1 = (p1[0], p1[1])
            p2 = (p2[0], p2[1])
            edges.append((p1, p2))

    loop = get_event_loop()
    coros = (generate(v) for v in graph.ridge_vertices)
    loop.run_until_complete(run_until_completed(coros))
    wait_for_event_loop(loop)
    return edges


def create_grid_and_edges(data, drone_altitude, safety_distance):
    '''
        Create a grid representation of a 2D configuration space and a Voronoi Graph
    '''
    # minimum and maximum north coordinates
    north_min = np.floor(np.min(data[:, 0] - data[:, 3]))
    north_max = np.ceil(np.max(data[:, 0] + data[:, 3]))
    # minimum and maximum east coordinates
    east_min = np.floor(np.min(data[:, 1] - data[:, 4]))
    east_max = np.ceil(np.max(data[:, 1] + data[:, 4]))

    # given the minimum and maximum coordinates we can
    # calculate the size of the grid.
    north_size = int(np.ceil(north_max - north_min))
    east_size = int(np.ceil(east_max - east_min))

    # Initialize an empty grid
    grid = np.zeros((north_size, east_size))
    # Initialize an empty list for Voronoi points
    
    grid, points = generate_obstacles(grid, data, safety_distance, drone_altitude, north_min, north_size, east_min, east_size)
    # create a voronoi graph based on location of obstacle centres
    graph = Voronoi(points)
    # check each edge from graph.ridge_vertices for collision
    edges = generate_edges(grid, graph)
    return grid, edges


class SessionModelViewSet(ModelViewSet):
    serializer_class = SessionSerializer
    queryset = Session.objects.all()
    ordering_fields = ('id')
    ordering = ('-id')

    def get_queryset(self):
        return Session.objects.all().order_by("-id")


class SessionViewSet(ViewSet):
    def retrieve(self, request, pk=None):
        queryset = Session.objects.all()
        session = get_object_or_404(queryset, pk=pk)
        serializer = SessionSerializer(session)
        target_altitude = serializer.data.get('target_altitude')
        map_data = settings.MAP_DATA
        grid, edges = create_grid_and_edges(map_data, target_altitude, 5)
        return Response({'grid': grid, 'edges': edges})


class MovementViewSet(ModelViewSet):
    queryset = Movement.objects.all()
    serializer_class = MovementSerializer


class DroneDataViewSet(ModelViewSet):
    queryset = DroneData.objects.all()
    serializer_class = DroneDataSerializer


class SimulationData(APIView):
    def get(self, request, pk=None):
        session = Session.objects.prefetch_related('movement_set', 'dronedata_set')
        session = get_object_or_404(session, pk=pk)
        try:
            movement = session.movement_set.values_list('value', flat=True)
        except Movement.DoesNotExist:
            movement = []
        try:
            drone_data = session.dronedata_set.latest()
            global_home = drone_data.global_home
            global_position = drone_data.global_position
            local_position = drone_data.local_position
            local_velocity = drone_data.local_velocity
        except DroneData.DoesNotExist:
            global_home = global_position = local_position = local_velocity = []
        
        response = {
            'session': {
                "isFinished": session.is_finished,
                "start": session.start,
                "goal": session.goal
            },
            'movement': movement,
            'globalPosition': global_position,
            'globalHome': global_home,
            'localPosition': local_position,
            'localVelocity': local_velocity
        }
        return Response(response)


class SimulationTableData(APIView):
    def get(self, request, pk=None):
        session = Session.objects.prefetch_related('movement_set', 'dronedata_set')
        session = get_object_or_404(session, pk=pk)
        try:
            movement = session.movement_set.values_list('value', flat=True)
        except Movement.DoesNotExist:
            movement = []
        try:
            drone_data = session.dronedata_set.all().order_by('timestamp')
            global_home = GlobalHomeSerializer(drone_data, many=True).data
            global_position = GlobalPositionSerializer(drone_data, many=True).data
            local_position = LocalPositionSerializer(drone_data, many=True).data
            local_velocity = LocalVelocitySerializer(drone_data, many=True).data
        except DroneData.DoesNotExist:
            global_home = global_position = local_position = local_velocity = []

        response = {
            'movement': movement,
            'globalPosition': global_position,
            'globalHome': global_home,
            'localPosition': local_position,
            'localVelocity': local_velocity
        }
        return Response(response)