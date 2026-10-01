# BEGIN TRON Bash attach
if [[ ${BLE_VERSION-} ]]; then
  # Existing startup scripts can append Windows paths again.
  if declare -F _tron_filter_path >/dev/null; then
    _tron_filter_path
    unset -f _tron_filter_path
  fi
  ble-attach
fi
# END TRON Bash attach
