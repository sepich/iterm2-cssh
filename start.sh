#!/bin/bash
PATH=/usr/local/bin:$PATH
if ! which fzf &>/dev/null; then
  echo "Please install fzf first"
  exit 1
fi

res=`cat ~/.ssh/known_hosts | tr ',' ' ' | awk '{gsub(/\]|\[/,"",$1); print $1}' | sort -u | fzf -m --reverse --print-query --exact --no-mouse`
if [ $? -gt 1 ]; then bash --login; exit; fi #ESC pressed - local session
q=`echo "$res" | head -1`
c=`echo "$res" | tail -n +2`

# empty choice, try query
if [ -n "$q" -a -z "$c" ]; then
  ssh "$q"
# single choice
elif [ `echo "$c" | wc -l` == 1 ]; then
  h=`echo "$c" | cut -d. -f1`
  echo -ne "\033]1;$h\a"
  if echo "$c" | grep -q :; then
    h=`echo "$c" | cut -d: -f1`
    p=`echo "$c" | cut -d: -f2`
    ssh -p $p $h
  else
    ssh "$c"
  fi
# multichoice
else
  python=`ls /Users/aryabov/Library/ApplicationSupport/iTerm2/iterm2env/versions/*/bin/python | cut -d' ' -f1`
  dir=`dirname "${BASH_SOURCE[0]}"`
  $python "$dir"/i2cssh.py $c || sleep 60
fi
