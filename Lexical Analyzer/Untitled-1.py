def is_zero(items:[int],idx:int)->bool:
    val:int=0
    val=items[idx]
    return val==0

lst=[1,2,3,4]
mylist:[int]=None
mylist = [1, 0, 1]
print(is_zero(mylist, 1))