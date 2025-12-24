from typing import List, Tuple

def make_list(gap: List[int]) -> List[int]:
    return list(range(gap[0], gap[1] + 1))


def guess_number(type_of_alg: int, number: int, gap_list: List[int]) -> Tuple[int, int]:
    count_of_compare = 1

    if type_of_alg == 1:
        index = 0
        while index < len(gap_list) and gap_list[index] != number:
            index += 1
            count_of_compare += 1
        if index == len(gap_list):
            raise ValueError
        return gap_list[index], count_of_compare

    elif type_of_alg == 2:
        start = 0
        end = len(gap_list) - 1
        while start <= end:
            middle = (start + end) // 2
            if gap_list[middle] == number:
                return gap_list[middle], count_of_compare
            elif gap_list[middle] < number:
                start = middle + 1
            else:
                end = middle - 1
            count_of_compare += 1
        raise ValueError

    else:
        raise ValueError


def main() -> Tuple[int, int]:
    number = 73
    gap = [1, 100]
    type_of_alg = 2

    result, n_of_attempts = guess_number(type_of_alg, number, make_list(gap))
    return result, n_of_attempts


if __name__ == '__main__':
    print(main())