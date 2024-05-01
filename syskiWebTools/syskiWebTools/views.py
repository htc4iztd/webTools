# syskiWebTools/views.py

from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from .models import Task
import csv
from io import StringIO
from django.shortcuts import render

def index(request):
    return render(request, 'sysKiOpeTool.html')

@csrf_exempt
def upload_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES.get('file')
        if not csv_file.name.endswith('.csv'):
            return HttpResponseBadRequest('File is not CSV type')
        
        file_data = csv_file.read().decode('UTF-8')
        io_string = StringIO(file_data)
        reader = csv.DictReader(io_string)
        
        with transaction.atomic():  # トランザクションの開始
            for row in reader:
                # CSVから取得するカラム名がModelのフィールド名と一致していることを想定
                task, created = Task.objects.update_or_create(
                    id=row['id'],
                    defaults={key: row[key] for key in row}
                )
        return JsonResponse({'status': 'success'}, status=200)
    return HttpResponseBadRequest('Invalid request')