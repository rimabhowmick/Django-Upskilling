from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . models import students
from .serializers import studentsSerializer
from django.db import connection
from django.db import connections
from collections import namedtuple

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

def home(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM dafapp_students")
        students_list = dictfetchall(cursor)
        print(students_list)
    return render(request, 'home.html', {'students_list': students_list})

def add_mapping(request):
    with connections['datamgmtpf'].cursor() as cursor:
        cursor.execute("SELECT ds_id,ds_name FROM dmp.data_source")
        datasource_list = dictfetchall(cursor)
        print(datasource_list)
    return render(request, 'add_mapping.html', {'datasource_list': datasource_list})

class studentsList(APIView):
    def get(self,request):
        students1 =  students.objects.all()
        serializer = studentsSerializer(students1, many=True)
        return Response(serializer.data)

    def post(self):
        pass

