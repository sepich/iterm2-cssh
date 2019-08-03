#!/usr/bin/env python3.7
import argparse
import iterm2
from math import sqrt, ceil

profile = 'Default'

parser = argparse.ArgumentParser(description='csshX like tool for iTerm2v3.3 via Python-API')
parser.add_argument('-o', dest='options', help='arguments to be passed to ssh when making the connection')
parser.add_argument('hosts', metavar='[user@]hostname', nargs='+')
args = parser.parse_args()


async def main(connection):
    command = f'ssh -o {args.options}' if args.options else 'ssh'
    cols = 3 if len(args.hosts) <= 3 else ceil(sqrt(len(args.hosts)))
    app = await iterm2.async_get_app(connection)
    window = app.current_terminal_window

    # create sessions in new tab
    tab = None
    sessions = [None for x in range(cols)]  # sessions to split down
    col = 0
    for host in args.hosts:
        tmp_profile = iterm2.LocalWriteOnlyProfile()
        tmp_profile.set_use_custom_command('Yes')
        tmp_profile.set_command(f'{command} {host}')
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
