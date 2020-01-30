from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from .models import User, Keywordsearch
from datetime import datetime

# Create your views here.
# rest_framework 없이 rest api 작성 - https://cholol.tistory.com/468?category=739855
# CRUD 기능 - https://wayhome25.github.io/django/2017/04/01/django-ep9-crud/
@csrf_exempt
def create(request):
    if request.method == 'POST':
        search_url = request.POST['searchURL']
        keywords = request.POST['keywords']
        user_id = request.POST['userID']
        end_time = datetime.strptime(request.POST['endTime'], "%Y-%m-%d %H:%M")

        if (datetime.now() < end_time):
            Keywordsearch.objects.create(search_url=search_url, keywords=keywords, user_no=User.objects.get(id=user_id), end_time=end_time)

            return JsonResponse({
                'success': True,
            }, json_dumps_params = { 'ensure_ascii': True })

    return JsonResponse({
        'success': False,
    }, json_dumps_params = { 'ensure_ascii': True })

def check_list(request):
    search_list = Keywordsearch.objects.filter(end_time < today, complete_time != null).values('no', 'search_url', 'keywords', 'end_time')

    for item in search_list:
        for key in item:
            if type(item[key]) is datetime:
                item[key] = item[key].strftime('%Y/%m/%d %H:%M')

    return JsonResponse({
        'searchList': search_list,
    }, json_dumps_params = { 'ensure_ascii': True })

@csrf_exempt
def search_list(request):
    if request.method == 'POST':
        # select
        if request.POST.get('userID', None):
            search_list = list(Keywordsearch.objects.filter(user_no=User.objects.get(id=request.POST['userID'])).values('no', 'search_url', 'keywords', 'start_time', 'end_time', 'complete_time'))

            for item in search_list:
                for key in item:
                    if type(item[key]) is datetime:
                        item[key] = item[key].strftime('%Y/%m/%d %H:%M')
        # update
        elif request.POST.get('no', None):
            search_list = list(Keywordsearch.objects.filter(no=request.POST["no"]).values('search_url', 'keywords', 'end_time'))
        
        count = len(search_list)

        return JsonResponse({
            'success': True,
            'count': count,
            'searchList': search_list,
        }, json_dumps_params = { 'ensure_ascii': True })

    return JsonResponse({
        'success': False,
    }, json_dumps_params = { 'ensure_ascii': True })

def complete(request):
    try:
        no = request.GET['no']
        complete_time = request.GET['completeTime']

        Keywordsearch.objects.filter(no=no).update(complete_time=datetime.strptime(complete_time, "%Y-%m-%d %H:%M"))

        return JsonResponse({
            'success': True,
        }, json_dumps_params = { 'ensure_ascii': True })
    except Exception:
        pass

    return JsonResponse({
        'success': False,
    }, json_dumps_params = { 'ensure_ascii': True })

@csrf_exempt
def update(request):
    if request.method == 'POST':
        searching_no = request.POST['no']
        search_url = request.POST['searchURL']
        keywords = request.POST['keywords']
        end_time = datetime.strptime(request.POST['endTime'], "%Y-%m-%d %H:%M")

        if (datetime.now() < end_time):
            count = Keywordsearch.objects.filter(no=searching_no).update(search_url=search_url, keywords=keywords, end_time=end_time)

            return JsonResponse({
                'success': True,
            }, json_dumps_params = { 'ensure_ascii': True })

    return JsonResponse({
        'success': False,
    }, json_dumps_params = { 'ensure_ascii': True })

@csrf_exempt
def delete(request):
    if request.method == 'POST':
        no_list = request.POST['no'].split(',')
        
        for no in no_list:
            try:
                Keywordsearch.objects.get(no=no).delete()
            except Exception:
                pass

        return JsonResponse({
            'success': True,
        }, json_dumps_params = { 'ensure_ascii': True })

    return JsonResponse({
        'success': False,
    }, json_dumps_params = { 'ensure_ascii': True })