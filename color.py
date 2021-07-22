import sys
import colorama
colorama.init()

from termcolor import colored, cprint

text = colored('Hello, World!', 'red', attrs=['reverse', 'blink'])
print(text)
cprint('Hello, World!', 'green', 'on_red')

print_red_on_cyan = lambda x: cprint(x, 'red', 'on_cyan')
print_red_on_cyan('Hello, World!')
colorama.deinit()

print_red_on_cyan('Hello, Universe!')

for i in range(10):
    cprint(i, 'magenta', end=' ')

cprint("Attention!", 'red', attrs=['bold'], file=sys.stderr)


"""

Text colors:

grey
red
green
yellow
blue
magenta
cyan
white
Text highlights:

on_grey
on_red
on_green
on_yellow
on_blue
on_magenta
on_cyan
on_white
Attributes:

bold
dark
underline
blink
reverse
concealed


"""