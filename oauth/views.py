from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json

# Create your views here.
def kakaoRequestLogin(request):
    client_id = "7347aa7b82ad90e1675c3065dc1ce2bf"
    redirect_uri = "http://172.19.8.34:8000/oauth/kakao/login/"
    app_uri = request.GET['appURI']
    fail_app_uri = request.GET['failAppURI']

    request.session['clientID'] = client_id
    request.session['redirectURI'] = redirect_uri
    request.session['appURI'] = app_uri
    request.session['failAppURI'] = fail_app_uri

    loginRequestURI = f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope=talk_message";

    return redirect(loginRequestURI)

def getKakaotalkUserProfile(access_token):
    headers = {
        'Content-Type': "application/x-www-form-urlencoded;charset=utf-8",
        'Authorization': f"Bearer {access_token}",
    }

    kakao_user_profile_uri = 'https://kapi.kakao.com/v2/user/me'

    response = requests.get(kakao_user_profile_uri, headers=headers).json()

    return response

def kakaoGetCode(request):
    try:
        code = request.GET['code']
        
        return JsonResponse({
            'success': 'true',
            'code': code,
        }, json_dumps_params = { 'ensure_ascii': True })
    except Exception:
        return JsonResponse({
            'success': False,
        }, json_dumps_params = { 'ensure_ascii': True })

@csrf_exempt
def kakaoLogin(request):
    if request.method == "POST":
        client_id = request.POST['clientID']
        redirect_uri = request.POST['redirectURI']
        code = request.POST['code']
        # print(f"client_id = {client_id}")
        # print(f"redirect_uri = {redirect_uri}")
        # print(f"code = {code}")

        access_token_request_uri = f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}"
        # print(access_token_request_uri)

        access_token_request_uri_data = requests.get(access_token_request_uri)
        json_data = access_token_request_uri_data.json()
        # print(json_data)

        try:
            access_token = json_data['access_token']

            user_profile_info = getKakaotalkUserProfile(access_token)
            user_id = user_profile_info['id']
            nick_name = user_profile_info['kakao_account']['profile']['nickname']
            
            return JsonResponse({
                'success': True,
                'kakaoAccessToken': access_token,
                'userID': user_id,
                'nickName': nick_name,
            }, json_dumps_params = { 'ensure_ascii': True })
        except KeyError:
            pass

    return JsonResponse({
        'success': False,
    }, json_dumps_params = { 'ensure_ascii': True })

@csrf_exempt
def kakaoLogout(request):
    if request.method == "POST":
        access_token = request.POST['kakaoAccessToken']

        headers = {
            'Authorization': f"Bearer {access_token}",
        }

        kakao_logout_uri = 'https://kapi.kakao.com/v1/user/logout'

        resopnse = requests.get(kakao_logout_uri, headers=headers).json()

        return JsonResponse({
            'success': True,
        }, json_dumps_params = { 'ensure_ascii': True })

    return JsonResponse({
        'success': False,
    }, json_dumps_params = { 'ensure_ascii': True})

def send_to_me(request):
    access_token = request.session.get('kakaoAccessToken')
    template_dict_data = str({
        "object_type": "feed",
        "content": {
            "title": "디저트 사진",
            "description": "아메리카노, 빵, 케익",
            "image_url": "http://mud-kage.kakao.co.kr/dn/NTmhS/btqfEUdFAUf/FjKzkZsnoeE4o19klTOVI1/openlink_640x640s.jpg",
            "image_width": 640,
            "image_height": 640,
            "link": {
                "web_url": "http://www.daum.net",
                "mobile_web_url": "http://m.daum.net",
                "android_execution_params": "contentId=100",
                "ios_execution_params": "contentId=100"
            }
        },
        "social": {
            "like_count": 100,
            "comment_count": 200,
            "shared_count": 300,
            "view_count": 400,
            "subscriber_count": 500
        },
        "buttons": [
            {
                "title": "웹으로 이동",
                "link": {
                    "web_url": "http://www.daum.net",
                    "mobile_web_url": "http://m.daum.net"
                }
            },
            {
                "title": "앱으로 이동",
                "link": {
                    "android_execution_params": "contentId=100",
                    "ios_execution_params": "contentId=100"
                }
            }
        ]
    })

    kakao_to_me_uri = 'https://kapi.kakao.com/v2/api/talk/memo/default/send'

    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Authorization': "Bearer " + access_token,
    }

    template_json_data = "template_object=" + str(json.dumps(template_dict_data))
    template_json_data = template_json_data.replace("\"", "")
    template_json_data = template_json_data.replace("'", "\"")
    
    response = requests.request(method="POST", url=kakao_to_me_uri, data=template_json_data, headers=headers)
    print(response.json())

    return redirect(str(request.session.get('appURI')))