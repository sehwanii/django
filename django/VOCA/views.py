from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import matplotlib.pyplot as plt
from pytesseract import Output
import pytesseract
import imutils
import cv2
import requests
import numpy as np


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
        typeList = []

        print(testId, classId, fileList)
        for content in testContentList:
            typeList.append(content['type'])
            print(content['id'], content['type'], content['question'], content['answer'])
        for member in memberList:
            print(member['id'], member['username'], member['name'])
            
        return_data = create_json_file(testId, classId, fileList, testContentList, memberList, typeList)
        # JSON 파일 처리
        # 예시로 받은 JSON 파일을 수정하여 응답으로 전송
        
        #modified_data = {'message': 'Received and modified JSON data'}
        return JsonResponse(return_data)
    elif request.method == 'GET':
        # GET 요청에 대한 응답
        return JsonResponse({'message': 'GET method received'})

    else:
        return JsonResponse({'message': 'POST method required'})
    

def create_json_file(testId, classId, fileList, testContentList, memberList, typeList):
    # JSON 데이터 생성
    data = {
        "testId": testId,
        "classId" : classId,
        "personalResultList": []
    }

    for url in fileList:
        user_id, user_answer = my_ocr(url,typeList)
        print(user_id)
        print("!!!!!")
        print(len(user_answer))
        print("!!!!!")
        for i in range(len(memberList)):
            if(memberList[i]["username"] == user_id):
                personal_result = {
                    "url" : url,
                    "username": user_id,
                    "name" : memberList[i]["name"],
                    "totalScore": 0,
                    "contentList": []
                }
                for j in range(len(user_answer)):
                    content = {
                        "contentId": testContentList[j]["id"],
                        "question": testContentList[j]["question"],
                        "answer": testContentList[j]["answer"],
                        "userAnswer": user_answer[j],
                        "result": user_answer[j] in testContentList[j]["answer"]
                    }

                    # 정답인 경우 점수 증가
                    if content["result"]:
                        personal_result["totalScore"] += 100/len(user_answer)
                    personal_result["contentList"].append(content)
            
        data["personalResultList"].append(personal_result)

    # JSON 파일 생성
    print(data)
    return data
    with open("data.json", "w") as json_file:
        json.dump(data, json_file)




#테스트 출력용 함수
def plt_imshow(title='image', img=None, figsize=(8 ,5)):
    plt.figure(figsize=figsize)
 
    if type(img) == list:
        if type(title) == list:
            titles = title
        else:
            titles = []
 
            for i in range(len(img)):
                titles.append(title)
 
        for i in range(len(img)):
            if len(img[i].shape) <= 2:
                rgbImg = cv2.cvtColor(img[i], cv2.COLOR_GRAY2RGB)
            else:
                rgbImg = cv2.cvtColor(img[i], cv2.COLOR_BGR2RGB)
 
            plt.subplot(1, len(img), i + 1), plt.imshow(rgbImg)
            plt.title(titles[i])
            plt.xticks([]), plt.yticks([])
 
        plt.show()
    else:
        if len(img.shape) < 3:
            rgbImg = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        else:
            rgbImg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
 
        plt.imshow(rgbImg)
        plt.title(title)
        plt.xticks([]), plt.yticks([])
        plt.show()


def my_ocr(url, type_list):

    user_return = []


    image_nparray = np.asarray(bytearray(requests.get(url).content), dtype=np.uint8)
    org_image = cv2.imdecode(image_nparray, cv2.IMREAD_COLOR)

    #plt_imshow("orignal image", org_image)

    image = org_image.copy()
    image = imutils.resize(image, width=500)
    ratio = org_image.shape[1] / float(image.shape[1])

    # 이미지를 grayscale로 변환하고 blur를 적용
    # 모서리를 찾기위한 이미지 연산
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5,), 0)
    edged = cv2.Canny(blurred, 75, 200)
    
    #plt_imshow(['gray', 'blurred', 'edged'], [gray, blurred, edged])
    #user id 추출
    x = 40
    y = 50
    w = 100
    h = 50
    border = 4
    id_image = image[y + border:y + h - border, x + border : x + w - border]
    #plt_imshow("Outline", id_image) 
    gray_image = cv2.cvtColor(id_image, cv2.COLOR_BGR2GRAY)
    gray_enlarge = cv2.resize(gray_image, (2*w, 2*h), interpolation=cv2.INTER_LINEAR)
    denoised = cv2.fastNlMeansDenoising(gray_enlarge, h=10, searchWindowSize=21, templateWindowSize=7)

    gray_pin = 196
    ret, thresh = cv2.threshold(denoised, gray_pin, 255, cv2.THRESH_BINARY)
    thresh[260:2090] = ~thresh[260:2090]
    result_image = np.hstack((denoised, thresh))
    user_id = pytesseract.image_to_string(denoised.copy(),lang='eng').strip()

    print(user_id)
    print(type_list[0])

    # contours를 찾아 크기순으로 정렬
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    
    Cnt = []
    
    # 정렬된 contours를 반복문으로 수행하며 4개의 꼭지점을 갖는 도형을 검출
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
    
        if len(approx) == 4:
            Cnt.append(approx)
    
    # 만약 추출한 윤곽이 없을 경우 오류
    if Cnt is None:
        raise Exception(("Could not find outline."))

    output = image.copy()
    cv2.drawContours(output, Cnt, -1, (0, 255, 0), 2)

    #plt_imshow("Outline", output)
    sorted_Cnt = sorted(Cnt, key=lambda x: x[0][0][1])

    
    user_return = []
    idx = 0
    english_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    print(sorted_Cnt)
    for contour in sorted_Cnt:
        print("1")
        x, y, w, h = cv2.boundingRect(contour)
        
        print(x,y,w,h)
        if(w<30 or h < 10):
            continue
        # if(h>500):
        #     continue
        cropped_image = image[y + border: y + h - border , x + border: x + w - border]
        #plt_imshow("Outline", cropped_image) 
        gray_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
        gray_enlarge = cv2.resize(gray_image, (2*w, 2*h), interpolation=cv2.INTER_LINEAR)
        denoised = cv2.fastNlMeansDenoising(gray_enlarge, h = 10, searchWindowSize=21, templateWindowSize=7)

        gray_pin = 196
        ret, thresh = cv2.threshold(denoised, gray_pin, 255, cv2.THRESH_BINARY)
        thresh[260:2090] = ~thresh[260:2090]
        result_image = np.hstack((denoised, thresh))

        if (type_list[idx] == 'KOR_TO_ENG'): #영어 OCR
            print("영어")
            
            #result = pytesseract.image_to_data(denoised.copy(), config=english_config, lang='eng',output_type=pytesseract.Output.DICT)
            detected_text = pytesseract.image_to_string(gray_enlarge.copy(), config=english_config, lang='eng').strip()
            # detected_text = result['text'][4]
            # if(len(result['text'])>5):
            #     for i in range(5,len(result['text'])):
            #         detected_text += result['text'][i]
            #bounding_box = [x,y,w,h]
            #confidence = min(result['conf'][4:])
            #ret_json.append({'bounding_box': bounding_box, 'text': detected_text.lower(), 'confidence':confidence})
            user_return.append(detected_text.lower())
            print(f"detected_text = {detected_text}")
            #plt_imshow("Outline", gray_enlarge) 
        else:   #한글 OCR
            print("한글")
            detected_text = pytesseract.image_to_string(gray_enlarge.copy(), config='--psm 6', lang='kor').strip()
            print(detected_text)
            # detected_text = result['text'][4]
            # if(len(result['text'])>5):
            #     for i in range(5,len(result['text'])):
            #         detected_text += result['text'][i]
            # bounding_box = [x,y,w,h]
            # confidence = min(result['conf'][4:])

            #ret_json.append({'bounding_box': bounding_box, 'text': detected_text.lower(), 'confidence':confidence})
            user_return.append(detected_text.lower())
            print(f"detected_text = {detected_text}")
            #plt_imshow("Outline", gray_enlarge) 
        idx+=1
    print(user_return)
    return user_id, user_return
    with open('test.json', 'w', encoding='utf-8') as make_file:
            json.dump(ret_json, make_file, ensure_ascii=False, indent="\t")


# def id_ocr(url):
#     image_nparray = np.asarray(bytearray(requests.get(url).content), dtype=np.uint8)
#     org_image = cv2.imdecode(image_nparray, cv2.IMREAD_COLOR)

#     plt_imshow("orignal image", org_image)

#     image = org_image.copy()
#     image = imutils.resize(image, width=500)
#     ratio = org_image.shape[1] / float(image.shape[1])

#     # 이미지를 grayscale로 변환하고 blur를 적용
#     # 모서리를 찾기위한 이미지 연산
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     blurred = cv2.GaussianBlur(gray, (5, 5,), 0)
#     edged = cv2.Canny(blurred, 75, 200)


#print(my_ocr('https://user-images.githubusercontent.com/69428232/148330274-237d9b23-4a79-4416-8ef1-bb7b2b52edc4.jpg'))