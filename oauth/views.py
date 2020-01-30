from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from .models import User
import requests
import json

# Create your views here.
def getKakaoUserInfo(access_token):
    headers = {
        'Content-Type': "application/x-www-form-urlencoded;charset=utf-8",
        'Authorization': f"Bearer {access_token}",
    }

    kakao_user_profile_uri = 'https://kapi.kakao.com/v2/user/me'

    response = requests.get(kakao_user_profile_uri, headers=headers).json()

    return response

# django view.py response 방식 - https://wayhome25.github.io/django/2017/03/19/django-ep3-fbv/
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

# django post 데이터 받기 - https://stackoverflow.com/questions/17716624/django-csrf-cookie-not-set
@csrf_exempt
def kakaoLogin(request):
    if request.method == "POST":
        client_id = request.POST['clientID']
        redirect_uri = request.POST['redirectURI']
        code = request.POST['code']
        uuid = request.POST.get('deviceID', None)
        platform = request.POST.get('platform', None)
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

            user_info = getKakaoUserInfo(access_token)
            user_id = user_info['id']
            user_account_info = user_info['kakao_account']
            nick_name = user_account_info['profile']['nickname']
            is_user_email = False
            user_email = None

            try:
                if not user_account_info['email_needs_agreement'] and user_account_info['is_email_valid'] and user_account_info['is_email_verified']:
                    is_user_email = True
                    user_email = user_info['kakao_account']['email']
            except:
                pass

            is_regist = False

            try:
                user = User.objects.get(id=user_id)

                if uuid:
                    User.objects.filter(id=user_id).update(device_id=uuid, platform=platform)

                is_regist = True
            except ObjectDoesNotExist:
                # django model에 데이터 추가 - https://jay-ji.tistory.com/19
                if uuid:
                    user = User(id=user_id, email=user_email, device_id=uuid, platform=platform)
                    user.save()
                else:
                    user = User(id=user_id, email=user_email)
                    user.save()

            User.objects.filter(id=user_id).update(access_token=access_token)
            
            return JsonResponse({
                'success': True,
                'kakaoAccessToken': access_token,
                'userID': user_id,
                'nickName': nick_name,
                'isUserEmail': is_user_email,
                'userEmail': user_email,
                'isRegist': is_regist
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