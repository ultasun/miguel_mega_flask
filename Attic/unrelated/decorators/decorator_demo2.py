def wrap(func):
    def wrapper():
        print("Say hellow? Y/N")
        if input() == "Y":
            func()
        else:
            print("OK.")
    return wrapper

@wrap
def hello():
    print("Hello, world!")

hello()

