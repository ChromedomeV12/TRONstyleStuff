# BEGIN TRON remote Bash highlighting
# Load before prompt/key-binding initialization; attach at the end of .bashrc.
# Skip for a session with: TRON_BASH_HIGHLIGHT=0 bash
if [[ $- == *i* && -t 0 && -t 1 && ${TERM-} != dumb && ${TRON_BASH_HIGHLIGHT-1} != 0 && ! ${BLE_VERSION-} ]] &&
   [[ -r $HOME/.local/share/tron-blesh/ble-nightly/ble.sh && -r $HOME/.config/tron/blesh-init.sh ]]; then
  source "$HOME/.local/share/tron-blesh/ble-nightly/ble.sh" --attach=none --rcfile "$HOME/.config/tron/blesh-init.sh"
fi
# END TRON remote Bash highlighting
