from hashlib import sha256


class Merkel_Tree:

    def __init__(self,data,m,n):
        self.l=data
        self.root,self.high,self.SonTree=self.merkel()
        self.path=self.proof(m,n)
        self.lst=self.creat_chain()


    def creat_chain(self):
        lst = []
        for i in self.l:
            lst.append(Hash(i))
        return lst

    def get_num1(self,l):
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
                P.append(self.mth(l[k:len(l)]))#接收第一个返回值
                return P
            elif m>=k:
                P.extend(self.aupath(m-k,l[k:len(l)]))
                P.append(self.mth(l[0:k]))
                return P
        else:
            return P


    def creat_sontree(self):
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
            else:
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
            h=h+1
        return lst[0],h+1,SonTree

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


    def mth(self,l):
        T = []

        if len(l)==1:#输入个数为1时
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



    def proof(self,m,leaf):

        audit_path=self.AuditPaths(m)
        through_path=[]
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
            print('we get the Wrong tree!!!')
            

    def merkel(self):
        SonTree=dict()
        root,high,SonTree=self.creat_sontree()
        return root,high,SonTree

def hex_func(num1,num2):
        return hex(1)+num1+num2

def Hash(data):
    return sha256(data.encode('utf-8')).hexdigest()   

if __name__=='__main__':

    T = ['10', '20', '30','40','50']
    MT=Merkel_Tree(T,1,'20')
    print('the higth of the merkle tree',MT.high)
    print('the root of the merkle tree',MT.root)
    print('the path from root to tail',MT.path)
    print('the whole structure of the merkle tree',MT.SonTree)#0为左子树，1为右子树