from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404
from .models import Students, MarkAndPresence
from students.api.serializers import StudentSerializer, MarkAndPresenceSerializer
from rest_framework import generics


class GetSmthng(generics.ListAPIView):
    serializer_class = StudentSerializer

    def get_queryset(self):
        queryset = Students.objects.all()
        name = self.request.query_params.get('name', '')
        if name is not None:
            queryset = queryset.filter(last_name=name)
        else:
            return queryset
        return queryset

    def getname(self):
        student = self.get_queryset()
        serializer = StudentSerializer(student)
        return Response(serializer.data)


class GetDP(generics.ListAPIView):
    serializer_class = MarkAndPresenceSerializer

    def get_queryset(self):
        queryset = MarkAndPresence.objects.all()
        present = self.request.query_params.get('present', '')
        if present:
            if present == 'False':
                present = False
            elif present == 'True':
                present = True
            else:
                return queryset
            return queryset.filter(present=present)
        return queryset

    def getdate(self):
        student = self.get_queryset()
        serializer = MarkAndPresenceSerializer(student)
        return Response(serializer.data)


class Map(APIView):

    def getAll(self, request, format=None):
        queryset = MarkAndPresence.objects.all()
        serializer = MarkAndPresenceSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = MarkAndPresenceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self, pk):
        try:
            return MarkAndPresence.objects.get(pk=pk)
        except Student.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        student = self.get_object(pk)
        serializer = MarkAndPresenceSerializer(student)
        return Response(serializer.data)