from pyparsing import Word, alphas, nums, Optional

def parse_quaternion(s):
    s.replace(' ', '')
    int_num = Word(nums)
    real_num = int_num + Optional('.' + int_num)
    pm = Word("+-", max=1)
    signed_real_num = Optional(pm + real_num)('num')

    a = Optional(Optional(pm) + real_num)('a')
    b = Optional(signed_real_num + '*i')('b')
    c = Optional(signed_real_num + '*j')('c')
    d = Optional(signed_real_num + '*k')('d')

    expr = (a + b + c + d).parseString(s)
    res = [
        expr.get('a', ['0']),
        expr.get('b', ['0', '*i'])[:-1],
        expr.get('c', ['0', '*j'])[:-1],
        expr.get('d', ['0', '*k'])[:-1]
    ]
    return [
        float(''.join(x)) for x in res
    ]

def main():
    print(parse_quaternion('-1+5.4*i+3.0*j'))

if __name__ == "__main__":
    main()
