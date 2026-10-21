from test_framework.test_failure import TestFailure


class ClientsCreditsInfo:
    def __init__(self):
        self.offset = 0
        self.credits = {}

    def insert(self, client_id, credit):
        self.credits[client_id] = credit - self.offset

    def remove(self, client_id):
        if client_id not in self.credits:
            return False
        del self.credits[client_id]
        return True

    def lookup(self, client_id):
        return self.credits[client_id] + self.offset if client_id in self.credits else -1

    def add_all(self, amount):
        self.offset += amount

    def max(self):
        return max(self.credits, key=self.credits.get) if self.credits else ''


def client_credits_info_tester(ops):
    clients = ClientsCreditsInfo()
    for operation, client, value in ops:
        if operation == 'ClientsCreditsInfo':
            clients = ClientsCreditsInfo()
        elif operation == 'insert':
            clients.insert(client, value)
        elif operation == 'add_all':
            clients.add_all(value)
        elif operation == 'remove':
            if clients.remove(client) != (value == 1):
                raise TestFailure('Removal did not report whether the client existed.')
        elif operation == 'lookup':
            if clients.lookup(client) != value:
                raise TestFailure('The client credit differs from the expected credit.')
        elif operation == 'max':
            if clients.max() != client:
                raise TestFailure('The maximum-credit client differs from the expected client.')
        else:
            raise ValueError('Unknown credits operation: ' + operation)
