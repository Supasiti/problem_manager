from tests.test_problem_editor import MockRepository
from datetime import date

if __name__ == '__main__':
    
    numbers = [1, 1,1,1,2,3,3,3,4,4,4,5]

    uniques = list(dict.fromkeys(numbers).keys())
    print(uniques)