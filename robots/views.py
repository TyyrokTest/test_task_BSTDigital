from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.views.generic import TemplateView
from django.utils import timezone
from django.db.models import Count
from robots.forms import RobotForm
from robots.models import Robot
from robots.utils import createExcel
import json

class ManagerReportView(TemplateView):
    template_name = 'index.html'
    
class ManagerReportCreateView(View):
    
    def get(self, request, *args, **kwargs):

        delta = timezone.timedelta(days=7)
        start_date = timezone.now() - delta
        end_date = timezone.now()
        robots = (
            Robot.objects.filter(created__range=(start_date, end_date))
                         .values('model', 'version')
                         .annotate(num=Count("version"))
                         .order_by('model', 'version')
        )
        if len(robots) == 0:
            return HttpResponse("No data for report") 
        stream = createExcel(qs=robots)
        
        return HttpResponse(content=stream, headers={
            "Content-Type": "application/vnd.ms-excel",
            "Content-Disposition": 'attachment; filename="week_report.xlsx"',
        })

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