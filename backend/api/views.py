from django.contrib.staticfiles.storage import staticfiles_storage
from rest_framework.viewsets import ViewSet, ModelViewSet
from django.views.generic import TemplateView
from rest_framework.response import Response
from django.shortcuts import _get_queryset
from rest_framework.views import APIView
from django.http import Http404
from bresenham import bresenham
from scipy.spatial import Voronoi
import numpy as np

from .serializers import *
from .models import *

def get_latest_object_or_404(klass, *args, **kwargs):
    queryset = _get_queryset(klass)
    try:
        return queryset.filter(*args, **kwargs).latest()
    except queryset.model.DoesNotExist:
        raise Http404('No %s matches the given query.' % queryset.model._meta.object_name)


def get_data():
    data = np.load(staticfiles_storage.path('colliders.npy'))
    return data


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
    points = []

    # Populate the grid with obstacles
    for i in range(data.shape[0]):
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

    # create a voronoi graph based on location of obstacle centres
    graph = Voronoi(points)

    # check each edge from graph.ridge_vertices for collision
    edges = []
    for v in graph.ridge_vertices:
        p1 = graph.vertices[v[0]]
        p2 = graph.vertices[v[1]]
        cells = list(bresenham(int(p1[0]), int(p1[1]), int(p2[0]), int(p2[1])))
        hit = False

        for c in cells:
            # First check if we're off the map
            if np.amin(c) < 0 or c[0] >= grid.shape[0] or c[1] >= grid.shape[1]:
                hit = True
                break
            # Next check if we're in collision
            if grid[c[0], c[1]] == 1:
                hit = True
                break

        # If the edge does not hit on obstacle
        # add it to the list
        if not hit:
            # array to tuple for future graph creation step)
            p1 = (p1[0], p1[1])
            p2 = (p2[0], p2[1])
            edges.append((p1, p2))

    return grid, edges
    
class SessionModelViewSet(ModelViewSet):
    serializer_class = SessionSerializer
    queryset = Session.objects.all()

class SessionViewSet(ViewSet):
    def retrieve(self, request, pk=None):
        queryset = Session.objects.all()
        session = get_object_or_404(queryset, pk=pk)
        serializer = SessionSerializer(session)
        target_altitude = serializer.data.get('target_altitude')
        map_data = get_data()
        grid, edges = create_grid_and_edges(map_data, target_altitude, 5)
        return Response({'grid': grid, 'edges': edges})

class MovementViewSet(ViewSet):
    def list(self, request, session_id):
        queryset = Movement.objects.filter(session=session_id)
        serializer = MovementSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, session_id):
        movement = get_latest_object_or_404(Movement, session=session_id)
        serializer = MovementSerializer(movement)
        return Response(serializer.data)
    

class GlobalPositionViewSet(ViewSet):
    def list(self, request, session_id):
        queryset = GlobalPosition.objects.filter(session=session_id)
        serializer = GlobalPositionSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, session_id):
        position = get_latest_object_or_404(GlobalPosition, session=session_id)
        serializer = GlobalPositionSerializer(position)
        return Response(serializer.data)


class GlobalHomeViewSet(ViewSet):
    def list(self, request, session_id):
        queryset = GlobalHome.objects.filter(session=session_id)
        serializer = GlobalHome(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, session_id):
        position = get_latest_object_or_404(GlobalHome, session=session_id)
        serializer = MovementSerializer(position)
        return Response(serializer.data)


class LocalPositionViewSet(ViewSet):
    def list(self, request, session_id):
        queryset = LocalPosition.objects.filter(session=session_id)
        serializer = LocalPositionSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, session_id):
        position = get_latest_object_or_404(LocalPosition, session=session_id)
        serializer = LocalPositionSerializer(position)
        return Response(serializer.data)


class LocalVelocity(ViewSet):
    def list(self, request, session_id):
        queryset = LocalVelocity.objects.filter(session=session_id)
        serializer = LocalVelocitySerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, session_id):
        velocity = get_latest_object_or_404(LocalVelocity, session=session_id)
        serializer = LocalVelocitySerializer(velocity)
        return Response(serializer.data)


class SimulationData(APIView):
    def get(self, request, session_id):
        pass