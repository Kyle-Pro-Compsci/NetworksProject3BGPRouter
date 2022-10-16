import pytest

#router = __import__('3700router')
from router_copy import Router

def test_mask():
    test_router = Router(14, ['56399-192.168.0.2-cust', '59522-172.168.0.2-cust'])
    assert(test_router.mask('5.168.0.0', '255.0.0.0')) == '5.0.0.0'
