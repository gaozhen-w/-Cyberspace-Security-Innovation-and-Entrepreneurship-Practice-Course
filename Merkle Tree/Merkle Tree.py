import string
import random
from hashlib import sha256



def Hash(data):
    return sha256(data.encode('utf-8')).hexdigest()
def func1(d0):
    return hex(0)+d0
def func2(d1,d2):
    return hex(1)+d1+d2

class Merkel:
    def __init__(self , data):
        self.l=data
        self.root,self.LR=self.merkel()
        print('root hash:',self.root)
        print('字典',self.LR)

    def merkel(self):
        lst = []
        LR=dict()#字典，标记左右,0左1右
        h=0
        if len(self.l)==0:
            lst=sha256().hexdigest()
            print('depth:0')
            return lst,{}
        elif len(self.l)==1:
            lst.append(Hash(func1(self.l[0])))
            print('depth:1')
            return lst,{}
        else:
            for i in self.l:
                lst.append(Hash(i))

            while len(lst) >1:
                h+=1
                temp=[]
                if len(lst)%2 == 0:
                    while len(lst) >1 :
                        a = lst.pop(0)
                        LR[a]=0
                        b = lst.pop(0)
                        LR[b]=1
                        temp.append(Hash(func2(a,b)))
                    lst = temp
                else:
                    last = lst.pop(-1)
                    while len(lst) >1 :
                        a = lst.pop(0)
                        LR[a]=0
                        b = lst.pop(0)
                        LR[b]=1
                        temp.append(Hash(func2(a,b)))
                    temp.append(last)
                    LR[last]=1
                    lst = temp
            print('depth:',h+1)
            return lst[0],LR


    def aupath(self,m,l):
        k=0
        P=[]
        if len(l)==2:
            P.append(l[(m+1)%2])
            return P
        elif len(l)>2:
            for i in range(1,len(l)):
                if pow(2,i)>=len(l):
                    k=pow(2,i-1)
                    break
            if m<k:
                P.extend(self.aupath(m,l[0:k]))
                P.append(self.mth(l[k:len(l)]))#接收第一个返回值
                return P
            elif m>=k:
                P.extend(self.aupath(m-k,l[k:len(l)]))
                P.append(self.mth(l[0:k]))
                return P
        else:
            return P



    def AuditPaths(self,m):#第m位置的path
        lst=[]
        if len(self.l)>1:
            for i in range(0,len(self.l)):
                lst.append(Hash(self.l[i]))
            return self.aupath(m,lst)
        elif len(self.l)==1:
            return {}
        else:
            return -1

    def mt(self,l):
        #print('len:', len(l))
        k = 0
        if len(l)==1:
            return l[0]
        elif len(l)==2:
            return Hash(func2(l[0], l[1]))
        else:
            for i in range(0,len(l)):
                if pow(2,i)>=len(l):
                    k = pow(2, i-1)
                    break
            #print('k:', k)
            return Hash(func2(self.mt(l[0:k]), self.mt(l[k:len(l)])))


    def mth(self,l):
        L = []

        h = 0 #merkle树高度

        if len(l)==1:#输入个数为1时
            L = l[0]
            #L = hash_data(concatenation_0(l[0]))
            return L

        elif len(l)>1:
            return self.mt(l)



    def proof(self,m,leaf):
        # root,LR=Merkel(l)


        audit_path=self.AuditPaths(m)
        print('audit path:',audit_path)

        leafhash=Hash(leaf)
        for i in audit_path:
            if self.LR[i]==0:
                leafhash=Hash(func2(i,leafhash))
            else:
                leafhash=Hash(func2(leafhash,i))

        if leafhash == self.root:
            return True
        else:
            return False










map=string.punctuation+string.ascii_letters+string.digits

#测试十万个叶子节点？
def test(length):
    longrandom=''
    for i in  range(length):
        longrandom+=random.choice(map)





    allstr=[longrandom[i:i+2]for i in range(0,len(longrandom))]
    print("leaves:",allstr)
    print("nums",len(allstr))
    print("root:",Merkel(allstr).root)

if __name__=='__main__':

    l = ['1', '2', '3','4','5']
    # print(Merkel(l).root )

    # 测试叶子节点十万个：
    # test(100000)





    #存在性证明
    # m=1
    #
    ex=Merkel(l)
    print(ex.proof(1,'2'))

