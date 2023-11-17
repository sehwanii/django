import json

def create_json_file(testId, usernames, questions, answers, userAnswers):
    # JSON 데이터 생성
    data = {
        "testId": testId,
        "personalResultList": []
    }

    # 개별 결과 생성
    for i in range(len(usernames)):
        personal_result = {
            "username": usernames[i],
            "totalScore": 0,
            "contentList": []
        }
        
        # 개별 문제 생성
        for j in range(len(questions)):
            content = {
                "contentId": j + 1,
                "question": questions[j],
                "answer": answers[j],
                "userAnswer": userAnswers[i][j],
                "result": userAnswers[i][j] in answers[j]
            }
            
            # 정답인 경우 점수 증가
            if content["result"]:
                personal_result["totalScore"] += 10
            
            personal_result["contentList"].append(content)
        
        data["personalResultList"].append(personal_result)

    # JSON 파일 생성
    with open("data.json", "w") as json_file:
        json.dump(data, json_file)

# 예시 데이터
testId = 1
usernames = ["student1", "student2"]
questions = ["aboard", "apple", "cat"]
answers = ["배위에, 기내에, 찻간에", "사과", "고양이"]
userAnswers = [["배위에", "사과", "고양이"], ["배위에", "apple", "cat"]]

# JSON 파일 생성
create_json_file(testId, usernames, questions, answers, userAnswers)
