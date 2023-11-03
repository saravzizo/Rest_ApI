from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Students
from .serializer import StudentSerializer
from django.shortcuts import get_object_or_404
# Create your views here.


class FETCH(APIView):
    def get(self, request):
        result = Students.objects.all()
        serializers = StudentSerializer(result, many=True)
        return Response({'status': 'success', "students": serializers.data}, status=200)


class GET(APIView):
    def get(self, request, id):

        if Students.objects.filter(roll_number=id).exists():
            result1 = Students.objects.get(roll_number=id)
            serializers = StudentSerializer(result1)
            return Response({'success': 'success', "students": serializers.data}, status=200)
        else:
            return Response({'status': 'error', 'message': 'Student with roll number {} does not exist'.format(id)}, status=404)


class POST(APIView):

    def post(self, request):
        serializer = StudentSerializer(data=request.data, many=True)

        data = (request.data)
        skipped_data = []
        skipped_roll_no = []
        added_data = []
        error_data_roll_no = []
        for i in data:

            print(data)
            if Students.objects.filter(roll_number=i.get("roll_number")).exists():
                skipped_data.append(i)
                skipped_roll_no.append(i.get('roll_number'))

            else:
                serializer = StudentSerializer(data=i)
                if serializer.is_valid():
                    added_data.append(i)
                    serializer.save()
                else:
                    print(i)
                    error_data_roll_no.append(i)
                    return Response({"status": "error","error data" :'error in student data {}'.format(error_data_roll_no), "data": serializer.errors, "Added Data": added_data}, status=status.HTTP_400_BAD_REQUEST)

        if skipped_data:
            return Response({'status': 'error', 'message': 'Students with roll number {} already exists'.format(skipped_roll_no), "Added Data": added_data, "skipped_data": skipped_data}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"status": "success", "message": "Students added successfully","Added Data": added_data}, status=status.HTTP_200_OK)


class PATCH(APIView):
    def patch(self, request, id):

        data = request.data

        if Students.objects.filter(roll_number=id).exists():
            result = Students.objects.get(roll_number=id)
            serializer = StudentSerializer(result, data=request.data, partial=True)
            if serializer.is_valid():
                if Students.objects.filter(roll_number=data.get('roll_number')).exists():
                    return Response({'status': 'error', 'message': 'Student with roll number {} already found.'.format(data.get('roll_number'))}, status=400)
                else:
                    serializer.save()
                    return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

        else:
            return Response({'status': 'error', 'message': 'Student with id {} does not exist'.format(id)}, status=404)


class DELETE(APIView):
    def delete(self, request, id):
        result = get_object_or_404(Students, roll_number=id)
        result.delete()
        return Response({"status": "success", "data": "Record Deleted"})
