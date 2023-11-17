from django.http import JsonResponse, HttpRequest
import requests
def send_request_to_another_server(request):
    if request.method == 'GET':
        # 요청에 필요한 데이터 처리
        # ...

        # 요청 보내기
        url = 'http://127.0.0.1:8080/VOCA/'
        data_to_send = {'key': 'value', 'another_key': 'another_value'}  # 보낼 JSON 데이터
        
        # JSON 데이터를 POST 요청으로 보내기
        response = requests.post(url, json=data_to_send)
        
        # 요청에 대한 응답 확인
        if response.status_code == 200:
            # 수정된 JSON 파일 확인
            modified_data = response.json()
            print("Modified JSON data from another server:", modified_data)
            return JsonResponse(modified_data)
        else:
            return JsonResponse({'message': 'Failed to send JSON data'})
    else:
        return JsonResponse({'message': 'GET method required'})