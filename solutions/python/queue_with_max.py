from collections import deque

class QueueWithMax:
    def __init__(self):
        self.values = deque()
        self.candidates = deque()

    def enqueue(self, value):
        self.values.append(value)
        while self.candidates and self.candidates[-1] < value:
            self.candidates.pop()
        self.candidates.append(value)

    def dequeue(self):
        value = self.values.popleft()
        if self.candidates[0] == value:
            self.candidates.popleft()
        return value

    def max(self):
        return self.candidates[0]
