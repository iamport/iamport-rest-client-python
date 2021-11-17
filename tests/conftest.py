from pytest import fixture

from iamport import Iamport

DEFAULT_TEST_IMP_KEY = 'imp_apikey'
DEFAULT_TEST_IMP_SECRET = (
    'ekKoeW8RyKuT0zgaZsUtXXTLQ4AhPFW3ZGseDA6b'
    'kA5lamv9OqDMnxyeB9wqOsuO9W3Mx9YSJ4dTqJ3f'
)


def pytest_addoption(parser):
    parser.addoption(
        '--imp-key',
        default=DEFAULT_TEST_IMP_KEY,
        help='iamport client key for testing [default: %(default)s]'
    )
    parser.addoption(
        '--imp-secret',
        default=DEFAULT_TEST_IMP_SECRET,
        help='iamport secret key for testing [default: %(default)s]'
    )


@fixture
def iamport(request):
    imp_key = request.config.getoption('--imp-key')
    imp_secret = request.config.getoption('--imp-secret')
    return Iamport(imp_key=imp_key, imp_secret=imp_secret)
