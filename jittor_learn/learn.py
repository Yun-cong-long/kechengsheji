import jittor as jt
a = jt.float32([1,2,3])
print(a)
print(a.data)

x = jt.Var([2,3,4])
print(x)

b = jt.array([jt.float32(2),jt.float32(3),jt.float32(4)])
print(b)

c = a*b
print(c)
print(type(a), type(b), type(c))

d = c.max()
e = c.min()
print(d,e)

# help(jt.ops)