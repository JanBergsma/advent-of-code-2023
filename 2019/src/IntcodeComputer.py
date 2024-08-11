from math import inf
from typing import Generator


class IntcodeComputer:
    def __init__(self, s: str) -> None:
        self.state = {a: int(i) for a, i in enumerate(s.split(","))}
        self.ip = 0
        self.waiting_for_input = False

    def run(self) -> Generator[int | None, int, None]:
        offset = 0

        while True:
            mode_c, mode_b, mode_a, opcode = self.opcode()

            if opcode == 1:
                c = self.value(mode_c, offset)
                b = self.value(mode_b, offset)
                self.state[self.adress(mode_a, offset)] = c + b
            elif opcode == 2:
                c = self.value(mode_c, offset)
                b = self.value(mode_b, offset)
                self.state[self.adress(mode_a, offset)] = c * b
            elif opcode == 3:
                self.waiting_for_input = True
                f = yield
                self.waiting_for_input = False
                self.state[self.adress(mode_c, offset)] = f
            elif opcode == 4:
                c = self.value(mode_c, offset)
                yield c
            elif opcode == 5:
                c = self.value(mode_c, offset)
                b = self.value(mode_b, offset)
                if c != 0:
                    self.ip = b
            elif opcode == 6:
                c = self.value(mode_c, offset)
                b = self.value(mode_b, offset)
                if c == 0:
                    self.ip = b
            elif opcode == 7:
                c = self.value(mode_c, offset)
                b = self.value(mode_b, offset)
                self.state[self.adress(mode_a, offset)] = 1 if c < b else 0
            elif opcode == 8:
                c = self.value(mode_c, offset)
                b = self.value(mode_b, offset)
                self.state[self.adress(mode_a, offset)] = 1 if c == b else 0
            elif opcode == 9:
                offset += self.value(mode_c, offset)
            elif opcode == 99:
                return
            else:
                raise ValueError(f"1202 program alarm. opcode={opcode}")

    def opcode(self):
        code = self.state[self.ip]
        self.ip += 1
        opcode = code % 100
        code //= 100
        mode_c = code % 10
        code //= 10
        mode_b = code % 10
        code //= 10
        mode_a = code % 10
        return mode_c, mode_b, mode_a, opcode

    def value(self, mode: int, offset: int) -> int:
        adress = self.adress(mode, offset)
        if adress > -1:
            if adress not in self.state:
                self.state[adress] = 0
            return self.state[adress]

        raise ValueError(
            f"Adress should be bigger then 0: adress={self.state[self.ip] + offset}"
        )

    def adress(self, mode: int, offset: int) -> int:
        ip = self.ip
        self.ip += 1

        if mode == 0:
            return self.state[ip]

        if mode == 1:
            return ip

        if mode == 2:
            return self.state[ip] + offset

        raise ValueError(f"Unknown adress mode: mode={mode}")

    def __repr__(self) -> str:
        return ",".join(str(i) for i in self.state)
