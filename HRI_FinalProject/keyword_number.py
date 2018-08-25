# with open and close function for the .txt file
with open("douban.txt","w") as f:
f.write("this is for the test")

# write something to sys.stdout
import sys
with open('test.txt','w') as f:
    sys.stdout = f
    print([1,2,3])
    print('hello')

# csv file
import csv
with open('log.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([1,2,3,4,5])
    writer.writerows([[1,1,1],[2,2,2]])