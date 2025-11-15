class Color:
    GREEN = "\033[32m"
    RED = "\033[31m"
    YELLOW = "\033[33m"
    CYAN = "\033[36m"
    BOLD = "\033[1m"
    RESET = "\033[0m"

def green(msg):
    return f"{Color.GREEN}{msg}{Color.RESET}"

def red(msg):
    return f"{Color.RED}{msg}{Color.RESET}"

def yellow(msg):
    return f"{Color.YELLOW}{msg}{Color.RESET}"

def cyan(msg):
    return f"{Color.CYAN}{msg}{Color.RESET}"

def bold(msg):
    return f"{Color.BOLD}{msg}{Color.RESET}"
