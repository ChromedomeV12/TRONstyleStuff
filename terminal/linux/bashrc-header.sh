# BEGIN TRON Bash highlighting
# Skip with: TRON_BASH_HIGHLIGHT=0 bash
if [[ $- == *i* && -t 0 && -t 1 && ${TERM-} != dumb && ${TRON_BASH_HIGHLIGHT-1} != 0 && ! ${BLE_VERSION-} ]] &&
   [[ -r $HOME/.local/share/tron-blesh/ble-nightly/ble.sh && -r $HOME/.config/tron/blesh-init.sh ]]; then
  # Windows executable discovery is slow in WSL. Keep all Linux PATH entries;
  # Windows files remain accessible by their /mnt paths.
  _tron_filter_path() {
    local entry remaining=$PATH filtered= separator=
    while :; do
      entry=${remaining%%:*}
      case $entry in
        /mnt/[a-z]/*) ;;
        *) filtered+=$separator$entry; separator=: ;;
      esac
      [[ $remaining == *:* ]] || break
      remaining=${remaining#*:}
    done
    export PATH=$filtered
  }
  _tron_filter_path
  source "$HOME/.local/share/tron-blesh/ble-nightly/ble.sh" --attach=none --rcfile "$HOME/.config/tron/blesh-init.sh"
fi
# END TRON Bash highlighting
