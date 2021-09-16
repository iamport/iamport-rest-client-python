I'mport; REST Client Python
---------------------------

[![Python Versions](https://img.shields.io/pypi/pyversions/iamport-rest-client)](https://pypi.org/project/iamport-rest-client/)
[![PyPI Release (latest by date)](https://img.shields.io/pypi/v/iamport-rest-client?color=blue)](https://pypi.org/project/iamport-rest-client/)
[![GitHub Workflow Status (Build)](https://img.shields.io/github/workflow/status/iamport/iamport-rest-client-python/Build%20Status)](https://github.com/iamport/iamport-rest-client-python/actions)
[![GitHub LICENSE](https://img.shields.io/github/license/iamport/iamport-rest-client-python)](https://github.com/iamport/iamport-rest-client-python/blob/master/LICENSE)
[![Lines of Code](https://img.shields.io/tokei/lines/github/iamport/iamport-rest-client-python)](https://github.com/iamport/iamport-rest-client-python/tree/master/iamport)


설명
---
> Python 개발자를 위한 [아임포트 REST API](https://api.iamport.kr/) 연동 패키지입니다.

주의 사항
-------
* 이용 중 발생한 문제에 대해 책임지지 않습니다.
* `lexifdev`님의 도움을 받아 작성되었습니다[`lexifdev's iamport 모듈](https://github.com/lexifdev/iamport)
* 최초 작성은 `[핑크퐁 북스토어](https://store.pinkfong.com)`에서 쓰기 위해 만들었습니다.

주요 기능
---
1. 결제 정보 찾기
2. 가격 확인
3. 취소
4. 비 인증 결제
5. 정기 예약 결제
6. 본인인증결과 조회 및 삭제

설치
---
[추천 사항] 아나콘다 환경에서 작업하신다면, 우선 아래의 절차를 진행해주세요.
```bash
# 아임포트 패키지를 위한 새로운 파이썬 가상환경을 생성해주세요. 이 때, 파이썬 버전은 최소 3.6 이상을 선택해주세요.
conda create --name iamport python=3.6

# 위에서 파이썬 가상환경이 정상적으로 설치되었다면, 해당 가상환경을 활성화해주세요.
conda activate pymodi
```

다음 커맨드를 실행하여 최신버전의 아임포트 패키지를 설치해주세요.
```bash
python -m pip install iamport-rest-client --upgrade
```

현재 개발중인 버전의 아임포트 패키지를 아래의 커맨드로 설치하실 수 있습니다.
```bash
python -m pip install git+https://github.com/iamport/iamport-rest-client-python.git@develop --upgrade
```

혹은, 특정 버전의 아임포트 패키지를 다음과 같이 설치하실 수 있습니다.
```bash
python -m pip install git+https://github.com/iamport/iamport-rest-client-python.git@v1.0.0 --upgrade
```

사용 준비
-------
```python
from iamport import Iamport

# 아임포트 객체를 테스트용 키와 시크릿을 사용하여 생성합니다 (테스트시 지출된 금액은 매일 밤 환불됩니다).
iamport = Iamport(
    imp_key='imp_apikey', 
    imp_secret=(
        'ekKoeW8RyKuT0zgaZsUtXXTLQ4AhPFW3ZGseDA6b'
        'kA5lamv9OqDMnxyeB9wqOsuO9W3Mx9YSJ4dTqJ3f'
    )
)

# 아임포트 객체를 각자 발급받으신 실제 키와 시크릿을 사용하여 생성합니다.
iamport = Iamport(imp_key='{발급받은 키}', imp_secret='{발급받은 시크릿}')
```

사용 예제
-------

- 찾기  
결제를 진행한 상품 아이디나, 전달받은 IMP 아이디를 이용해 결제 정보를 찾습니다.

```python
# 상품 아이디로 조회
response = iamport.find(merchant_uid='{상품 아이디}')

# I'mport; 아이디로 조회
response = iamport.find(imp_uid='{IMP UID}')
```

실제 제품 가격과 결제된 가격이 같은지 확인합니다.

```python
# 상품 아이디로 확인
iamport.is_paid(product_price, merchant_uid='{상품 아이디}')

# I'mport; 아이디로 확인
iamport.is_paid(product_price, imp_uid='{IMP UID}')

# 이미 찾은 response 재활용하여 확인
iamport.is_paid(product_price, response=response)
```


결제를 취소합니다.

```python
# 상품 아이디로 취소
response = iamport.cancel(u'취소하는 이유', merchant_uid='{상품 아이디}')

# I'mport; 아이디로 취소
response = iamport.cancel(u'취소하는 이유', imp_uid='{IMP UID}')

# 취소시 오류 예외처리(이미 취소된 결제는 에러가 발생함)
try:
    response = iamport.cancel(u'취소하는 이유', imp_uid='{IMP UID}')
except Iamport.ResponseError as e:
    print e.code
    print e.message  # 에러난 이유를 알 수 있음
except Iamport.HttpError as http_error:
    print http_error.code
    print http_error.reason # HTTP not 200 에러난 이유를 알 수 있음
```

1회성 비인증 결제를 진행합니다.

```python
# 테스트용 값
payload = {
    'merchant_uid': '00000000',
    'amount': 5000,
    'card_number': '4092-0230-1234-1234',
    'expiry': '2019-03',
    'birth': '500203',
    'pwd_2digit': '19'
}
try:
    response = iamport.pay_onetime(**payload)
except KeyError:
    # 필수 값이 없을때 에러 처리
    pass
except Iamport.ResponseError as e:
    # 응답 에러 처리
    pass
except Iamport.HttpError as http_error:
    # HTTP not 200 응답 에러 처리
    pass
```

저장된 빌링키로 재결제합니다.

```python
# 테스트용 값
payload = {
    'customer_uid': '{고객 아이디}',
    'merchant_uid': '00000000',
    'amount': 5000,
}
try:
    response = iamport.pay_again(**payload)
except KeyError:
    # 필수 값이 없을때 에러 처리
    pass
except Iamport.ResponseError as e:
    # 응답 에러 처리
    pass
except Iamport.HttpError as http_error:
    # HTTP not 200 응답 에러 처리
    pass
```

정기 결제를 예약합니다.

```python
# 테스트용 값
payload = {
    'customer_uid': '{고객 아이디}',
    'schedules': [
        {
            'merchant_uid': 'test_merchant_01',
            # UNIX timestamp
        'schedule_at': 1478150985,
        'amount': 1004
        },
        {
            'merhcant_uid': 'test_merchant_02',
        # UNIX timestamp
        'schedule_at': 1478150985,
        'amount': 5000,
        'name': '{주문명}',
        'buyer_name': '{주문자명}',
        'buyer_email': '{주문자 이메일}',
        'buyer_tel': '{주문자 전화번호}',
        'buyer_addr': '{주문자 주소}',
        'buyer_postcode': '{주문자 우편번호}',
        },
    ]
}
try:
    reponse = iamport.pay_schedule(**payload)
except KeyError:
    # 필수 값이 없을때 에러 처리
    pass
except Iamport.ResponseError as e:
    # 응답 에러 처리
    pass
except Iamport.HttpError as http_error:
    # HTTP not 200 응답 에러 처리
    pass
```

정기 결제 예약을 취소합니다.

```python
# 테스트용 값 (merchant_uid 가 누락되면 customer_uid 에 대한 결제예약정보 일괄취소)
payload = {
    'customer_uid': '{고객 아이디}',
    'merchant_uid': 'test_merchant_01',
}
try:
    response = iamport.pay_unschedule(**payload)
except KeyError:
    # 필수 값이 없을때 에러 처리
    pass
except Iamport.ResponseError as e:
    # 응답 에러 처리
    pass
except Iamport.HttpError as http_error:
    # HTTP not 200 응답 에러 처리
    pass
```

결제될 내역에 대한 사전정보를 등록합니다

```python
# 테스트용 값
amount = 12000
mid = 'merchant_test'
try:
    response = iamport.prepare(amount=amount, merchant_uid=mid)
except Iamport.ResponseError as e:
    # 응답 에러 처리
    pass
except Iamport.HttpError as http_error:
    # HTTP not 200 응답 에러 처리
    pass
```

등록된 사전정보를 확인합니다.

```python
# 테스트용 값
amount = 12000
mid = 'merchant_test'
try:
    result = iamport.prepare_validate(merchant_uid=mid, amount=amount)
except Iamport.ResponseError as e:
    # 응답 에러 처리
    pass
except Iamport.HttpError as http_error:
    # HTTP not 200 응답 에러 처리
    pass
```

본인인증결과를 조회합니다.

```python
try:
    response = iamport.find_certification(imp_uid='{IMP UID}')
except Iamport.ResponseError as e:
    # 응답 에러 처리
    pass
except Iamport.HttpError as http_error:
    # HTTP not 200 응답 에러 처리
    pass
```

본인인증결과를 아임포트에서 삭제합니다.

```python
try:
    response = iamport.cancel_certification(imp_uid='{IMP UID}')
except Iamport.ResponseError as e:
    # 응답 에러 처리
    pass
except Iamport.HttpError as http_error:
    # HTTP not 200 응답 에러 처리
    pass      
```

기여하기
------
[iamport-rest-client-python 프로젝트 보드](https://github.com/iamport/iamport-rest-client-python/projects/1)의 `To do` 탭을 참고해주세요.