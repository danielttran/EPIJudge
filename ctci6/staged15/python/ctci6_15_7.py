class FizzContext:
    def Wait(self,gate: int) -> None:
        raise RuntimeError("Provided synchronization primitive")
    def Signal(self,gate: int) -> None:
        raise RuntimeError("Provided synchronization primitive")
    def Print(self,value: int) -> None:
        raise RuntimeError("Provided role-bound print callback")
def RunFizzBuzz(role: int, limit: int, context: FizzContext) -> None:
    def owner(value):
        return 3 if value % 15 == 0 else 1 if value % 3 == 0 else 2 if value % 5 == 0 else 0

    for value in range(1, limit + 1):
        if owner(value) != role:
            continue
        context.Wait(role)
        context.Print(value)
        if value < limit:
            context.Signal(owner(value + 1))
