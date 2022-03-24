import time


class Timer:
    def __init__(self):
        self.time: float = time.time()

    def timeit(self, message: str) -> None:
        new_time: float = time.time()
        print(f"{message} with {new_time-self.time} seconds")
        self.time = new_time


if __name__ == "__main__":
    timer = Timer()
    timer.timeit()