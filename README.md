# iterm2-cssh
cssh like tool for iTerm2 via v3.3 Python-API

## Description
New [Python-API](https://iterm2.com/python-api/) had been added to iTerm2 v3.3. I have many issues with [wouterdebie/i2cssh](https://github.com/wouterdebie/i2cssh) so decided to try out this new API.  
This a tool to connect to multiple servers in iTerm2 Split-View, and then manage them at once via Broadcasted Input (`Cmd-Shift-I`).   
For example you can use `start.sh` in your iterm Profile for new sessions, which displays all your servers from `.ssh/known_hosts`. You then interactively (via `fzf`) filter the list and select multiple to connect to (via `Tab`), then press `Enter` and new tab would be created in iTerm2 with all the servers selected, and broadcast input activated.

## Install
 - Enable API in iTerm2 at:  
`General > Magic > Enable Python API`
 - Install runtime:  
`Menu Scripts > Manage > Download runtime`
 - Clone repo
```bash
git clone https://github.com/sepich/iterm2-cssh.git
cd iterm2-cssh
python=`ls /Users/aryabov/Library/ApplicationSupport/iTerm2/iterm2env/versions/*/bin/python | cut -d' ' -f1`
$python i2cssh.py host1 [host2 ...]
```