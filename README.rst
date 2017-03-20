=====================
I'mport; REST Client
=====================

.. image:: https://travis-ci.org/iamport/iamport-rest-client-python.svg?branch=master
    :target: https://travis-ci.org/iamport/iamport-rest-client-python

.. image:: https://codecov.io/gh/iamport/iamport-rest-client-python/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/iamport/iamport-rest-client-python


Python 사용자를 위한 아임포트 REST API 연동 모듈입니다.

* 이용 중 발생한 문제에 대해 책임지지 않습니다.
* lexifdev님의 도움을 받아 작성되었습니다(`lexifdev's iamport 모듈 <https://github.com/lexifdev/iamport>`_)
* 최초 작성은 `핑크퐁 북스토어 <https://store.pinkfong.com>`_ 에서 쓰기 위해 만들었습니다.

설치
=======

.. code-block:: shell

    pip install iamport-rest-client


기능
======
1. 결제 정보 찾기
2. 가격 확인
3. 취소
4. 비 인증 결제


사용법
=======

준비
------

사용하기 위해 객체를 만듭니다.

.. code-block:: python

    from iamport import Iamport

    # 테스트 용
    iamport = Iamport(imp_key='{테스트용 키}', imp_secret='{테스트 시크릿}')
    # 테스트용 키와 시크릿은 tests/conftest.py 파일에 DEFAULT_TEST_IMP_KEY, DEFAULT_TEST_IMP_SECRET를 참고하세요.

    # 실제 상점 정보
    iamport = Iamport(imp_key='{발급받은 키}', imp_secret='{발급받은 시크릿}')



찾기
------

결제를 진행한 상품 아이디나, 전달받은 IMP 아이디를 이용해 결제 정보를 찾습니다.

.. code-block:: python

    # 상품 아이디로 조회
    response = iamport.find(merchant_uid='{상품 아이디}')

    # I'mport; 아이디로 조회
    response = iamport.find(imp_uid='{IMP UID}')


가격 확인
----------

실제 제품 가격과 결제된 가격이 같은지 확인합니다.

.. code-block:: python

    # 상품 아이디로 확인
    iamport.is_paid(product_price, merchant_uid='{상품 아이디}')

    # I'mport; 아이디로 확인
    iamport.is_paid(product_price, imp_uid='{IMP UID}')

    # 이미 찾은 response 재활용하여 확인
    iamport.is_paid(product_price, response=response)


취소
------

결제를 취소합니다.

.. code-block:: python

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


비인증 결제
-------------

1회성 비인증 결제를 진행합니다.

.. code-block:: python

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


저장된 빌링키로 재결제합니다.

.. code-block:: python

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


결제 사전 검증
-------------

결제될 내역에 대한 사전정보를 등록합니다

.. code-block:: python

    # 테스트용 값
    amount = 12000
    mid = 'merchant_test'
    try:
        response = iamport.prepare(amount=amount, merchant_uid=mid)
    except Iamport.ResponseError as e:
        # 응답 에러 처리
        pass


등록된 사전정보를 확인합니다

.. code-block:: python

    # 테스트용 값
    amount = 12000
    mid = 'merchant_test'
    try:
        result = iamport.prepare_validate(merchant_uid=mid, amount=amount)
    except Iamport.ResponseError as e:
        # 응답 에러 처리
        pass


개발환경 및 테스트 설정
==========================
macOS 기준 pyenv 설치 권장

::

    # pyenv 준비
    brew install pyenv
    pyenv install 2.7.12 3.4.5 3.5.2 pypy-5.6.0
    pyenv local 2.7.12 3.4.5 3.5.2 pypy-5.6.0
    # tox
    pip install tox-pyenv detox
    detox

    # 커버리지 확인
    pip install pytest-cov
    python -m pytest tests/ --cov=./

기여
======
- 파이썬 3 지원, 테스트: `dahlia <https://github.com/dahlia>`_ `#4 <https://github.com/iamport/iamport-rest-client-python/pull/4>`_
- 비인증 결제(onetime) 지원: `psy2848048 <https://github.com/psy2848048>`_ `#8 <https://github.com/iamport/iamport-rest-client-python/pull/8>`_
- 부분 취소 지원:  `pcompassion <https://github.com/pcompassion>`_ `#10 <https://github.com/iamport/iamport-rest-client-python/pull/10>`_
- 재결제 지원: `Leop0ld <https://github.com/Leop0ld>`_ `#13 <https://github.com/iamport/iamport-rest-client-python/pull/13>`_
- 결제사전검증 지원: `Bumsoo Kim <https://github.com/bskim45>`_ `#17 <https://github.com/iamport/iamport-rest-client-python/pull/17>`_

할 일
======
- 결제 목록 읽기
- 비인증 결제 세부 기능 지원
- 문서화
- 기타 등등
