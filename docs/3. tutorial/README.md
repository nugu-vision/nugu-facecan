# Tutorial

 간단하게 알아본 얼굴인식 서비스의 실제 사용을 위해 SK OpenAPI를 사용하여 어떻게 연동할 수 있는지 알아보겠습니다. 간단한 가정을 하고, 거기에 맞는 DB를 구축하고 그에 따른 사용 방법을 실습합니다. 간단한 가정과 실습에는 Postman과 같은 REST API 접근을 위한 도구를 활용하거나, curl 명령을 이용하도록 합니다. 여기서는 curl 명령을 이용하여 진행합니다. 

먼저, 다음과 같은 환경을 가정합니다. A 라는 회사의 1층/2층에 각각 얼굴인식을 위한 시스템을 구성하고자 합니다. 1/2층 각각 서로 다른 구성원이 근무하고 있으며, 1층에는 A, B 사원, 2층에는 C, D 사원이 있다. 이런 경우에 어떤 식으로 얼굴인식을 위한 DB 구축을 할지 하나씩 살펴봅니다.


본 문서에서 다루는 내용은 얼굴인식API 구조에 대한 이해와 사용을 위한 것이고, 그 외의 내용은 다루지 않습니다. 실제 서비스 구축에는 얼굴의 촬영을 위한 App 개발이나 Device 연동 등이 필요합니다. 


<br>
<br>

> ## SK OpenAPI Key

우선 SK OpenAPI에 가입하고, 얼굴인식 서비스의 사용 신청을 하면 Key 메뉴에서 다음의 [Fig 1.](#fig_1) 과 같이 Project Key(App Key) 와 Access Key Name에 해당하는 app-id 라는 이름과 Access Key Value 값을 얻을 수 있습니다. 이 두 값은 해당 API를 사용하는 데 있어서 필수적인 값이며, 신청할때 임의로 생성되어 제공 됩니다. 앞으로 이 계정을 사용하여 테스트하기 위해 지속적으로 사용되는 값이니 따로 기록해둡니다.

<br>

- appKey : l7xx4bfa60c6bc8945819a114c5e34cc930c  
- app-id : GZ0E4G4YI1

<br>

<p />
<p /><a name="fig_1">Fig. 1</a> appKey, app-id 
<p /><img src="figures/fig1.appkey,appid.jpg">


<br>
<br>


> ## Group 생성 및 확인

<br>
1/2층 각각 다른 구성원이 근무하고, 1층은 A, B 사원, 2층은 C, D 사원이 있기 때문에, Group/Subject 은 다음과 같이 구성합니다.  

<br>

Group 1층 - Subject A, B  
Group 2층 - Subject C, D 

<br>

우선 가장 큰 카테고리인 Group을 만들고, 제대로 만들어졌는지 확인하고 난 후, Subject을 하나씩 추가하도록 합니다. 그리고 난 후, A, B, C, D에 맞는 각각의 얼굴 사진을 추가한 이후에 정상적으로 기능이 동작하는지 확인하도록 합니다.  
먼저 1층 Group을 만들도록 합니다. 이름은 한글을 사용할 수 없으므로 1st-floor 로 지정하여 만들도록 합니다.

<br>


|Category|Contents|
|---|---|
|Request| curl --location <br> --request POST 'https://apis.openapi.sk.com/nugufacecan/v1/group' <br> --header 'appKey: l7xx4bfa60c6bc8945819a114c5e34cc930c' <br> --header 'app-id: GZ0E4G4YI1' <br> --header 'group-name: 1st-floor' <br> |
|Response| 200 OK  <pre>{<br>  “group_id”: “80NOKFZPAL”,<br>  “group_name”: “1st-floor”,<br>  “transaction_id”: “F00003858A8P”<br> }</pre>  |

- (주의) 여기서 group_id, transaction_id 는 임의 생성되므로 예시와 값이 다름

<br>

이와 같이 api/face/group에 POST 형태로 헤더를 appKey, app-id, 그리고 생성할 그룹의 이름인 group-name을 추가하여 실행하면, 정상적으로 생성이 되었으며 200 OK 와 함께, group-name에 맞는 group-id를 Response 로 받을 수 있습니다. 이를 활용하여, Subject A, B를 추가할때는 group-id를 헤더에 추가하여 Group 1층에 사람을 추가할 수 있습니다.  
정상적으로 Group 이 추가되었는지 확인은 다음과 같이 동일 URL에 GET 형태로 appKey, app-id 만을 헤더로 추가하여 수행하면 됩니다. 해당 명령을 수행하면, 추가된 모든 Group 정보를 확인할 수 있습니다.

<br>

|Category|Contents|
|---|---|
|Request| curl --location <br><ensp> --request GET 'https://apis.openapi.sk.com/nugufacecan/v1/group' <br><ensp> --header 'appKey: l7xx4bfa60c6bc8945819a114c5e34cc930c' <br><ensp> --header 'app-id: GZ0E4G4YI1' |
|Response| 200 OK <pre>{<br>  {<br>    “group_id”: “80NOKFZPAL”,<br>    “group_name”:“1st-floor”,<br>  }<br>}</pre> |
    
<br>
정상적으로 추가된 것을 확인하면 이어서, 2층 Group을 추가하도록 합니다.   

<br>

|Category|Contents|
|---|---|
|Request| curl --location <br> --request POST 'https://apis.openapi.sk.com/nugufacecan/v1/group' <br> --header 'appKey: l7xx4bfa60c6bc8945819a114c5e34cc930c' <br> --header 'app-id: GZ0E4G4YI1' <br> --header 'group-name: 2nd-floor' <br> |
|Response| 200 OK  <pre>{<br>  “group_id”: "RQFW3CNS3V",<br>  “group_name”: “2nd-floor”,<br>  “transaction_id”: "H00003858A9I"<br> }</pre>  |

<br>

마찬가지로 다시 GET을 통하여 정상적으로 Group 2개가 추가되었는지 확인합니다. 만약 정상적으로 추가되었다면 다음과 같은 결과를 확인할 수 있습니다.

<br>

|Category|Contents|
|---|---|
|Request| curl --location <br><ensp> --request GET 'https://apis.openapi.sk.com/nugufacecan/v1/group' <br><ensp> --header 'appKey: l7xx4bfa60c6bc8945819a114c5e34cc930c' <br><ensp> --header 'app-id: GZ0E4G4YI1' |
|Response| 200 OK <pre>{<br>  {<br>    “group_id”: “80NOKFZPAL”,<br>    “group_name”:“1st-floor”,<br>  },<br>  {<br>    "group_id": "RQFW3CNS3V", <br>    "group_name": "2nd-floor" <br>  } <br>}</pre> |


> ## Subject 생성 및 확인

<br>

이제 1층/2층 Group의 구성이 완료되었으니 이에 Subject 데이터를 추가하도록 합니다. 1층은 A, B, 2층은 C, D인데, 1층의 group_id는 “80NOKFZPAL” 이고, 2층은 “RQFW3CNS3V” 이므로 다음과 같이 Subject에 대한 추가를 진행합니다.

<br>

|Category|Contents|
|---|---|
|Request| curl --location <br><ensp> --request POST 'https://apis.openapi.sk.com/nugufacecan/v1/subject' <br><ensp> --header 'appKey: l7xx4bfa60c6bc8945819a114c5e34cc930c' <br><ensp> --header 'app-id: GZ0E4G4YI1' <br><ensp> --header 'group-id: 80NOKFZPAL' <br><ensp>  --header 'subject-name: A'   |
|Response| 200 OK <pre>{<br>  “subject_id”: “8YLHWXT0K0”,<br>   "group_name”: “1st-floor”,<br>  “subject_name”: “A”,<br>   "transaction_id”: “D00003858AAB” <br>} </pre> |


정상적으로 추가가 완료되면, 위와 같이 subject_id 가 부여되고, 추가한 정보들도 같이 나열됩니다. 위와 A를 추가한 방식으로 나머지 B, C, D를 모두 추가하고, Group 과 마찬가지로 /api/open/face/subject에 GET으로 호출하면, 정상적으로 추가되었을 경우 아래와 같이 볼 수 있습니다.


|Category|Contents|
|---|---|
|Request| curl --location <br> --request GET 'https://apis.openapi.sk.com/nugufacecan/v1/subject' <br> --header 'appKey: l7xx4bfa60c6bc8945819a114c5e34cc930c' <br> --header 'app-id: GZ0E4G4YI1' <br> --header 'group-id: VOFLIDEYD6' |
|Response| 200 OK <pre>{<br>  {<br>    “subject_id”: “8YLHWXT0K0”,<br>     "group_name”: “1st-floor”,<br>    “subject_name”: “A”,<br>  }, <br>  {<br>    "subject_id": "M0N69EP2VJ",<br>    "group_name": "1st-floor", <br>    "subject_name": "B"<br>   }<br>} </pre> |


|Category|Contents|
|---|---|
|Request| curl --location <br> --request GET 'https://apis.openapi.sk.com/nugufacecan/v1/subject' <br> --header 'appKey: l7xx4bfa60c6bc8945819a114c5e34cc930c' <br> --header 'app-id: GZ0E4G4YI1' <br> --header 'group-id: 80NOKFZPAL'' |
|Response| 200 OK <pre>{<br>  {<br>    “subject_id”: “2GEMZVDYE4”,<br>     "group_name”: “2nd-floor”,<br>    “subject_name”: “C”,<br>  }, <br>  {<br>    "subject_id": "YN5V8SG213",<br>    "group_name": "2nd-floor", <br>    "subject_name": "D"<br>   }<br>} </pre> |

<br>

> ## Face 추가와 확인

<br>

Face 역시 마찬가지로 group-id, subject-id를 header 로 넣고, face_name을 추가로 지정해서 파라미터로 넣습니다. 그리고 해당 인물의 얼굴이 있는 사진을 첨부하여 넣는데, 이때, 한 사람의 여러 형태의 얼굴 데이터를 넣는 것이 인식률 향상에 도움이 될 수 있습니다. 아래의 코드와 같이 form 형태로 이미지 데이터를 넣으면 Response는 200 OK 외에 아무것도 나타나지 않으며, 정상적으로 처리가 됩니다.

<br>

|Category|Contents|
|---|---|
|Request| curl --location <br>--request POST 'https://apis.openapi.sk.com/nugufacecan/v1/face' <br>--header 'appKey: l7xx4bfa60c6bc8945819a114c5e34cc930c' <br> --header 'app-id: GZ0E4G4YI1' <br> --header 'group-id: VOFLIDEYD6' <br>--header 'subject-id: 8YLHWXT0K0 <br> --header 'face-name: A_face' <br> --form 'image=@"A_face_1.jpg"' |
|Response| 200 OK |

<br>

Face 역시 Group/Subject 와 같이 GET 으로 호출하면, 얼굴 데이터가 정상적으로 추가 되었는지 확인할 수 있는데, 정상적으로 추가 된 경우 아래와 같은 형태로 Response 를 확인할 수 있습니다. 

<br>

|Category|Contents|
|---|---|
|Request| curl --location <br>--request GET 'https://apis.openapi.sk.com/nugufacecan/v1/face' <br>--header 'appKey: l7xx4bfa60c6bc8945819a114c5e34cc930c' <br>--header 'app-id: GZ0E4G4YI1' <br>--header 'group-id: VOFLIDEYD6' <br> --header 'subject-id: 8YLHWXT0K0' |
|Response| 200 OK <pre>[<br>  {<br>    "face_id": "AIF2SGCB9R",<br>    "face_name": "A",<br>    "box": {<br>      "landmark": [<br>        315.33056640625,<br>        395.97271728515625,<br>        509.1438293457031,<br>        382.5447692871094,<br>        402.6089172363281,<br>        496.8799133300781,<br>        341.49383544921875,<br>        597.4930419921875,<br>        504.7567138671875,<br>        585.8673706054688<br>      ],<br>      "topLeftX": 215,<br>      "topLeftY": 181,<br>      "faceWidth": 436,<br>      "faceHeight": 561<br>    },<br>    "face_score": 1.0,<br>    "expression": "smile",<br>    "expression_score": 0.932392954826355,<br>    "age": 25,<br>    "gender": "female", <br>    "attribute": "normal",<br>    "image_width": 900,<br>    "image_height": 1350,<br>    "engine_version": 390<br>  },<br>  {<br>    "face_id": "IQA498UJYO",<br>    "face_name": "A",<br>    "box": {<br>      "landmark": [ <br>        315.33056640625,<br>        395.97271728515625,<br>        509.1438293457031,<br>        382.5447692871094,<br>        402.6089172363281,<br>        496.8799133300781,<br>        341.49383544921875,<br>        597.4930419921875,<br>        504.7567138671875,<br>        585.8673706054688<br>      ],<br>      "topLeftX": 215,<br>      "topLeftY": 181,<br>      "faceWidth": 436,<br>      "faceHeight": 561<br>    },<br>    "face_score": 1.0,<br>    "expression": "smile",<br>    "expression_score": 0.932392954826355, <br>    "age": 25,<br>    "gender": "female", <br>    "attribute": "normal",<br>    "image_width": 900, <br>    "image_height": 1350, <br>    "engine_version": 390 <br>  }<br>] |

<br>

여기까지 A, B, C D 에 대한 모든 데이터를 등록하면, API 를 사용할 준비가 완료되었습니다. 이제 Recognize API 를 사용하여 실제 얼굴인식을 사용해볼 수 있습니다.

<br>

> ## 얼굴인식 기능의 사용

<br>

얼굴인식 API는 사용자가 전달한 이미지를 분석해서 해당 이미지에서 얼굴정보와 특징을 추출하고, 기존에 구축한 DB에서 가장 유사한 얼굴 데이터를 찾아 사용자에게 식별 정보를 반환하는 방식으로 동작합니다. 위의 내용을 모두 진행 했으면 Group/Subject/Face 데이터를 사전에 구축했기 때문에, 이제 얼굴인식 API를 사용하여 식별을 요청할 수 있습니다. 실제 API에서 요청을 진행하면 다음과 같은 방식으로 요청을 처리하게 됩니다([Fig 2.](#fig_2)).

<br>

<p />
<p /><a name="fig_2">Fig. 2</a> Face Recognition Processing
<p /><img src="figures/fig2.recognition-processing.jpg">

<br>


API 의 요청 명령과 결과는 다음과 같이 확인할 수 있습니다.

|Category|Contents|
|---|---|
|Request| curl --location <br> --request POST 'https://apis.openapi.sk.com/nugufacecan/v1/recognize' <br> --header 'appKey: l7xx4bfa60c6bc8945819a114c5e34cc930c' <br> --header 'app-id: GZ0E4G4YI1' <br> --header 'group-id: VOFLIDEYD6' <br> --form 'image=@"A_Face_3.jpg"' |
|Response| 200 OK <pre>{<br>  "subject_id": "8YLHWXT0K0",<br>  "subject_name": "A",<br>  "distance": 0.19108226147411367,<br>  "face_box": {<br>    "topLeftX": 148,<br>    "topLeftY": 84,<br>    "faceWidth": 205,<br>    "faceHeight": 281,<br>    "landmark": [<br>      222.57568359375,<br>      197.8626708984375,<br>      316.3310546875,<br>      191.84608459472656,<br>      285.20001220703125,<br>      246.61094665527344,<br>      235.28875732421875,<br>      297.4136657714844,<br>      311.33209228515625,<br>      292.1959533691406<br>    ]<br>  },<br>  "face_id": "AIF2SGCB9R",<br>  "face_score": 1.0,<br>  "expression": "smile",<br>  "expression_score": 0.67128611,<br>  "expression_raw": {<br>    "neutral": 0.32691383,<br>    "smile": 0.67128611,<br>    "sad": 0.00118194,<br>    "surprised": 0.00312898,<br>    "fear": 0.00042589,<br>    "angry": 0.0013624,<br>    "etc": 0.00249748<br>  },<br>  "age": 27,<br>  "gender": "female",<br>  "attribute": "normal",<br>  "transaction_id": "M00003858C4Q"<br>} </pre>

여기서 사용자의 식별에 사용하는 용도라면, subject_id/name 이 가장 중요한 요소가 될 것이고, 그 외에 다른 정보들도 활용이 가능합니다. 예를 들면, face_score 가 1.0 이지만, 이보다 적은 수치가 나오면, 이는 현재 촬영한 영상 내에서 얼굴의 형태가 신뢰하기 어렵다는 의미이기 때문에, 재촬영을 요구할 수 있습니다. 또한, distance 값이 너무 크게 나온다면, 그 결과의 신뢰도가 떨어지는 의미 이기 때문에, 재촬영을 요구하거나 하는 등의 처리가 가능합니다.

그리고 부가적으로 한 사진에 여러 명의 얼굴이 있고, 여러 명을 동시에 찾는 것이 필요한 경우에는 header에 multi: 1 값을 추가하면, 한 번에 여러 개의 얼굴 결과를 동시에 출력하게 됩니다.


여기까지 사용자 DB를 만드는 과정과 얼굴인식을 수행하는 과정에 사용하는 API 와 개략적인 구조를 살펴보았습니다. curl 명령에 있는 POST/header/form 등은 어느 언어를 사용하든 동일한 인터페이스를 사용하기 때문에 이를 참조하여 진행하면 됩니다. 실제 서비스는 영상을 촬영하는 방식을 결정/구현해야 하고, 자료구조를 어떻게 결정하는 것이 활용에 편의성이 있을지 많은 검토가 필요합니다. 

중간에 문의 사항이나 구현 상의 어려움이 있다면 [SK OpenAPI 사용자 문의](https://openapi.sk.com) 에 연락주시기 바랍니다.

감사합니다. 