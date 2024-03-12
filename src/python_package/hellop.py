"""This is a docstring for a dummy file :)"""
def hello_world(i: int = 0) -> str:
    """Function description"""
    print("hello world")
    return f"string-{i}"


def good_night() -> str:
    """Function description"""
    print("good night")
    return "string"


def hello_goodbye():
    """Function description"""
    hello_world(1)
    good_night()
