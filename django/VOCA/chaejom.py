import json
import ocr
def create_json_file(testId, classId, fileList, testContentList, memberList, typeList):
    # JSON 데이터 생성
    data = {
        "testId": testId,
        "classId" : classId,
        "personalResultList": []
    }

    for url in fileList:
        user_id, user_answer = ocr.my_ocr(url,typeList)
        for i in range(len(memberList)):
            if(memberList[i]["username"] == user_id):
                personal_result = {
                    "url" : url,
                    "username": user_id,
                    "name" : memberList[i]["name"],
                    "totalScore": 0,
                    "contentList": []
                }
                for j in len(user_answer):
                    content = {
                        "contentId": testContentList[j]["contentId"],
                        "question": testContentList[j]["question"],
                        "answer": testContentList[j]["answer"],
                        "userAnswer": user_answer[j],
                        "result": user_answer[j] in testContentList[j]["answer"]
                    }

                    # 정답인 경우 점수 증가
                    if content["result"]:
                        personal_result["totalScore"] += 100/user_answer
                personal_result["contentList"].append(content)
            
        data["personalResultList"].append(personal_result)

    # JSON 파일 생성
    print(data)
    return data
    with open("data.json", "w") as json_file:
        json.dump(data, json_file)


# 예시 데이터
# testId = 1
# questions = ["aboard", "apple", "cat"]
# answers = ["배위에, 기내에, 찻간에", "사과", "고양이"]
# testContentList = [
#         {
#             "id": 1,
#             "type": "ENG_TO_KOR",
#             "question": "aboard",
#             "answer": "배위에, 기내에, 찻간에"
#         },
#         {
#             "id": 2,
#             "type": "ENG_TO_KOR",
#             "question": "abroad",
#             "answer": "외국에, 해외로"
#         },
#         {
#             "id": 3,
#             "type": "ENG_TO_KOR",
#             "question": "akin",
#             "answer": "동족의, 동종의, 유사한"
#         }
#     ]
# memberList = [
#         {
#             "id": 1,
#             "username": "student1",
#             "name": "student1"
#         },
#         {
#             "id": 2,
#             "username": "student2",
#             "name": "student2"
#         }
#     ]
# url_list = ["url1", "url2"]

# JSON 파일 생성


def chaejeom_main(testId, classId, fileList, testContentList, memberList):
    json_file = create_json_file(testId, classId, fileList, testContentList, memberList)
    return json_file

#chaejeom_main(url_list, memberList)