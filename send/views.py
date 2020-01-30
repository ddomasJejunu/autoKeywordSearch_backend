from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json

# Create your views here.
def kakaoPush(request):
    return JsonResponse({
        'success': False,
    }, json_dumps_params = { 'ensure_ascii': True })

@csrf_exempt
def kakaoSendToMe(request):
    search_url = request.POST['searchURL']
    keywords = request.POST['keywords']
    template_dict_data = str({
        "object_type": "text",
        "text": f"{search_url}에서 키워드 {keywords}가 검색되었습니다!",
            'link': {
                "mobile_web_url": search_url
            }
    })

    kakao_to_me_uri = 'https://kapi.kakao.com/v2/api/talk/memo/default/send'
    
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Authorization': "Bearer " + request.POST['accessToken'],
    }

    template_json_data = "template_object=" + str(json.dumps(template_dict_data))
    template_json_data = template_json_data.replace("\"", "")
    template_json_data = template_json_data.replace("'", "\"")
    
    response = requests.request(method="POST", url=kakao_to_me_uri, data=template_json_data, headers=headers)
    response = response.json()

    if response["result_code"] == "0":
        return JsonResponse({
            'success': True,
        }, json_dumps_params = { 'ensure_ascii': True })
    else:
        return JsonResponse({
            'success': False,
        }, json_dumps_params = { 'ensure_ascii': True })