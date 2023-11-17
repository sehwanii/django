from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def receive_data(request):
    if request.method == 'POST':
        received_data = json.loads(request.body)
        # 받은 JSON 파일 확인
        print("Received JSON data:", received_data)

        # JSON 파일 처리
        # 예시로 받은 JSON 파일을 수정하여 응답으로 전송
        modified_data = {'message': 'Received and modified JSON data'}
        return JsonResponse(modified_data)
    elif request.method == 'GET':
        # GET 요청에 대한 응답
        return JsonResponse({'message': 'GET method received'})

    else:
        return JsonResponse({'message': 'POST method required'})