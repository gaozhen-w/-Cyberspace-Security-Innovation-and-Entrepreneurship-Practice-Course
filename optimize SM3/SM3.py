import random
from numpy import append

def get_num(len):

    seed = "1234567890"
    str1=[]
    for i in range(len):
        str1.append(random.choice(seed))
    String=''.join(str1)

    return String

def test(num):

    res1=sm3(num)
    res2=sm3(num)
    print('the test number is:{}'.format(num))
    if res1.result==res2.result:
        print ('By test,two same figures lead to the same results,True!')  
    else:
        print ('By test,two same figures lead to different results,Wrong!') 

key = [0x3614B2B9,0x5390166F, 0xACD442D7, 0xE38D0600, 
0xA96F30BC, 0x30BC8D06, 0x0FB0EE4D, 0xB0FB3901]

R_key = [0x79cc4519, 0x7a879d8a]

class sm3:

    def __init__(self,str1):
        self.result=self.SM3(str1)
    
    def SM3(self,message):

        m = self.TianChong(message)  # 填充后消息
        M = self.Group(m)  # 数据分组
        Vn = self.iteration(M)  # 迭代
        res = ''
        for x in Vn:
                res += hex(x)[2:]
        return res

    def T_(self,j):

        if j >= 0 and j <= 15:
            return R_key[0]
        else:
            return R_key[1]
    

    def FF(self,X, Y, Z, j):

        if j >= 0 and j <= 15:
            return X ^ Y ^ Z
        else:
            return ((X & Y) | (X & Z) | (Y & Z))
    
    def GG(self,X, Y, Z, j):

        if j >= 0 and j <= 15:
            return X ^ Y ^ Z
        else:
            return ((X & Y) | (~X & Z))


    def TianChong(self,message):

        m = bin(int(message, 16))[2:]
        if len(m) != len(message) * 4:
            m = '0' * (len(message) * 4 - len(m)) + m
        l = len(m)
        l_bin = '0' * (64 - len(bin(l)[2:])) + bin(l)[2:]
        m = m + '1'
        if len(m) % 512 > 448:
            m = m + '0' * (512 - len(m) % 512 + 448) + l_bin
        else:
            m = m + '0' * (448 - len(m) % 512) + l_bin
        m = hex(int(m, 2))[2:]
        return m


    def Group(self,m):

        n = len(m) / 128
        M = []
        for i in range(int(n)):
            M.append(m[0 + 128 * i:128 + 128 * i])
        return M

    def get_num(self,X):

        return X ^ self.ROL(X, 15) ^ self.ROL(X, 23)

    def Expand(self,M, n):

        W = []
        W_ = []
        for j in range(16):
            W.append(int(M[n][0 + 8 * j:8 + 8 * j], 16))
        for j in range(16, 68):
            W.append(self.get_num(W[j - 16] ^ W[j - 9] ^ self.ROL(W[j - 3], 15)) ^ self.ROL(W[j - 13], 7) ^ W[j - 6])
        for j in range(64):
            W_.append(W[j] ^ W[j + 4])
        Wstr = ''
        W_str = ''
        for x in W:
            Wstr += (hex(x)[2:] + ' ')
        for x in W_:
            W_str += (hex(x)[2:] + ' ')
        return W, W_

    def ROL(self,X,i):

        i = i % 32
        return ((X << i) & 0xFFFFFFFF) | ((X & 0xFFFFFFFF) >> (32 - i))

    def P0(self,X):

        return X ^ self.ROL(X, 9) ^ self.ROL(X, 17)

    def Cross_Func(self,V, M, i):

        A, B, C, D, E, F, G, H = V[i]
        W, W_ = self.Expand(M, i)
        for j in range(64):
            sh1 = self.ROL((self.ROL(A, 12) + E + self.ROL(self.T_(j), j % 32)) % (2 ** 32), 7)
            sh2 = sh1 ^ self.ROL(A, 12)
            test1 = (self.FF(A, B, C, j) + D + sh2 + W_[j]) % (2 ** 32)
            test2 = (self.GG(E, F, G, j) + H + sh1 + W[j]) % (2 ** 32)
            D = C
            C = self.ROL(B, 9)
            B = A
            A = test1
            H = G
            G = self.ROL(F, 19)
            F = E
            E = test2 ^ self.ROL(test2, 9) ^ self.ROL(test2, 17)
        a, b, c, d, e, f, g, h = V[i]
        V_ = [a ^ A, b ^ B, c ^ C, d ^ D, e ^ E, f ^ F, g ^ G, h ^ H]
        return V_

    
    def iteration(self,M):
        
        n = len(M)
        V = []
        V.append(key)
        for i in range(n):
            V.append(self.Cross_Func(V, M, i))
        return V[n]


if __name__ == '__main__':
    #得到一个长度为10的随机数字加密结果
    a=get_num(10)

    res=sm3(a)
    print('the final result we get is:\n{}'.format(res.result))

    b='1231255683' #长度为10的稳定性测试
    test(b)
