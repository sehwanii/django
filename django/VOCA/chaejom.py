import json
import ocr
def create_json_file(member_list, test_data):
    # JSON 데이터 생성
    data = {
        "testId": testId,
        "personalResultList": []
    }

    # 개별 결과 생성
    for i in range(len(member_list)):
        personal_result = {
            "url" : member_list[i]["url"],
            "username": member_list[i]["username"],
            "name" : member_list[i]["name"],
            "totalScore": 0,
            "contentList": []
        }
        
        userAnswers = ocr.my_ocr(member_list[i]["url"])
        # 개별 문제 생성

        for j in range(len(test_data)):
            content = {
                "contentId": j + 1,
                "question": test_data[j]["question"],
                "answer": test_data[j]["answer"],
                "userAnswer": userAnswers[i][j],
                "result": userAnswers[i][j] in test_data[j]["answer"]
            }

        # for j in range(len(questions)):
        #     content = {
        #         "contentId": j + 1,
        #         "question": questions[j],
        #         "answer": answers[j],
        #         "userAnswer": userAnswers[i][j],
        #         "result": userAnswers[i][j] in answers[j]
        #     }
            
            # 정답인 경우 점수 증가
            if content["result"]:
                personal_result["totalScore"] += 10
            
            personal_result["contentList"].append(content)
        
        data["personalResultList"].append(personal_result)

    # JSON 파일 생성
    print(data)
    return data
    with open("data.json", "w") as json_file:
        json.dump(data, json_file)


def check_test_url(url_list, memberList):
    for url in url_list:
        id = ocr.id_ocr(url)
        for i in memberList:
            if(memberList[i]["username"] == id):
                memberList[i]["url"] = url
                break


# 예시 데이터
testId = 1
questions = ["aboard", "apple", "cat"]
answers = ["배위에, 기내에, 찻간에", "사과", "고양이"]
test_data = [
        {
            "id": 1,
            "type": "ENG_TO_KOR",
            "question": "aboard",
            "answer": "배위에, 기내에, 찻간에"
        },
        {
            "id": 2,
            "type": "ENG_TO_KOR",
            "question": "abroad",
            "answer": "외국에, 해외로"
        },
        {
            "id": 3,
            "type": "ENG_TO_KOR",
            "question": "akin",
            "answer": "동족의, 동종의, 유사한"
        }
    ]
memberList: [
        {
            "id": 1,
            "username": "student1",
            "name": "student1"
        },
        {
            "id": 2,
            "username": "student2",
            "name": "student2"
        }
    ]
url_list = ["url1", "url2"]

# JSON 파일 생성
create_json_file(memberList, test_data)
