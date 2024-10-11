# Standard Library
import typing


def count_donuts(h: int, w: int, grid: typing.List[str]) -> int:
    donut_pattern = [["#", "#", "#"], ["#", ".", "#"], ["#", "#", "#"]]

    donut_count: int = 0

    for i in range(h - 2):
        for j in range(w - 2):
            # 3x3の範囲を取り出す
            section: list[list[str]] = [
                list(row[j : j + 3]) for row in grid[i : i + 3]
            ]

            if section == donut_pattern:
                donut_count += 1

    return donut_count


h, w = map(int, input().split())
grid = [input() for _ in range(h)]

print(count_donuts(h, w, grid))
