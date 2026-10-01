# TRON syntax colors for interactive Bash, matching PowerShell's current roles.
bleopt term_true_colors=semicolon
# Keep the change focused on highlighting, without automatic suggestions/menus.
bleopt complete_auto_complete= complete_auto_history= complete_auto_menu=
bleopt complete_ambiguous= complete_menu_complete= complete_menu_filter=
bleopt edit_marker= edit_marker_error=
bleopt highlight_filename= highlight_variable=
bleopt prompt_eol_mark='' exec_errexit_mark='' exec_elapsed_mark='' exec_exit_mark=''
ble-face -s syntax_default 'fg=#D8E1DD'
ble-face -s syntax_command 'fg=#6FC3DF'
ble-face -s syntax_quoted 'fg=#D8E1DD'
ble-face -s syntax_quotation 'fg=#D8E1DD'
ble-face -s syntax_varname 'fg=#D8E1DD'
ble-face -s syntax_param_expansion 'fg=#D8E1DD'
ble-face -s syntax_function_name 'fg=#6FC3DF'
ble-face -s syntax_delimiter 'fg=#8892A0'
ble-face -s syntax_comment 'fg=#667D94'
ble-face -s syntax_error 'fg=#FF6B4A'
ble-face -s syntax_expr 'fg=#FF8C1A'
ble-face -s syntax_escape 'fg=#FF8C1A'
ble-face -s syntax_glob 'fg=#D8E1DD'
ble-face -s syntax_brace 'fg=#8892A0'
ble-face -s syntax_tilde 'fg=#D8E1DD'
ble-face -s syntax_document 'fg=#D8E1DD'
ble-face -s syntax_document_begin 'fg=#8892A0'
ble-face -s argument_option 'fg=#D8E1DD'
ble-face -s command_builtin_dot 'fg=#6FC3DF'
ble-face -s command_builtin 'fg=#6FC3DF'
ble-face -s command_alias 'fg=#6FC3DF'
ble-face -s command_function 'fg=#6FC3DF'
ble-face -s command_file 'fg=#6FC3DF'
ble-face -s command_keyword 'fg=#6FC3DF'
ble-face -s command_jobs 'fg=#6FC3DF'
ble-face -s command_directory 'fg=#6FC3DF'
ble-face -s region 'fg=#D8E1DD,bg=#183C66'
ble-face -s region_match 'fg=#050E14,bg=#FFE600'
ble-face -s auto_complete 'fg=#667D94'
