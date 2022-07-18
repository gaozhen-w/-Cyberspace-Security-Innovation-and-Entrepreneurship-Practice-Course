import random

def ROL(X, i):
    i = i % 32
    return ((X << i) & 0xFFFFFFFF) | ((X & 0xFFFFFFFF) >> (32 - i))

Try = [0x519d4519, 0xc4519d8a]

def Do_T(j):
    if j >= 0 and j <= 15:
        return Try[0]
    else:
        return Try[1]

def Fill(message):
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

def Group(m):
    n = len(m) / 128
    M = []
    for i in range(int(n)):
        M.append(m[0 + 128 * i:128 + 128 * i])
    return M

def Process1(X):
    return X ^ ROL(X, 9) ^ ROL(X, 17)

def Process2(X):
    return X ^ ROL(X, 15) ^ ROL(X, 23)

def Expand(M, n):
    W = []
    W_ = []
    for j in range(16):
        W.append(int(M[n][0 + 8 * j:8 + 8 * j], 16))
    for j in range(16, 68):
        W.append(Process2(W[j - 16] ^ W[j - 9] ^ ROL(W[j - 3], 15)) ^ ROL(W[j - 13], 7) ^ W[j - 6])
    for j in range(64):
        W_.append(W[j] ^ W[j + 4])
    Wstr = ''
    W_str = ''
    for x in W:
        Wstr += (hex(x)[2:] + ' ')
    for x in W_:
        W_str += (hex(x)[2:] + ' ')
    return W, W_

def Ado(X, Y, Z, i):
    if i >= 0 and i <= 15:
        return X ^ Y ^ Z
    else:
        return ((X & Y) | (~X & Z))

def Bdo(X, Y, Z, j):
    if j >= 0 and j <= 15:
        return X ^ Y ^ Z
    else:
        return ((X & Y) | (X & Z) | (Y & Z))

def CF(V, M, i):
    A, B, C, D, E, F, G, H = V[i]
    W, W_ = Expand(M, i)
    for j in range(64):
        M1 = ROL((ROL(A, 12) + E + ROL(Do_T(j), j % 32)) % (2 ** 32), 7)
        M2 = M1 ^ ROL(A, 12)
        T1 = (Bdo(A, B, C, j) + D + M2 + W_[j]) % (2 ** 32)
        T2 = (Ado(E, F, G, j) + H + M1 + W[j]) % (2 ** 32)
        D = C
        C = ROL(B, 9)
        B = A
        A = T1
        H = G
        G = ROL(F, 19)
        F = E
        E = Process1(T2)
    a, b, c, d, e, f, g, h = V[i]
    Group1 = [a ^ A, b ^ B, c ^ C, d ^ D, e ^ E, f ^ F, g ^ G, h ^ H]
    return Group1

R_key = [0x3614B2B9,0x5390166F, 0xACD442D7, 0xE38D0600, 0xA96F30BC, 0x30BC8D06, 0x0FB0EE4D, 0xB0FB3901]

def Iterate(M):
    n = len(M)
    V = []
    V.append(R_key)
    for i in range(n):
        V.append(CF(V, M, i))
    return V[n]

def SM3(message):
    m = Fill(message)  # 填充后消息
    M = Group(m)  # 数据分组
    ITER = Iterate(M)  # 迭代
    res = ''
    for x in ITER:
            res += hex(x)[2:]
    return res

def Pollard_Rho(example):
    num = int(example/4)                # 16进制位数
    x = hex(random.randint(0, 2**(example+1)-1))[2:]
    x_a = SM3(x)                # x_a = x_1
    x_b = SM3(x_a)              # x_b = x_2
    i = 1
    while x_a[:num] != x_b[:num]:
        i += 1
        x_a = SM3(x_a)              # x_a = x_i
        x_b = SM3(SM3(x_b))         # x_b = x_2i
    x_b = x_a           # x_b = x_i
    x_a = x             # x_a = x
    for j in range(i):
        if SM3(x_a)[:num] == SM3(x_b)[:num]:
            return SM3(x_a)[:num], x_a, x_b
        else:
            x_a = SM3(x_a)
            x_b = SM3(x_b)

if __name__ == '__main__':
    gaozhen = 12 
    formal, m1, m2 = Pollard_Rho(gaozhen)
    print("message1:", m1)
    print("message2:", m2)
    print("找到碰撞，哈希值的前{}bit相同，其16进制为:{}".format(gaozhen, formal))