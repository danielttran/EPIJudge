class ForkContext:
    def Take(self,fork: int) -> None:
        raise RuntimeError("Provided fork lock")
    def Drop(self,fork: int) -> None:
        raise RuntimeError("Provided fork lock")
    def Eat(self) -> None:
        raise RuntimeError("Provided eating callback")
def Dine(role: int, philosophers: int, bites: int, context: ForkContext) -> None:
    left, right = role, (role + 1) % philosophers
    lower, higher = min(left, right), max(left, right)
    for _ in range(bites):
        context.Take(lower)
        context.Take(higher)
        context.Eat()
        context.Drop(higher)
        context.Drop(lower)
