import math


def f(x1):
    return (x1 - 400) ** 2 / 200


frames = 90

with open("attack_left.txt", "w") as file:
    for i in range(frames):
        x = 600 - (400 * i / frames)
        file.write(f"{x:.0f} {f(x):.0f}\n")
    for i in range(frames):
        x = 400 * i / frames + 200
        file.write(f"{x:.0f} 200\n")

with open("attack_right.txt", "w") as file:
    for i in range(frames):
        x = 400 * i / frames + 200
        file.write(f"{x:.0f} {f(x):.0f}\n")
    for i in range(frames):
        x = 600 - (400 * i / frames)
        file.write(f"{x:.0f} 200\n")

with open("attack_ult_right.txt", "w") as file:
    for x in range(90):
        file.write(f"{300 + math.cos(x / 25):.0f} {200 + math.sin(x / 25):.0f}\n")

