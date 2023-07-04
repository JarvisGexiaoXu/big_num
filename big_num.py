import numpy as np

class big_num(object):
    np.set_printoptions(suppress=True)

    def __init__(self, num, n, sign) -> None:
        self.num = num
        self.n = n
        self.sign = sign
    
    # Functions for conversions

    # convert number strings into numpy array, the form of big number
    def write_num_into_vector(num_str, n=0):
        if num_str[0] == '-': 
            sign = '-'
            num_str = num_str[1:len(num_str)]
        else: sign = '+'
        if n == 0 or n == 1:
            res = np.array([int(num) for num in num_str])
        else:
            l = len(num_str)
            k = l % n
            if k!= 0:res = [int(str(num_str[0:k]))]
            else: res = []
            for i in range(k, len(num_str),n):
                res.append(int(num_str[i:i+n]))
            res = np.array(res)
        return big_num(res, n, sign)
    
    def write_num_into_str(num):
        if num.sign == '-': res = '-'
        else: res = '+'
        n = num.n
        v = num.num
        v = v.astype(int)
        for i in range(len(v)):
            if i > 0:
                temp = str(v[i]) 
                if len(temp) == n:
                    res += temp
                else:
                    res += temp.zfill(n) 
            else: res += str(v[0])
        return res
    
    # Functions for comparisons
    
    def equal(num_a, num_b):
        if num_a.sign == num_b.sign and np.array_equal(num_a.num, num_b.num):
            return True
        if np.array_equal(num_a.num, np.zeros(1)) and np.array_equal(num_b.num, np.zeros(1)):
            return True
        return False
    
    def larger(num_a, num_b):
        if big_num.equal(num_a, num_b):
            return False
        
        a, b, s_a, s_b = num_a.num, num_b.num, num_a.sign, num_b.sign
        l_a, l_b = len(a), len(b)
        if s_a == '+' and s_b == '-': return True
        if s_a == '+' and s_b == '+':
            if l_a > l_b: return True
            elif l_a < l_b: return False
            else:
                for i in range(l_a):
                    if a[i] > b[i]: return True
                    elif a[i] < b[i]: return False
        if s_a == '-' and s_b == '-':
            if l_a > l_b: return False
            elif l_a < l_b: return True
            else:
                for i in range(l_a):
                    if a[i] > b[i]: return False
                    elif a[i] < b[i]: return True
        return False 
    
    def smaller(num_a, num_b):
        if big_num.equal(num_a, num_b): return False
        if big_num.larger(num_a, num_b): return False
        return True
    
    # Functions for mathematical operations
    
    def addition(num_a, num_b):
        if num_a.n != num_b.n: 
            raise ValueError("The big numbers are in different element length representations",(num_a.n,num_b.n))    
        # a + b = res
        if (num_a.sign == '+' and num_b.sign == '+') or (num_a.sign == '-' and num_b.sign == '-'):
            l1, l2, a, b = len(num_a.num), len(num_b.num), num_a.num, num_b.num
            if(l1 > l2): b = np.hstack((np.zeros(l1-l2), b)) # add paddings to make two array
            elif(l2 > l1): a = np.hstack((np.zeros(l2-l1), a)) # has equal length       
            res = a + b
            i, carry, n = len(res)-1, 0, 10**num_a.n
            while(True):
                res[i] += carry
                if res[i] >= n: 
                    res[i] -= n
                    carry = 1
                else: carry = 0
                if i == 0:
                    if carry == 1:
                        res = np.hstack((np.ones((1)),res)) 
                    break
                i -= 1
            return big_num(res, num_a.n, num_a.sign)
        if num_a.sign == '+' and num_b.sign == '-':
            temp = big_num(num_b.num, num_b.n, '+')
        if num_a.sign == '-' and num_b.sign == '+':
            temp = big_num(num_b.num, num_b.n, '-')
        return big_num.subtract(num_a, temp)
        
    def subtract(num_a, num_b):
        if num_a.n != num_b.n: 
            raise ValueError("The big numbers are in different element length representations",(num_a.n,num_b.n))
        if (num_a.sign == '+' and num_b.sign == '+') or (num_a.sign == '-' and num_b.sign == '-'):
            temp_1, temp_2 = big_num(num_a.num, num_a.n, '+'), big_num(num_b.num, num_b.n, '+')
            if big_num.smaller(temp_1, temp_2):
                if num_a.sign == '+': sign = '-'
                else: sign = '+'
                l1, l2, a, b = len(num_b.num), len(num_a.num), num_b.num, num_a.num
            else:
                sign = num_a.sign 
                l1, l2, a, b = len(num_a.num), len(num_b.num), num_a.num, num_b.num
            if(l1 > l2): b = np.hstack((np.zeros(l1-l2), b)) # add paddings to make two array
            elif(l2 > l1): a = np.hstack((np.zeros(l2-l1), a))   
            res = a - b
            i, carry, n = len(res)-1, 0, 10**num_a.n
            while(True):
                res[i] += carry
                if res[i] < 0: 
                    res[i] = n + res[i]
                    carry = -1
                else: carry = 0
                if i == 0:
                    # if carry == -1:
                    #     res = np.hstack((np.ones((1)),res)) 
                    break
                i -= 1                
            return big_num(res, num_a.n, sign)
        if num_a.sign == '+' and num_b.sign == '-':
            temp = big_num(num_b.num, num_b.n, '+')
        if num_a.sign == '-' and num_b.sign == '+':
            temp = big_num(num_b.num, num_b.n, '-')
        return big_num.addition(num_a, temp)

    def multiplication(num_a, num_b):
        if num_a.n != num_b.n: 
            raise ValueError("The big numbers are in different element length representations",(num_a.n,num_b.n))    
        if (num_a.sign == '+' and num_b.sign == '+') or (num_a.sign == '-' and num_b.sign == '-'): sign = '+'
        else: sign = '-'
        l1, l2, a, b = len(num_a.num), len(num_b.num), num_a.num, num_b.num
        table = []
        for i in range(l1):
            temp = []
            for j in range(l2):
                temp.append(a[i] * b[j])
            for _ in range(l1-i-1):
                temp.append(0)
            table.append(np.asarray(temp))
        max_l = len(table[0]) + 1
        table = np.asarray(table,dtype=object)
        i = len(table)-1
        new_table = []
        while(True): # add paddings to the left of every row
            if i < 0: break
            new_table.append(np.hstack((np.zeros(max_l-len(table[i])), table[i])))
            i -= 1
        new_table = np.asarray(new_table)
        res = np.sum(new_table, axis = 0)
        i, carry, n= len(res)-1, 0, 10**num_a.n
        while(True): # compute carry and reform the number
            if i < 0: break
            res[i] += carry
            carry = res[i] - (res[i]%n)
            res[i] -= carry
            carry /= n
            i -= 1
        if int(res[0]) == 0: res = np.delete(res, 0)
        return big_num(res, num_a.n, sign)
    
    def division(num_a, num_b):
        if num_a.n != num_b.n: 
            raise ValueError("The big numbers are in different element length representations",(num_a.n,num_b.n))    
        if int(big_num.write_num_into_str(num_b)) == 0:
            raise ValueError("Error: Divisor = 0.")
        if (num_a.sign == '+' and num_b.sign == '+') or (num_a.sign == '-' and num_b.sign == '-'): sign = '+'
        else: sign = '-'
        l1, l2, a, b = len(num_a.num), len(num_b.num), num_a.num, num_b.num
        if big_num.equal(big_num(a, num_a.n, '+'), big_num(b, num_b.n, '+')): 
            return [big_num(np.ones(1), num_a.n, sign), big_num(np.zeros(1), num_a.n, num_a.sign)]
        elif big_num.smaller(big_num(a, num_a.n, '+'), big_num(b, num_b.n, '+')):
            return [big_num(np.zeros(1), num_a.n, num_a.sign), num_a]
        # start actual division from here
        # idea, dividend subtract multiples of divisors,
        # start from n = 10000, where n * divisor
        # gradually decrease n, by dividing by 10 until n = 1.
        n, res = 10000, 0
        temp_a = big_num(a, num_a.n, '+')
        while(True):
            print(123456)#------------------------------test--------------------------------------
            temp = big_num.write_num_into_vector(str(int(n)), num_a.n)
            sub = big_num.multiplication(temp, big_num(b, num_b.n, '+'))
            if big_num.smaller(sub, temp_a) or big_num.equal(sub, temp_a):
                temp_a = big_num.subtract(temp_a, sub)
                res += n
            elif big_num.larger(sub, temp_a) and n > 1:
                n /= 10
            if (big_num.equal(temp_a, big_num.write_num_into_vector('0'))):
                print(1234567)#------------------------------test--------------------------------------
                break 
            if (n == 1 and big_num.smaller(temp_a, big_num(b, num_b.n, '+'))):
                print(12345678)#------------------------------test--------------------------------------
                break
            print(res)
        res = big_num.write_num_into_vector(str(int(res)))
        return [big_num(res.num, res.n, sign), big_num(temp_a.num, temp_a.n, num_a.sign)]
                    

print('enter first num:')
temp_num1 = '+32'
print('enter second num:')
temp_num2 = '-8'
num_1 = big_num.write_num_into_vector(temp_num1,4)
print('num_1 = ', temp_num1)
print(num_1.num)
num_2 = big_num.write_num_into_vector(temp_num2,4)
print('num_2 = ', temp_num2)
print(num_2.num)
# print(temp_num2)
# print(num_2.num)
# num_sum = big_num.addition(num_1, num_2)
# print(num_sum.num)
# num_sum_str = big_num.write_num_into_str(num_sum)
# print(num_sum_str)
# print(big_num.equal(num_1, num_2))
# print(big_num.larger(num_1, num_2))
# print(big_num.smaller(num_1, num_2))
# num_sub = big_num.subtract(num_2, num_1)
# print(num_sub.num)

# print(big_num.write_num_into_str(big_num.subtract(num_1, num_2)))
# print(big_num.write_num_into_str(big_num.subtract(num_2, num_1)))
# print(big_num.write_num_into_str(big_num.addition(num_1, num_2)))
# print(big_num.write_num_into_str(big_num.addition(num_2, num_1)))
# print(big_num.write_num_into_str(big_num.multiplication(num_1, num_2)))
# print(big_num.write_num_into_str(big_num.multiplication(num_2, num_1)))
res = big_num.division(num_1, num_2)
print(big_num.write_num_into_str(res[0]),',',big_num.write_num_into_str(res[1]))
print("-----------------------------------------------------------------")


# print(int(temp_num1)-int(temp_num2))
# print(int(temp_num2)-int(temp_num1))
# print(int(temp_num2)+int(temp_num1))
# print(int(temp_num1)+int(temp_num2))
# print(int(temp_num1)*int(temp_num2))
# print(int(temp_num2)*int(temp_num1))
# print(int(temp_num1)/int(temp_num2))

# 已完成
# 字符转数字，数字转字符
# 大小比较函数
# 加减乘除
