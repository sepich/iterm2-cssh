#!/usr/bin/env python3.7
import iterm2
import sys
from math import sqrt, ceil

profile = 'Default'


async def main(connection):
    if len(sys.argv) == 1:
        print('No hosts to connect to found! Usage is:\ni2cssh.py host1 [host2 ...]')
        return
    hosts = sys.argv[1:]
    cols = 3 if len(hosts) <= 3 else ceil(sqrt(len(hosts)))
    app = await iterm2.async_get_app(connection)
    window = app.current_terminal_window

    # create sessions in new tab
    tab = None
    sessions = [None for x in range(cols)]  # sessions to split down
    col = 0
    for host in hosts:
        tmp_profile = iterm2.LocalWriteOnlyProfile()
        tmp_profile.set_use_custom_command('Yes')
        tmp_profile.set_command(f'ssh {host}')
        tmp_profile.set_close_sessions_on_end(False)

        if not tab:  # create new tab first
            tab = await window.async_create_tab(profile=profile, profile_customizations=tmp_profile)
            sessions[col] = tab.current_session
        else:
            if sessions[col]:  # split down
                sessions[col] = await sessions[col].async_split_pane(vertical=False, profile=profile, profile_customizations=tmp_profile)
            else:  # first row, split right
                # https://gitlab.com/gnachman/iterm2/issues/7903
                if not sessions[col-1]:
                    return
                sessions[col] = await sessions[col-1].async_split_pane(vertical=True, profile=profile, profile_customizations=tmp_profile)
        col = (col+1) % cols


    # enable broadcast
    for session in tab.sessions:
        await iterm2.MainMenu.async_select_menu_item(connection, 'Broadcast Input.Broadcast Input to All Panes in Current Tab')


iterm2.run_until_complete(main)
