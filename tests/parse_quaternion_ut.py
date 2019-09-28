import pytest

from parse_quaternion import parse_quaternion
import numpy as np

@pytest.mark.parametrize("qs,expected", [
    ('1', [1, 0, 0, 0]),
    ('+1*i', [0, 1, 0, 0]),
    ('1-1i+5.3j-3.1k', [1, -1, 5.3, -3.1]),
    ('1 - 1*i + 5.3*j - 3.1*k', [1, -1, 5.3, -3.1]),
    ('-1i + 2*i', [0, 1, 0, 0]),
    ('-0.5', [-0.5, 0, 0, 0]),
    ('1 + 2 - 3.4 + 5.6 * i - 2.1 * j + 1.3 * j', [-0.4, 5.6, -0.8, 0]),
])
def test_parse(qs, expected):
    assert np.allclose(np.array(parse_quaternion(qs)), np.array(expected))
