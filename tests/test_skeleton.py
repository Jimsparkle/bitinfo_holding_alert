# -*- coding: utf-8 -*-

import pytest

from doge_holding_alert.skeleton import fib

__author__ = "Jimsparkle"
__copyright__ = "Jimsparkle"
__license__ = "mit"


def test_fib():
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(7) == 13
    with pytest.raises(AssertionError):
        fib(-10)
