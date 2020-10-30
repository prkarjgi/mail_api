import io

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.parsers import JSONParser

from schedules.models import Schedule
from schedules.serializers import ScheduleSerializer


@csrf_exempt
def schedule_list(request):
    """
    view to fetch all schedules stored or to add a new schedule
    """
    if request.method == 'GET':
        schedules = Schedule.objects.all()
        serializers = ScheduleSerializer(instance=schedules, many=True)
        return JsonResponse(serializers.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ScheduleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def schedule_one(request, pk):
    """
    view to get or update or delete a single schedule corresponding
    to the primary key passed as an argument to the view.
    """
    try:
        schedule = Schedule.objects.get(pk=pk)
    except Schedule.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = ScheduleSerializer(instance=schedule)
        return JsonResponse(serializer.data, status=200)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = ScheduleSerializer(instance=schedule, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        schedule.delete()
        return HttpResponse(status=204)
