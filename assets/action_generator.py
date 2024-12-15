import math


def f(x1):
    return (x1 - 375) ** 2 / 400 + 75


frames = 90

with open("attack_left.txt", "w") as file:
    for i in range(frames):
        x = 600 - (450 * i / frames)
        file.write(f"{x:.0f} {f(x):.0f}\n")
    for i in range(frames):
        x = 450 * i / frames + 150
        file.write(f"{x:.0f} 200\n")

with open("attack_right.txt", "w") as file:
    for i in range(frames):
        x = 450 * i / frames + 150
        file.write(f"{x:.0f} {f(x):.0f}\n")
    for i in range(frames):
        x = 600 - (450 * i / frames)
        file.write(f"{x:.0f} 200\n")

with open("ultimate_right.txt", "w") as file:
    for x in range(158):
        file.write(f"{350 + -200 * math.cos(x / 25):.0f} {200 + -200 * math.sin(x / 25):.0f}\n")


with open("escape_left.txt", "w") as file:
    for x in range(30):
        file.write(f"{150 - 150 * x / 25:.0f} 200\n")
