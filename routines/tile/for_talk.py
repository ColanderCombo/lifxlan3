from typing import List, Dict, Any, Optional, Union

import inspect

from lifxlan import Dir
from routines.cli import info
from routines.morse_code import Morse
from routines.tile.core import animate, translate
from routines.tile.snek import play_snek, auto_play_snek

__author__ = 'acushner'


class Funcs:
    @staticmethod
    def color_info():
        info()

    @staticmethod
    def simulate_morse_code():
        Morse.from_str('copilot').simulate()

    @staticmethod
    def tile_animate():
        animate('./imgs/ff4_tellah.png', sleep_secs=1, in_terminal=True)

    @staticmethod
    def tile_translate():
        translate('./imgs/ff6_sabin.png', split=False, sleep_secs=.1, n_iterations=4, in_terminal=True)

    @staticmethod
    def play_snek():
        play_snek()

    @staticmethod
    def auto_play_snek():
        auto_play_snek()


def __main():
    fns = (fn for fn in vars(Funcs) if not fn.startswith('_'))
    d = {n: fn for n, fn in enumerate(fns)}
    s = '\n'.join(f'{k}: {v}' for k, v in d.items())
    f_num = int(input(f'{s}\n? '))
    getattr(Funcs, d[f_num])()


if __name__ == '__main__':
    __main()
