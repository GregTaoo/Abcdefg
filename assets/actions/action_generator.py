import math


def f(x1):
    return (x1 - 375) ** 2 / 400 + 75


frames = 90

with open("attack_left.txt", "w") as file:
    for i in range(frames):
        x = 600 - (450 * i / frames)
        file.write(f"{x:.0f} {f(x):.0f}\n")
    file.write("150 200|10||hit\n")
    for i in range(frames // 2):
        x = 450 * i / frames * 2 + 150
        file.write(f"{x:.0f} 200\n")

with open("attack_right.txt", "w") as file:
    for i in range(frames):
        x = 450 * i / frames + 150
        file.write(f"{x:.0f} {f(x):.0f}\n")
    file.write("600 200|10||hit\n")
    for i in range(frames // 2):
        x = 600 - (450 * i / frames * 2)
        file.write(f"{x:.0f} 200\n")

with open("ultimate_right.txt", "w") as file:
    for x in range(10):
        file.write(f"{150 + 450 / 10 * x} 200\n")
    for x in range(10):
        file.write(f"600 200\n")
    for x in range(10):
        file.write(f"{600 - 100 / 10 * x} {200 - 100 / 10 * x} {600 + 100 / 10 * x} {200 - 100 / 10 * x}"
                   f" {600 - 100 / 10 * x} {200 + 100 / 10 * x} {600 + 100 / 10 * x} {200 + 100 / 10 * x}"
                   f"|6|分身之术!|zeus\n")
    # file.write(f"500 100 700 100 500 300 700 300|6||zeus\n")
    for x in range(90):
        k = (math.sqrt(100 / 90) * x) ** 2
        file.write(f"{500 + k} {100 + k} {700 - k} {100 + k}"
                   f" {500 + k} {300 - k} {700 - k} {300 - k}|0|分身之术!\n")
    for x in range(40):
        file.write(f"{600 - 450 / 40 * x} 200\n")


with open("escape_left.txt", "w") as file:
    for x in range(30):
        file.write(f"{150 + 350 / 30 * x} 200\n")
    for x in range(20):
        file.write(f"500 200\n")
    for x in range(50):
        file.write(f"500 200|0|菜就多练\n")
    for x in range(30):
        file.write(f"{500 - 550 * x / 25:.0f} 200\n")
