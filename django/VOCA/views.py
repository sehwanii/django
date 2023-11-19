from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import chaejom

@csrf_exempt
def receive_data(request):
    if request.method == 'POST':
        received_json = json.loads(request.body)

        # 여기서부터는 파싱된 JSON 데이터를 활용하여 원하는 작업 수행
        testId = received_json['testID']
        classId = received_json['classID']
        fileList = received_json['file']
        testContentList = received_json['testContentList']
        memberList = received_json['memberList']

        print(testId, classId, fileList)
        for content in testContentList:
            print(content['id'], content['type'], content['question'], content['answer'])
        for member in memberList:
            print(member['id'], member['username'], member['name'])
            
        return_data = chaejom.create_json_file(testId, classId, fileList, testContentList, memberList)
        # JSON 파일 처리
        # 예시로 받은 JSON 파일을 수정하여 응답으로 전송
        
        #modified_data = {'message': 'Received and modified JSON data'}
        return JsonResponse(return_data)
    elif request.method == 'GET':
        # GET 요청에 대한 응답
        return JsonResponse({'message': 'GET method received'})

    else:
        return JsonResponse({'message': 'POST method required'})
    