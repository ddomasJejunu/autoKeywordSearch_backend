from django.shortcuts import render

# Create your views here.
def kakaoPush(request):
    return JsonResponse({
        'success': False,
    }, json_dumps_params = { 'ensure_ascii': True })

def kakaoSendToMe(request):
    return JsonResponse({
        'success': False,
    }, json_dumps_params = { 'ensure_ascii': True })