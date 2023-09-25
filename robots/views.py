from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View
from robots.forms import RobotForm
import json

class RobotsAddView(View):
    def post(self, request):
        try:
            raw_data = json.loads(request.body)
        except Exception:
            return JsonResponse({"detail": "Incorrect request"}, status=400)
        
        result_data = []
        error_data = []
        i = 0
        if type(raw_data) != list:
            obj = raw_data
            raw_data = []
            raw_data.append(obj)

        for record in raw_data:
            #record['']
            form = RobotForm(data=record)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.serial = form.cleaned_data['model'] + '-' \
                                            + form.cleaned_data['version']
                result_data.append(form.cleaned_data)
                obj.save()
            else:
                error_data.append({f"Record {i} - ": form.errors})
            i += 1

        return JsonResponse({'success': result_data, 
                             'failure': error_data})