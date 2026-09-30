X, Y, Z = (int(x) for x in input().split())

for a in range(-1, 8):
    for b in range(-1, 8):
        for c in range(-1, 8):
            for d in range(-1, 8):
                for e in range(-1, 8):
                    for f in range(-1, 8):
                        c3 = (
                            max(min(7, a + 7, d + 7) - max(0, a, d), 0)
                            * max(min(7, b + 7, e + 7) - max(0, b, e), 0)
                            * max(min(7, c + 7, f + 7) - max(0, c, f), 0)
                        )
                        c2 = (
                            max(min(7, a + 7) - max(0, a), 0)
                            * max(min(7, b + 7) - max(0, b), 0)
                            * max(min(7, c + 7) - max(0, c), 0)
                        ) + (
                            max(min(7, d + 7) - max(0, d), 0)
                            * max(min(7, e + 7) - max(0, e), 0)
                            * max(min(7, f + 7) - max(0, f), 0)
                        ) + (
                            max(min(a + 7, d + 7) - max(a, d), 0)
                            * max(min(b + 7, e + 7) - max(b, e), 0)
                            * max(min(c + 7, f + 7) - max(c, f), 0)
                        ) - c3 * 3
                        c1 = 7 * 7 * 7 * 3 - c2 * 2 - c3 * 3
                        if c1 == X and c2 == Y and c3 == Z:
                            print("Yes")
                            print(0, 0, 0, a, b, c, d, e, f)
                            exit()

print("No")
