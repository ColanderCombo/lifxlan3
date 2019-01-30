from contextlib import suppress
from functools import lru_cache
from math import ceil
from pprint import pprint
from time import sleep
from typing import Optional, Dict

from lifxlan import TileChain, LifxLAN, Color, Colors, cycle, init_log, timer
from routines.tile.tile_utils import ColorMatrix, default_shape, tile_map, RC, default_color

__author__ = 'acushner'

log = init_log(__name__)


@lru_cache()
def get_tile_chain() -> Optional[TileChain]:
    with suppress(IndexError):
        lifx = LifxLAN()
        return lifx.tilechain_lights[0]


def _cm_test(c: Color) -> ColorMatrix:
    cm = ColorMatrix.from_shape(default_shape)
    cm[0, 0] = cm[0, 1] = cm[1, 0] = cm[1, 1] = c
    return cm


def id_tiles(tc: TileChain, rotate=False):
    """set tiles to different colors in the corner to ID tile"""
    colors = 'MAGENTA', 'YELLOW', 'YALE_BLUE', 'GREEN', 'BROWN'
    for ti in tile_map.values():
        name = colors[ti.idx]
        print(ti.idx, name)
        cm = _cm_test(Colors[name])
        if rotate:
            cm = cm.rotate_from_origin(ti.origin)
        tc.set_tile_colors(ti.idx, cm.flattened)


# interactive

_color_replacements: Dict[str, Dict[Color, Color]] = dict(
    crono={Color(hue=54612, saturation=65535, brightness=65535, kelvin=3200): Colors.OFF},
    ff6={Color(hue=32767, saturation=65535, brightness=32896, kelvin=3200): Colors.OFF},
    ff4={Color(hue=32767, saturation=65535, brightness=65535, kelvin=3200): Colors.OFF},
    mario_kart={Color(hue=21845, saturation=48059, brightness=65535, kelvin=3200): Colors.OFF},
    lttp={Color(hue=32767, saturation=65535, brightness=16448, kelvin=3200): Colors.OFF,
          Color(hue=32767, saturation=65535, brightness=32896, kelvin=3200): Colors.OFF})


def _get_color_replacements(filename):
    for k, v in _color_replacements.items():
        if k in filename:
            return v
    return {}


def animate(filename: str, *, center: bool = False, sleep_secs: float = .75, in_terminal=False, size=RC(16, 16)):
    """split color matrix and change images every `sleep_secs` seconds"""
    cm = ColorMatrix.from_filename(filename)
    color_map = _get_color_replacements(filename)
    for i, cm in enumerate(cycle(cm.split())):
        log.info('.')
        c_offset = 0 if not center else max(0, ceil(cm.width / 2 - 8))
        cm.replace(color_map)
        set_cm(cm, offset=RC(0, c_offset), size=size, in_terminal=in_terminal)
        sleep(sleep_secs)


def translate(filename: str, *, sleep_secs: float = .5, in_terminal=False, size=RC(16, 16)):
    """move right"""
    cm = ColorMatrix.from_filename(filename)
    color_map = _get_color_replacements(filename)
    cm = cm.split()[0]

    def _gen_offset():
        while True:
            for _c_offset in range(size.c * 2):
                yield size.c - _c_offset - 1

    for c_offset in _gen_offset():
        cm.replace(color_map)
        cm.wrap = True
        set_cm(cm, offset=RC(0, c_offset), size=size, in_terminal=in_terminal)
        sleep(sleep_secs)


@timer
def set_cm(cm: ColorMatrix, offset=RC(0, 0), size=RC(16, 16), in_terminal=False, with_mini=True):
    orig_cm = cm = cm.strip().get_range(RC(0, 0) + offset, size + offset)
    if in_terminal:
        print(cm.color_str)
        print(cm.describe)
        print(cm.resize().color_str)
        print(cm.resize((4, 4)).color_str)
        return

    cm.set_max_brightness_pct(60)
    tiles = cm.to_tiles()

    idx_colors_map = {}
    for t_idx, cm in tiles.items():
        t_info = tile_map[t_idx]
        cm.replace({default_color: Color(1, 1, 100, 9000)})
        idx_colors_map[t_info.idx] = cm.flattened

    if with_mini:
        idx_colors_map[tile_map[RC(2, -1)].idx] = orig_cm.resize((8, 8)).flattened

    tc = get_tile_chain()
    tc.set_tilechain_colors(idx_colors_map)
    # _cmp_colors(idx_colors_map)


def _cmp_colors(idx_colors_map):
    from itertools import starmap
    tc = get_tile_chain()
    lights = {idx: list(starmap(Color, tc.get_tile_colors(idx).colors)) for idx in idx_colors_map}

    here_there = {k: set(idx_colors_map[k]) - set(lights[k])
                  for k in idx_colors_map}
    there_here = {k: set(lights[k]) - set(idx_colors_map[k])
                  for k in idx_colors_map}

    print('here - there')
    pprint(here_there)
    print()
    print('there - here')
    pprint(there_here)
    print()


images = [
    'crono.png',
    'crono_magus.png',
    'ff4_cecil.png',
    'ff4_rydia.png',
    'ff4_tellah.png',
    'ff6_edgar.png',
    'ff6_locke.png',
    'ff6_locke_full.png',
    'ff6_sabin.png',
    'link.png',
    'link_all.png',
    'lttp_link.png',
    'maniac_bernard.png',
    'maniac_heads.png',
    'mario.png',
    'mario_kart_koopa.png',
    'mm.png',
    'mm_walk.png',
    'm_small.png',
    'punch_out_lm.png',
    'punch_out_mike.png',
    'zelda_blue_octorock.png',
    'zelda_enemies.png',
    'zelda_ghosts.png',
    'zelda_red_octorock.png']


def __main():
    # return id_tiles(get_tile_chain(), rotate=True)
    return translate('./imgs/link_all.png', in_terminal=True)
    return animate('./imgs/maniac_bernard.png')


if __name__ == '__main__':
    __main()
