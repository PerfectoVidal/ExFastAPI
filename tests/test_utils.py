import pytest

from utils import the_list_contain_the_same_elements


@pytest.mark.parametrize('list1,list2,result', [
    ([{1: 2, 2: 3}, {1: 3, 2: 4}], [{1: 2, 2: 3}, {1: 3, 2: 4}], True),
    ([{1: 2, 2: 3}, {1: 3, 2: 4}], [{1: 3, 2: 4}, {1: 2, 2: 3}], True),
    ([{1: 2, 2: 3}, {1: 3, 2: 4}, {1: 3, 2: 4}], [{1: 3, 2: 4}, {1: 2, 2: 3}], False),
    ([{1: 2, 2: 3}], [{1: 3, 2: 4}, {1: 2, 2: 3}], False),
    ([{1: 2, 2: 4}, {1: 3, 2: 4}], [{1: 3, 2: 4}, {1: 2, 2: 3}], False),
    ([{1: 3, 2: 3}, {1: 3, 2: 3}], [{1: 3, 2: 3}, {1: 2, 2: 4}], False),
])
def test_is_the_same_list(list1, list2, result):
    assert the_list_contain_the_same_elements(list1, list2) is result
