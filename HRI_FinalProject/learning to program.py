
#The array from 0 to the following
square=[1,2,3,4]
square=[1,2,3,4]+[2,3,4,5]
words = ['cat', 'window', 'defenestrate']

#While
a,b=0,1
while b<10
    print b
    a,b=b,a+b

#print
print "The value of i is", str(i)   # "," is important here
print "The value of i is" + str(i)
print 'The value of i is',i

#input
x = int(  raw_input("Please enter an integer: ")  )
x = int ( 4+1 )

#if
if x < 0:
     x = 0
     print 'Negative changed to zero'
 elif x == 0:
     print 'Zero'
 elif x == 1:
     print 'Single'
 else:
     print 'More'

#for
count = 0
for w in words[:]:  # Loop over a slice copy of the entire list.
     count = count +1
     if len(w) > 6:
         if __name__ == '__main__':
             words.insert(0, w) # insert function means to insert the word in "0" position

a = ['Mary', 'had', 'a', 'little', 'lamb']
count = 0
for i in range(len(a)):
    print i, a[i]
    count += 1








