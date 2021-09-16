I'mport; REST Client
--------------------

<div align="center">

[![Python Versions](https://img.shields.io/pypi/pyversions/iamport-rest-client)](https://pypi.org/project/iamport-rest-client/)
[![PyPI Release (latest by date)](https://img.shields.io/pypi/v/iamport-rest-client?color=blue)](https://pypi.org/project/iamport-rest-client/)
[![GitHub Workflow Status (Build)](https://img.shields.io/github/workflow/status/iamport/iamport-rest-client-python/Build%20Status)](https://github.com/iamport/iamport-rest-client-python/actions)
[![GitHub LICENSE](https://img.shields.io/github/license/iamport/iamport-rest-client-python)](https://github.com/iamport/iamport-rest-client-python/blob/master/LICENSE)
[![Lines of Code](https://img.shields.io/tokei/lines/github/iamport/iamport-rest-client-python)](https://github.com/iamport/iamport-rest-client-python/tree/master/iamport)

</div>

설명
---
> Python 개발자를 위한 [아임포트 REST API](https://api.iamport.kr/) 연동 패키지입니다.

기능
---
1. 결제 정보 찾기
2. 가격 확인
3. 취소
4. 비 인증 결제
5. 정기 예약 결제
6. 본인인증결과 조회 및 삭제

설치
---
> 아임포트를 설치하실 때 아나콘다를 이용한 아임포트 파이썬 가상환경 구성을 추천합니다.
[선택 사항] 아나콘다 환경에서 작업하신다면, 우선 아래의 절차를 진행해주세요.
```bash
# 아임포트 패키지를 위한 새로운 파이썬 가상환경을 생성해주세요. 이 때, 파이썬 버전은 최소 3.6 이상을 선택해주세요.
conda create --name iamport python=3.6

# 위에서 파이썬 가상환경이 정상적으로 설치되었다면, 해당 가상환경을 활성화해주세요.
conda activate pymodi
```

아래의 커맨드를 실행하여 최신버전의 아임포트를 설치해주세요.
```bash
python -m pip install iamport-rest-client --upgrade
```

준비
---
아임포트 객체를 생성합니다.
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

기여하기
------
[iamport-rest-client-python 프로젝트 보드](https://github.com/iamport/iamport-rest-client-python/projects/1)의 `To do` 탭을 참고해주세요.