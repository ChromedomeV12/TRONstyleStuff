# Initialize one prompt engine; preserve ble.sh and its existing attach order.
# Launch a new fallback shell with: TRON_PROMPT=starship bash
if [[ ${TRON_PROMPT-omp} != starship && -x $HOME/.local/bin/oh-my-posh && -r $HOME/.config/oh-my-posh/TRON.omp.json ]]; then
  eval "$("$HOME/.local/bin/oh-my-posh" init bash --config "$HOME/.config/oh-my-posh/TRON.omp.json")"
elif command -v starship >/dev/null 2>&1; then
  eval "$(starship init bash)"
fi
