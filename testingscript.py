import Justerror
import manual
Justerror.setup()
while True:
    manual.rc()
    Justerror.DoRound(*[float(i) for i in input("Enter MaxSpeed,BackSPeed,AngleToDo: ").split(" ")])
