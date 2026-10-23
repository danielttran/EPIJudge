class SyncContext:
    def Wait(self,gate: int) -> None:
        raise RuntimeError("Provided synchronization primitive")
    def Signal(self,gate: int) -> None:
        raise RuntimeError("Provided synchronization primitive")
    def Work(self) -> None:
        raise RuntimeError("Provided worker callback")
def RunOrdered(role: int, context: SyncContext) -> None:
    if role > 0:
        context.Wait(role - 1)
    context.Work()
    if role < 2:
        context.Signal(role)
