# UTF-8 to a single integer
# Hash function

def to_int_nonuniform(data_test, prime):
    # input: UTF-8
    # output: integer -- a user input value
    # algorihtm: data_test % prime
    sum = 0
    length = len(data_test)
    for i in range(length):
        sum += data_test[i]
    hash = sum % prime
    return hash

def to_int_uniform():
    # input UTF-8
    hash = 1
    return hash

def Hash_invertible():
    a = 3

# Test the result
print(  to_int_nonuniform('test', 8) )