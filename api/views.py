from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from .models import User, Keywordsearch
from datetime import datetime

# Create your views here.
# rest_framework 없이 rest api 작성 - https://cholol.tistory.com/468?category=739855
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

@csrf_exempt
def search_list(request):
    if request.method == 'POST':
        user_no = -1
        try:
            user_no = User.objects.get(id=request.POST['userID']).no
        except ObjectDoesNotExist:
            pass
            
        search_list = list(Keywordsearch.objects.filter(user_no=user_no).values('no', 'search_url', 'keywords', 'start_time', 'end_time', 'complete_time'))
        for item in search_list:
            for key in item:
                if type(item[key]) is datetime:
                    item[key] = item[key].strftime('%Y/%m/%d %H:%M:%S')
        count = len(search_list)

        return JsonResponse({
            'success': True,
            'count': count,
            'searchList': search_list,
        }, json_dumps_params = { 'ensure_ascii': True })

    return JsonResponse({
        'success': False,
    }, json_dumps_params = { 'ensure_ascii': True })

def update(request):
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