from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def receive_data(request):
    if request.method == 'POST':
        received_data = json.loads(request.body)
        # 받은 JSON 파일 확인
        print("Received JSON data:", received_data)
        process_json(request)
        # JSON 파일 처리
        # 예시로 받은 JSON 파일을 수정하여 응답으로 전송
        modified_data = {'message': 'Received and modified JSON data'}
        return JsonResponse(modified_data)
    elif request.method == 'GET':
        # GET 요청에 대한 응답
        return JsonResponse({'message': 'GET method received'})

    else:
        return JsonResponse({'message': 'POST method required'})
    
def process_json(request):
    if request.method == 'POST':
        try:
            received_json = json.loads(request.body)
            # 여기서부터는 파싱된 JSON 데이터를 활용하여 원하는 작업 수행
            test_id = received_json['testID']
            class_id = received_json['classID']
            file_url = received_json['file']
            test_content_list = received_json['testContentList']
            member_list = received_json['memberList']
            
            
            # 파싱된 데이터 활용 예시
            print(test_id, class_id, file_url)
            for content in test_content_list:
                print(content['type'], content['question'], content['answer'])
            for member in member_list:
                print(member['id'], member['username'], member['name'])
            
            return JsonResponse({'message': 'JSON data processed successfully'})
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    else:
        return JsonResponse({'error': 'POST method required'}, status=405)