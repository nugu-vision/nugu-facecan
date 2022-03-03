# Security

NUGU facecan API는 사용자의 이미지를 암호화하여 API 를 호출하는 기능을 제공합니다. 기본적으로 이미지 암호화를 하지 않아도 호출 가능하지만, 보다 확실한 이미지 데이터의 보안을 위해 AES-128 방식으로 암호화한 파일을 이용해 API를 호출하는 것도 지원합니다. 아래 내용은 이미지 암호화 시 플로우와 Python 예제 코드를 설명합니다.

<br>

### Flow

> 1. SKOpenAPI 서버로부터 RSA Public key를 얻어옵니다.(/api/v1/key)
> 2. 클라이언트에서는 AES-128 암호키를 생성하고 얼굴 인식 API에 사용할 이미지 파일을 해당 키로 암호화 합니다.
> 3. 클라이언트에서는 2번 과정에서 생성된 AES-128 암호키를 1번 과정에서 얻어온 RSA Public key로 암호화 합니다.
> 4. 인식 요청시 3번 과정의 RSA Public key로 암호화된 AES-128 암호키 값과 2번 과정에서 생성된 암호화된 이미지 파일로 얼굴 인식 API를 호출합니다.


<br>

### Sample Code

샘플 코드는 다음의 코드를 참조하시면 됩니다. ([aes_encode.py](codes/aes_encode.py)) 해당 코드는 전체 Flow의 1,2,3번 과정의 구현 내용을 포함하고 있습니다. 암호화된 API 호출은 얼굴 등록/얼굴 인식/얼굴 검출 API에 적용 가능하며 Header에 암호화 키 값, Body에 암호화된 이미지를 전달하는 식으로 호출하면 됩니다. API 호출에 대한 자세한 내용은 [NUGU facecan API Reference](https://openapi.sk.com) 을 참고하시기 바랍니다.

