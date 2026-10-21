class Queue:
    def __init__(self, capacity):
        self.buffer = [0] * max(1, capacity)
        self.head = self.count = 0

    def enqueue(self, value):
        if self.count == len(self.buffer):
            larger = [0] * (2 * len(self.buffer))
            for i in range(self.count):
                larger[i] = self.buffer[(self.head + i) % len(self.buffer)]
            self.buffer, self.head = larger, 0
        self.buffer[(self.head + self.count) % len(self.buffer)] = value
        self.count += 1

    def dequeue(self):
        if self.count == 0:
            raise IndexError('The queue is empty')
        value = self.buffer[self.head]
        self.head = (self.head + 1) % len(self.buffer)
        self.count -= 1
        return value

    def size(self):
        return self.count
