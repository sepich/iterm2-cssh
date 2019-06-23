#!/usr/bin/env python3.7
import iterm2
import sys
from math import sqrt, ceil

profile = 'Default'
#shell='/usr/bin/env bash -l'  # if set, each session would also have shell before ssh


async def main(connection):
    # init
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
        if col == cols:
            col = 1
        else:
            col += 1
        if not tab:  # create new tab first
            tab = await window.async_create_tab(profile=profile, command=f'ssh {host}')
            sessions[col-1] = tab.current_session
        else:
            tmp_profile = iterm2.LocalWriteOnlyProfile()
            tmp_profile.set_use_custom_command('Yes')
            tmp_profile.set_command(f'ssh {host}')
            if sessions[col-1]:  # split down
                sessions[col-1] = await sessions[col-1].async_split_pane(vertical=False, profile=profile, profile_customizations=tmp_profile)
            else:  # first row, split right
                try:
                    sessions[col-1] = await sessions[col-2].async_split_pane(vertical=True, profile=profile, profile_customizations=tmp_profile)
                except:
                    await iterm2.MainMenu.async_select_menu_item(connection, "Split Vertically with Current Profile")
                    sessions[col-1] = tab.current_session
                    await tab.current_session.async_send_text(f'ssh {host}\n', suppress_broadcast=True)

    # enable broadcast
    for session in tab.sessions:
        await iterm2.MainMenu.async_select_menu_item(connection, 'Broadcast Input.Broadcast Input to All Panes in Current Tab')


iterm2.run_until_complete(main)
