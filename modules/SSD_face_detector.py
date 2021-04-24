import cv2  # openCV 패키지
import numpy as np
import glob
import menu


faceProto = "opencv_face_detector.pbtxt"
faceModel = "opencv_face_detector_uint8.pb"
ageModel=cv2.dnn.readNet('faceModel.pb')
faceNet = cv2.dnn.readNet(faceModel, faceProto)

def highlightFace(net, frame, conf_threshold=0.7):  # conf_threshold: 임계값
    frameSSD = frame.copy()  # 객체 복사
    frameHeight = frameSSD.shape[0]  # 수직
    frameWidth = frameSSD.shape[1]  # 수평
    blob = cv2.dnn.blobFromImage(frameSSD, 1.0, (300, 300), [104, 117, 123], True, False)
    # blob: 4차원 블롭 객체
    # (frame, scale factor ,(출력영상크기) ,[조명변화 방지용 RGB 빼기] ,bgr->rgb ,크롭수행안함)
    net.setInput(blob)
    # blob을 네트워크 입력으로 설정
    detections = net.forward()
    # 네트워크 순방향 실행(추론과정)
    # detections : 1x1xNx7 차원 행렬 -> Nx7 7개의 종류를 가진 데이터 N개 존재(얼굴 후보군)
    # [0,0,N,2] 신뢰도 , [0,0,N,3~6] 좌측상단(x,y) 우측하단(x,y) 꼭지점좌표
    faceBoxes = []
    for i in range(detections.shape[2]):  # detections.shape[2]=N
        confidence = detections[0, 0, i, 2]
        if confidence > conf_threshold:
            x1 = int(detections[0, 0, i, 3] * (frameWidth))
            y1 = int(detections[0, 0, i, 4] * (frameHeight-50))
            x2 = int(detections[0, 0, i, 5] * (frameWidth))
            y2 = int(detections[0, 0, i, 6] * (frameHeight))
            faceBoxes.append([x1, y1, x2, y2])
            cv2.rectangle(frameSSD, (x1, y1), (x2, y2), (0, 0, 0), int(round(frameHeight / 1500)), 8)
    return frameSSD, faceBoxes
    
def facecheck():
    while True:
        check, frame = menu.cap.read()
        result, faceBoxes = highlightFace(faceNet, frame)
        if not faceBoxes:
            print("No face detected")
        else:
            break
        
    while True:
        space=[]
        for k in faceBoxes:
            space.append((k[2]-k[0])*(k[3]-k[1]))
        
        num=0
        check=0
        for k in range(len(space)):
            if space[k]>check:
                check=space[k]
                num=k
        dst=result[faceBoxes[num][1]:faceBoxes[num][3], faceBoxes[num][0]:faceBoxes[num][2]]

        blob = cv2.dnn.blobFromImage(dst, 1.0/255,(224, 224),[0,0,0], swapRB=True)
        ageModel.setInput(blob)
        preds=ageModel.forward()
        
        dd= dict()
        dd[1]=0
        dd[0]=1
        dd[2]=2

        return dd[np.argmax(preds[0])]

def save(name):
    frame1=frame2=0
    flag=False
    while True:
        check, frame1 = menu.cap.read()
        result, faceBoxes1 = highlightFace(faceNet, frame1)
        if not faceBoxes1:
            print("No face detected")
        elif flag:
            break
        else:
            flag=True
            frame2=frame1
            faceBoxes2=faceBoxes1
        
    faceBoxes1.sort(key=lambda k: (k[2]-k[0])*(k[3]-k[1]),reverse=True)
    dst1=result[faceBoxes1[-1][1]:faceBoxes1[-1][3], faceBoxes1[-1][0]:faceBoxes1[-1][2]]
    faceBoxes2.sort(key=lambda k: (k[2]-k[0])*(k[3]-k[1]),reverse=True)
    dst2=result[faceBoxes2[-1][1]:faceBoxes2[-1][3], faceBoxes2[-1][0]:faceBoxes2[-1][2]]
    cv2.imwrite('../image/member/'+str(name).zfill(5)+'.jpg',dst1)
    cv2.imwrite('../image/member/'+str(name+1).zfill(5)+'.jpg',dst2)
    
    blob = cv2.dnn.blobFromImage(dst1, 1.0/255,(224, 224),[0,0,0], swapRB=True)
    ageModel.setInput(blob)
    preds=ageModel.forward()

    #{'middle': 0, 'old': 1, 'young': 2}

    # old=0 middle=1 young=2

    dd= dict()
    dd[1]=0
    dd[0]=1
    dd[2]=2
    return dd[np.argmax(preds[0])]
    
