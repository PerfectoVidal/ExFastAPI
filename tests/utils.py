def the_list_contain_the_same_elements(list1: list, list2: list) -> bool:
    if len(list1) != len(list2):
        return False
    for el in list1:
        if el not in list2:
            return False
    for el in list2:
        if el not in list1:
            return False
    return True
