# iterm2-cssh
csshX like tool for iTerm2v3.3 via Python-API

## Description
New [Python-API](https://iterm2.com/python-api/) had been added to iTerm2 v3.3. I have many issues with [wouterdebie/i2cssh](https://github.com/wouterdebie/i2cssh), which uses AppleScript, so decided to try fix them via this new API.  
This is a tool to connect to multiple servers in iTerm2 Split-View, and then manage them at once via Broadcasted Input (`Cmd-Shift-I`)

## Install
 - Enable API in iTerm2 Settings:  
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

## Usage
Example of usage is provided in `start.sh`:
 - Configure new default Profile command to run `start.sh`
![Profile](https://habrastorage.org/webt/ay/f9/mb/ayf9mbu631fwf8dswip-fgyaq1i.png)
 - Press `Cmd-T` to open new tab, it would display all your servers from `.ssh/known_hosts`
 - You then interactively (via `fzf`) filter the list and select items to connect to:  
![](https://habrastorage.org/webt/fq/h1/ps/fqh1psnorl-focnqgnpttayclfk.png)
 - If single item is selected - connection opened in current tab
 - If there no such name yet in your `.ssh/known_hosts`, you can type it in and press `Enter` to connect
 - If multiple is selected (via `Tab`), new tab would be created with Split-Screen and broadcast input activated  
   ![](https://habrastorage.org/webt/ri/3-/a6/ri3-a69i00rvooznebkz6mbep8y.png)  
   For sessions inside Split-Screen it also sets `Session > After a session ends > No action` so that you can press `Right click > Restart` if single session is dropped, without reopening whole set.