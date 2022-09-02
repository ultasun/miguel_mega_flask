def decorate(func):
    print("Do something before func()")
    func()
    return func 

@decorate
def hello():
    print("Hello, world!")

