# Fall_Detection_System
* 제11회 2021 숭실 캡스톤디자인 경진대회 은상
* 발표영상 : result/캡스톤디자인 발표자료_유안낌벌리.mp4
* 구성원 : 김준용, 유기준, 안서연, 김현우

## 개요
노인 비율이 기하급수적으로 증가하는 우리나라에서 낙상은 노년 생활의 가장 큰 위험 요소입니다.  
치매환자, 독거노인, 기저질환 등 일상 속에서 낙상의 위험이 있는 사람들의 갑작스런 사고에 수월하게 대처할 수 있고  
넘어지고 나서 바로 신고가 이루어 진다면 골든 타임을 놓치는 상황을 막을 수 있습니다.

## 설계
![image](https://user-images.githubusercontent.com/62223905/136489126-fb849000-d6dc-4c4f-8c2e-fc7ba41c7022.png)

## 구현 방법
![image](https://user-images.githubusercontent.com/62223905/136489277-20dff04c-082e-40df-95f1-e2e067fb6d67.png)

## 차이점
* 기존 낙상감지는 대부분 센서에 있는 가속도 센서와 자이로스코프 센서를 이용하여 감지했습니다.  
* 센서는 항상 몸에 지니고 있어야 하는 단점이 있습니다.  
* Apple watch등과 같이 기계안에 센서를 결합시켰다면 충전이 필요합니다.  
* Openpose를 동작 시킬 때 두 명이상일 경우는 낙상 신고가 가능하므로 동작을 멈춰서 효율적으로 동작합니다.  
* 기존에 낙상 감지 및 알림을 넘어 신고 기능을 추가하여 119 및 보호자에게 신속하게 연락할 수 있습니다.  
* 낙상으로 추정될 시 영상을 캡처하여 사진으로 첨부하여 전송이 가능하므로 신고의 정확도를 높일 수 있습니다.  

## References
[1] Daniil Osokin(2018.11), “Real-time 2D Multi-Person Pose Estimation on CPU:Lightweight OpenPose”  
[2] 임동하, 박철호, 김상훈, 유윤섭, “3축 가속도 센서를 이용한 낙상 감지 시스템”, 한국정보처리학회 ,2013 May 10 , 2013년, pp.356 – 358  
[3] 한도협, 지석훈, 배연두, 김한슬, “ 가속도 센서 기반의 낙상 감지 알고리즘에 대한 연구”, 한국IT정책경영학회 논문지, ’20-12 Vol.12 No.06  
[4] 강윤규, 이지나, 신용태, “순환신경망, GRU를 이용한 자세 추정 기반 낙상 감지 기법”, 한국IT정책경영학회 논문지, ’20-10 Vol.12 No.06  
[5] 강윤규, 강희용, 원달수, “PoseNet과 GRU를 이용한 Skeleton Keypoints 기반 낙상 감지”, 한국IT정책경영학회 논문지, Vol. 22, No. 2 pp. 127-133, 2021  
[6] 정필성, 조양현, “사물인터넷 기반의 낙상 감지 시스템”, 한국정보통신학회논문지, Vol. 19, No. 11 : 2546~2553 Nov. 2015  


