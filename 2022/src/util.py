def print_hex(hex: str, text: str, end="\n") -> None:
    r, g, b = tuple(int(hex[1:][i : i + 2], 16) for i in (0, 2, 4))
    escape = "\033[{};2;{};{};{}m".format(38, r, g, b)
    print(escape + text + "\033[0m", end=end)


def hexcolor_str(hex: str, text: str) -> str:
    r, g, b = tuple(int(hex[1:][i : i + 2], 16) for i in (0, 2, 4))
    escape = "\033[{};2;{};{};{}m".format(38, r, g, b)
    return escape + text + "\033[0m"
