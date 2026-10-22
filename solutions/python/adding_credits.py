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
    # Model absolute credits independently of all submitted methods.
    expected_credits = {}
    for operation, client, value in ops:
        if operation == 'ClientsCreditsInfo':
            clients = ClientsCreditsInfo()
            expected_credits.clear()
        elif operation == 'insert':
            clients.insert(client, value)
            expected_credits[client] = value
        elif operation == 'add_all':
            clients.add_all(value)
            for name in expected_credits:
                expected_credits[name] += value
        elif operation == 'remove':
            if clients.remove(client) != (value == 1):
                raise TestFailure('Removal did not report whether the client existed.')
            expected_credits.pop(client, None)
        elif operation == 'lookup':
            if clients.lookup(client) != value:
                raise TestFailure('The client credit differs from the expected credit.')
        elif operation == 'max':
            actual = clients.max()
            valid = (actual in expected_credits and
                     expected_credits[actual] == max(expected_credits.values())) if expected_credits else actual == ''
            if not valid:
                raise TestFailure('Max must return an existing maximal-credit client, or empty when no clients exist.')
        else:
            raise ValueError('Unknown credits operation: ' + operation)
