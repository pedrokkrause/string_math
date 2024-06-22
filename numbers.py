from collections import defaultdict
from itertools import zip_longest

### Numbers are only allowed here in the beginning
BASE = 10
LAST_DIGIT = str(BASE - 1)

sumdict = defaultdict(lambda: {})
muldict = defaultdict(lambda: {})
gtdict = defaultdict(lambda: {})
ltdict = defaultdict(lambda: {})
invdict = {}

for i in range(BASE):
    for j in range(BASE):
        sumdict[str(i)][str(j)] = (str((i+j) % BASE), str((i+j)//BASE))
        muldict[str(i)][str(j)] = (str((i*j) % BASE), str((i*j)//BASE))
        gtdict[str(i)][str(j)] = (i>j)
        ltdict[str(i)][str(j)] = (i<j)
    invdict[str(i)] = str(int(LAST_DIGIT)-i)
###

GREATER = 'g'
LESS = 'l'
EQUAL = 'e'

class sint:

    def __init__(self, number, sign=None):
        if isinstance(number, sint):
            self.number = number.number
            if sign is None:
                self.sign = number.sign
            else:
                self.sign = sign
        elif isinstance(number, (str,int)):
            number = str(number)
            self.sign = (True if number[0] == '-' else False)
            if self.sign:
                self.number = list(number[1:])[::-1]
            else:
                self.number = list(number)[::-1]
        elif hasattr(number, '__iter__'):
            if sign is None:
                self.sign = False
            else:
                self.sign = sign
            self.number = list(number)
        else:
            raise ValueError

        self.length = None

    def __eq__(self, other):
        if isinstance(other, sint):
            return self.number == other.number and self.sign == other.sign
        return False

    def compare(self, other):
        if not self.sign and other.sign:
            return GREATER
        elif self.sign and not other.sign:
            return LESS
        if self.number == other.number:
            return EQUAL

        result = EQUAL
        decided = False
        for x,y in zip_longest(reversed(self.number), reversed(other.number)):
            if x is None:
                return LESS
            elif y is None:
                return GREATER
            if not decided:
                if gtdict[x][y]:
                    result = GREATER
                    decided = True
                elif ltdict[x][y]:
                    result = LESS
                    decided = True
        return result

    def __lt__(self, other):
        comparison = self.compare(other)
        if comparison == LESS:
            return True
        return False

    def __gt__(self, other):
        comparison = self.compare(other)
        if comparison == GREATER:
            return True
        return False

    def __le__(self, other):
        comparison = self.compare(other)
        if comparison == LESS or comparison == EQUAL:
            return True
        return False

    def __ge__(self, other):
        comparison = self.compare(other)
        if comparison == GREATER or comparison == EQUAL:
            return True
        return False

    def __neg__(self):
        return sint(self.number, sign=(not self.sign))

    def __add__(self, other):
        other = sint(other)
        if self.sign and not other.sign:
            return other-(-self)
        elif self.sign and other.sign:
            return -((-self)+(-other))
        elif not self.sign and other.sign:
            return self-(-other)
        result = []
        carry = '0'
        for x,y in zip_longest(self.number, other.number, fillvalue='0'):
            semi_digit, new_carry1 = sumdict[x][y]
            digit, new_carry2 = sumdict[semi_digit][carry]
            carry, _ = sumdict[new_carry1][new_carry2]
            result.append(digit)
        if carry != '0':
            result.append(carry)
        return sint(number=result)

    def __radd__(self, other):
        other = sint(other)
        return other.__add__(self)

    def inverse(self):
        result = [invdict[x] for x in self.number]
        return sint(result, sign=self.sign)

    def __sub__(self, other):
        other = sint(other)
        if self.sign and other.sign:
            return (-other) - (-self)
        elif self.sign and not other.sign:
            return -(other-self)
        elif not self.sign and other.sign:
            return self+(-other)

        comparison = self.compare(other)
        if comparison == LESS:
            result = (other.inverse() + self).inverse()
            result.sign = True
        else:
            result = (self.inverse()+other).inverse()
        result.clear()
        return result

    def __rsub__(self, other):
        other = sint(other)
        return other.__sub__(self)

    def __mul__(self, other):
        other = sint(other)
        sign = not (self.sign == other.sign)
        result = sint('0')
        carry = '0'
        zeros = []
        for x in self.number:
            adder = zeros.copy()
            for y in other.number:
                semi_digit, new_carry1 = muldict[x][y]
                digit, new_carry2 = sumdict[semi_digit][carry]
                carry, _ = sumdict[new_carry1][new_carry2]
                adder.append(digit)
            if carry != '0':
                adder.append(carry)
                carry = '0'
            zeros.append('0')
            result += sint(adder)
        return sint(result, sign=sign)

    def __rmul__(self, other):
        other = sint(other)
        return other.__mul__(self)

    def __divmod__(self, other):
        other = sint(other)
        if other.number == ['0']:
            raise ZeroDivisionError
        sign = not (self.sign == other.sign)
        if self < other:
            return sint('0'), sint(self)

        result = []

        multiples = {'0': sint('0')}
        i = '0'
        while i != '9':
            i,_ = sumdict[i]['1']
            multiples[i] = other * sint(i)
        self_digits = self.number.copy()
        current_digits = []
        while True:
            while True:
                if self_digits:
                    digit = self_digits.pop()
                    if digit != '0' or current_digits:
                        current_digits.insert(0,digit)
                    current_number = sint(current_digits)
                    if current_number >= other:
                        break
                    else:
                        result.append('0')
                else:
                    div = sint(reversed(result), sign=sign)
                    div.clear()
                    return div, sint(current_digits)
            for i in reversed(multiples):
                if multiples[i] <= current_number:
                    result.append(i)
                    current_number -= multiples[i]
                    if current_number == sint('0'):
                        current_digits.clear()
                    else:
                        current_digits = current_number.number.copy()
                    break

    def __rdivmod__(self, other):
        other = sint(other)
        return other.__divmod__(self)

    def __floordiv__(self, other):
        div,mod = divmod(self,other)
        return div

    def __rfloordiv__(self, other):
        other = sint(other)
        return other.__floordiv__(self)

    def __mod__(self, other):
        div,mod = divmod(self,other)
        return mod

    def __rmod__(self, other):
        other = sint(other)
        return other.__mod__(self)

    def clear(self):
        while self.number and self.number[-1] == '0':
            self.number.pop()
        if not self.number:
            self.number.append('0')

    def __len__(self):
        if self.length is None:
            i = sint('0')
            for x in self.number:
                i = i + sint('1')
            self.length = i
            return i
        else:
            return self.length

    def __repr__(self):
        return ('-' if self.sign else '')+''.join(self.number[::-1])
