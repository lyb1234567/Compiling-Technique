# 构造NFA
class NFA:
    # 初始化NFA
    def __init__(self, S, s0, F, move):
        self.S = S  # 状态集(list)
        self.s0 = s0  # 初态(int)
        self.F = F  # 终态(int)
        self.move = move  # 状态转换函数（list套dict）

    # 计算状态集T的n(代替ε)闭包U
    def getClosure(self, T):
        U = list()  # 闭包集合
        Stack = list()  # 栈
        for t in T:
            Stack.append(t)  # 将t入栈
            U.append(t)  # 先将T加入U
        # 当栈非空
        while Stack:
            t = Stack.pop()  # 取出栈顶元素
            # 如果能转换(判断字典中是否存在key为'n')
            if 'n' in move[t]:
                u = self.move[t]['n']  # 得到转换后状态u
                # 若转换后状态不在闭包集合U中，加u入U
                if u not in U:
                    # 因为u为list类型，所以循环加入
                    for x in u:
                        Stack.append(x)
                        U.append(x)
            # 如果不能转换
            else:
                #print('不能转换，啥事都不干~')
                pass

        #print('返回闭包', U)
        return U

    # smove方法,T为初态集，n为待识别字符(str类型),返回转换后的状态集U
    def smove(self, T, n):
        U = list()  # 存储smove后的状态集
        for t in T:
            # 如果能转换(判断字典中是否存在key为'n')
            if n in move[t]:
                u = self.move[t][n]  # 得到转换后状态u
                # 若转换后状态不在闭包集合U中，加u入U
                if u not in U:
                    # 因为u为list类型，所以循环加入
                    for x in u:
                        U.append(x)
            # 如果不能转换
            else:
                #print('不能转换，啥事都不干~')
                pass
        return U


# 构造DFA
class DFA:
    # 通过NFA对象N构造DFA
    def __init__(self, N):
        print('---------开始使用子集法构造DFA---------')
        self.s0 = N.getClosure([0])  # 初态(list)
        self.Dstates = [self.s0]  # 存储DFA的状态
        self.DstatesFlag = [0]  # 记录状态是否被标记过，元素个数代表还未被标记的数目
        self.F=N.F#终态
        curIndex = 0  # 当前处理到的Dstates的下标
        Dtran = list() # 状态转换矩阵
        U1 = list()#暂存器，用于存储转换后的状态集，便于写入转换矩阵
        U2 = list()#同上
        # 当DFA状态集中有尚未标记的状态T
        while self.DstatesFlag:
            self.DstatesFlag.pop()  # 取出一个标记
            #循环求闭包
            for ch in ['a', 'b']:
                #求出smove后的闭包U
                U = N.getClosure(N.smove(self.Dstates[curIndex], ch))
                #条件判断构造写入格式Dtran.append({'a': U1, 'b': U2})
                if ch == 'a':
                    U1 = U
                else:
                    U2 = U
                # 如果U不在Dstates中，将U作为未标记的状态加入Dstates中
                if U not in self.Dstates:
                    self.Dstates.append(U)#将U加入到状态集中
                    self.DstatesFlag.append(0)#长度增1，表示新增一个未标记状态
                    #print('Dstates更新为:',self.Dstates)

            Dtran.append({'a': U1, 'b': U2})#将转换结果写入转换矩阵中
            curIndex+=1 # 下标增1

        self.move = Dtran  # 构造状态转换函数（list套dict）
        print('DFA的初态s0:',self.s0)
        print('DFA的终态F:', self.F)
        print('DFA的状态集Dstates:', self.Dstates)
        print('DFA的状态转换矩阵Dtran:', self.move)

        print('---------DFA构造完成，开始验证字符识别功能---------')

    # 判断是否接受x
    def isAccept(self, x):
        print('开始判断是否接受输入的字符串:',x)
        #循环识别输入字符串
        for ch in x:
            #因为Dstatea中的状态为顺序加入，A集合对象下标0，B对应下标1
            # 而move矩阵也是按此方式存储，得到当前状态集在Dstates中的下标
            curindex=self.Dstates.index(self.s0)
            #状态转换
            if ch not in ['a', 'b']:
                break
            self.s0=self.move[curindex][ch]
            print('状态转换一次，此时的状态集为:', self.s0)
            #如果转换后状态集的下标等于Dstates的长度-1
            #说明当前转换状态为Dstates的末尾状态，即终态

        if self.F in self.s0:
            print('识别已结束，字符串',x,'被接受~~')
        else:
            print('识别已结束，字符串',x,'被拒绝T T')
        return 0


if __name__ == '__main__':
    print("---------本程序用于识别正规式为'(a|b)*abb'的字符序列---------")
    print("---------即将开始收集用于构造NFA的初始数据，请按提示操作---------' ")
    # 构造NFA  开始
    #S = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    print("请输入状态集S,输入格式为List嵌套Dict,如'[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]' ")
    S =  eval(input(":"))
    # s0 = 0
    s0 = int(input("请输入初态s0,如'0' :"))
    # F = 10
    F = int(input("请输入终态F,如'10' :"))
    #move = [{'n': [1, 7]}, {'n': [2, 4]}, {'a': [3]}, {'n': [6], }, {'b': [5]}, {'n': [6]}, {'n': [1, 7]}, {'a': [8]}, {'b': [9]}, {'b': [10]},{}]
    print("请输入状态转移矩阵,输入格式为List嵌套Dict,如'[{'n': [1, 7]}, {'n': [2, 4]}, {'a': [3]}, {'n': [6], }, {'b': [5]}, {'n': [6]}, {'n': [1, 7]}, {'a': [8]}, {'b': [9]}, {'b': [10]},{}]' ")
    move = eval(input(":"))

    N = NFA(S, s0, F, move)
    print("---------数据收集完毕，NFA构造完成---------' ")
    # 构造NFA  结束

    D=DFA(N)#通过NFA对象N构造DFA

    #print(D.move)#输出DFA转换矩阵
    while True:
        x = input('请输入要识别的字符串x：')#提示输入
        if x=='quit':
            print('程序结束运行')
            break
        D.isAccept(x)  # 判断是否接受