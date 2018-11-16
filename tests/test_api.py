import pytest
from itsdangerous import json

import app
import api


with app.app.app_context() as c:
    app.app.config.from_pyfile('config/test.py')


class TestGetFibonacci:
    @pytest.mark.parametrize('ref1,ref2,count,expect', (
        (None, None, 15, [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377]),
        (1, 2, 15, [3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584])
    ))
    def test_get_fibonacci(self, ref1, ref2, count, expect):
        res = list(api.get_fibonacci(ref1, ref2, count))

        assert res == expect

    def test_get_fibonacci_error_on_ref1_more_than_ref2(self):
        with pytest.raises(ValueError):
            res = list(api.get_fibonacci(2, 1, 10))


class TestApiFibonachi:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.base_url = '/fibonachi'
        self.app = app.app.test_client()

    @pytest.mark.parametrize('f,t,expect', (
        (5, 10, [5, 8, 13, 21, 34]),
        (0, 10, [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]),
        (20, 30, [6765, 10946, 17711, 28657, 46368, 75025, 121393, 196418, 317811, 514229])
    ))
    def test_get_slice(self, f, t, expect):
        with self.app as c:
            res = c.get('{}?from={}&to={}'.format(self.base_url, f, t))
        print(res)
        assert json.loads(res.data) == expect

    @pytest.mark.parametrize('qs', ('?from=5', '?to=5', ''))
    def test_http400_on_missing_params(self, qs):
        with self.app as c:
            res = c.get('{}{}'.format(self.base_url, qs))

        assert res.status_code == 400

    def test_http400_if_to_more_than_from(self):
        with self.app as c:
            res = c.get('{}?from=5&to=0'.format(self.base_url))

        assert res.status_code == 400

    @pytest.mark.parametrize('f,t', (
        (-4, 5),
        (9, -12),
        (-38, -2)
    ))
    def test_http400_on_negative_params(self, f, t):
        with self.app as c:
            res = c.get('{}?from={}&to={}'.format(self.base_url, f, t))

        assert res.status_code == 400
