from hashlib import sha256
import random
import string

class Merkel_Tree:

    def __init__(self,data,m,n):
        self.l=data
        self.root,self.high,self.SonTree=self.merkel()
        self.path=self.proof(m,n)
        self.lst=self.creat_chain()


    def creat_chain(self):              #创建链表

        lst = []
        for i in self.l:
            lst.append(Hash(i))
        return lst

    def get_num1(self,l):               #将表的长度与2的i次方做比较，并且返回2的i-1次方

        for i in range(1,len(l)):
            if pow(2,i)>=len(l):
                k=pow(2,i-1)
                return k
    

    def aupath(self,m,l):
        res=l[(m+1)%2]
        k=0
        P=[]
        if len(l)==2:
            P.append(res)
            return P
        elif len(l)>2:
           
            k=self.get_num1(l)
            if m<k:
                P.extend(self.aupath(m,l[0:k]))
                P.append(self.mth(l[k:len(l)]))   #接收第一个返回值

                return P
            elif m>=k:
                P.extend(self.aupath(m-k,l[k:len(l)]))
                P.append(self.mth(l[0:k]))
                return P
        else:
            return P


    def creat_sontree(self):            #生成merkel tree的子树

        lst=self.creat_chain()
        SonTree=dict()
        h=0
        while len(lst) >1:
            temp=[]
            if len(lst)%2 == 0:

                while len(lst) >1 :
                    a = lst.pop(0)
                    b = lst.pop(0)
                    SonTree[a]=0
                    SonTree[b]=1
                    temp.append(Hash(hex_func(a,b)))
                lst = temp
            else:                       #若块数为偶数，最后一个块直接放入下一层。

                last = lst.pop(-1)
                while len(lst) >1 :
                    a = lst.pop(0)
                    b = lst.pop(0)
                    SonTree[a]=0
                    SonTree[b]=1
                    temp.append(Hash(hex_func(a,b)))
                temp.append(last)
                SonTree[last]=1
                lst = temp
            h=h+1                       #最终数的高度要加上root，即+1
        return lst[0],h+1,SonTree

    def AuditPaths(self,m):             #求解从根节点到第m位置节点的路径

        lst=[]
        if len(self.l)>1:
            for i in range(0,len(self.l)):
                lst.append(Hash(self.l[i]))
            return self.aupath(m,lst)
        elif len(self.l)==1:
            return {}
        else:
            return -1


    def mth(self,l):
        T = []

        if len(l)==1:                   #输入的链表长度为1时
            T = l[0]
            return T

        elif len(l)>1:
            k=0
            if len(l)==1:
                return l[0]

            elif len(l)==2:
                return Hash(hex_func(l[0], l[1]))

            else:
                k=self.get_num1(l)
                return Hash(hex_func(self.mt(l[0:k]), self.mt(l[k:len(l)])))

    def mt(self,l):

        k = 0
        if len(l)==1:
            return l[0]
        elif len(l)==2:
            return Hash(hex_func(l[0], l[1]))
        else:
            for i in range(0,len(l)):
                if pow(2,i)>=len(l):
                    k = pow(2, i-1)
                    break
            return Hash(hex_func(self.mt(l[0:k]), self.mt(l[k:len(l)])))

    def proof(self,m,leaf):

        audit_path=self.AuditPaths(m)       # 指定元素在数第一层的索引值

        through_path=[]                     #审计路线
        through_path.append(self.root)
        through_path.extend(audit_path)

        leafhash=Hash(leaf)
        for i in audit_path:
            if self.SonTree[i]==0:
                leafhash=Hash(hex_func(i,leafhash))
            else:
                leafhash=Hash(hex_func(leafhash,i))

        if leafhash == self.root:
            print('we get the True tree!!!')
            
        else:
            print('we get the True tree!!!')
            

    def merkel(self):                       #运行，构建整个Merkel Tree
        SonTree=dict()
        root,high,SonTree=self.creat_sontree()
        return root,high,SonTree

def hex_func(num1,num2):
        return hex(1)+num1+num2

def Hash(data):
    return sha256(data.encode('utf-8')).hexdigest()   



tree=string.punctuation+string.ascii_letters+string.digits   #进行测试，测试结点为100000
def test(length):
    longrandom=''
    for i in  range(length):
        longrandom+=random.choice(tree)

    MT_all=[longrandom[i:i+2]for i in range(0,len(longrandom))]

    print("nums",len(MT_all))
    print("leaves:",MT_all)
    print("root:",Merkel_Tree(MT_all,1,'20').root)

if __name__=='__main__':


    #正确性证明
    T = ['10', '20', '30','40','50']
    MT=Merkel_Tree(T,1,'20')
    print('the higth of the merkle tree',MT.high)       #输出Merkel Tree的高度
    print('the root of the merkle tree',MT.root)        #输出树的根节点
    print('the path from root to tail',MT.path)         #输出其中毅腾最佳路径
    print('the whole structure of the merkle tree',MT.SonTree)   #其中0为左子树，1为右子树


    #测试，生成一个10万叶子节点的Merkel Tree
    #test(100000)

