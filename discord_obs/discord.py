import logging
from xdo import Xdo

from discord_obs.configuration import DISCORD_BUTTON_POS_Y, DISCORD_BUTTON_POS_X, DISCORD_BUTTON_COLOR_ACTIVATED, \
    DISCORD_BUTTON_COLOR_DEACTIVATED
from discord_obs.process import process_exec

logging.basicConfig(level=logging.DEBUG)


def set_discord_webcam(activate):
    xdo = Xdo()
    current_mouse_location = xdo.get_mouse_location()
    current_window = xdo.get_active_window()
    discord_window = xdo.search_windows(winname=b' - Discord$')
    xdo.activate_window(discord_window[0])

    xdo.move_mouse(0, 0, 0)
    import_result = process_exec([
        '/usr/bin/import',
        '-silent',
        '-window',
        'root',
        '-depth',
        '4',
        '-crop',
        '1x1+%s+%s' % (DISCORD_BUTTON_POS_X, DISCORD_BUTTON_POS_Y),
        'txt:-'
    ]).split("\n")
    button_color = import_result[1].replace('  ', ' ').split(' ')[2]

    if button_color == DISCORD_BUTTON_COLOR_DEACTIVATED and activate:
        logging.info('discord click activate webcam')
        xdo.move_mouse(DISCORD_BUTTON_POS_X, DISCORD_BUTTON_POS_Y, 0)
        xdo.click_window(discord_window[0], 1)
    if button_color == DISCORD_BUTTON_COLOR_ACTIVATED and not activate:
        logging.info('discord click deactivate webcam')
        xdo.move_mouse(DISCORD_BUTTON_POS_X, DISCORD_BUTTON_POS_Y, 0)
        xdo.click_window(discord_window[0], 1)
    xdo.activate_window(current_window)
    xdo.move_mouse(current_mouse_location.x, current_mouse_location.y, current_mouse_location.screen_num)
