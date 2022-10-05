import pixy
# from pixy import pring, TrueColour
from pathlib import Path


def gradient(colour_a, colour_b):

    output = []

    for i in range(0, 100, 2):

        p = i / 100

        output.append(
            (
                int(colour_a[0] + p * (colour_b[0] - colour_a[0])),
                int(colour_a[1] + p * (colour_b[1] - colour_a[1])),
                int(colour_a[2] + p * (colour_b[2] - colour_a[2])),
            )
        )

    return output


CWD = Path.cwd()
lorem_path = CWD / "tasks" / "lorem.txt"
with open(lorem_path, "r") as infile:
    lorem_ipsum = infile.read()

red_to_magenta = gradient((255, 0, 0), (255, 17, 255))
green_to_blue = gradient((0, 255, 0), (0, 0, 255))
blue_to_red = gradient((0, 0, 255), (255, 0, 0))

for color in red_to_magenta:
    print(
        pixy.pring(
            """Elit minim nostrud ullamco ipsum minim culpa eu culpa incididunt minim pariatur ex pariatur aliquip Lorem. In voluptate laborum pariatur ipsum ipsum deserunt eu eu officia. Cupidatat pariatur sit dolor irure consectetur qui nisi veniam laboris. Sunt irure adipisicing id aute magna voluptate anim sit est ad exercitation est ut nostrud. Nostrud amet occaecat labore excepteur aliqua amet culpa irure. Tempor deserunt ea ad reprehenderit excepteur pariatur nostrud velit adipisicing nostrud commodo cupidatat. Consequat cupidatat enim nostrud aliqua anim. Mollit excepteur nulla aliqua aute occaecat. Deserunt ex ex dolor ex nostrud nisi duis nostrud sunt reprehenderit irure culpa irure ad nostrud. Sit in est duis incididunt dolore.""",
            pixy.TrueColour(color, background=True),
        ),  # type: ignore
        end="",
    )

print()

# for colour in green_to_blue:
#     print(
#         pring(  # type: ignore
#             " ", pixy.TrueColour(*colour, background=True)  # type: ignore
#         ),
#         end="",
#     )

# print()

# for colour in blue_to_red:
#     print(
#         pring(  # type: ignore
#             " ", pixy.TrueColour(*colour, background=True)  # type: ignore
#         ),
#         end="",
#     )

# print()
