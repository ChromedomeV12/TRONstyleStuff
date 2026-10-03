# TRON input roles: white text/references, blue commands/keywords, orange numbers/types.
# PowerShell's default directory style uses ANSI blue BACKGROUND (44), which
# hides names when the terminal's foreground is also TRON blue. Use cyan text
# with the terminal's normal background instead. Leave ls aliases untouched.
if ($PSVersionTable.PSVersion -ge [version]'7.2') {
    $PSStyle.FileInfo.Directory = "$([char]27)[49;38;2;0;238;238;1m"
}

if (Get-Module -ListAvailable PSReadLine) {
    Import-Module PSReadLine
    Set-PSReadLineOption -Colors @{
        Default            = '#D8E1DD'
        Command            = '#6FC3DF'
        Keyword            = '#6FC3DF'
        Parameter          = '#D8E1DD'
        Variable           = '#D8E1DD'
        Type               = '#FF8C1A'
        Member             = '#D8E1DD'
        Operator           = '#8892A0'
        ContinuationPrompt = '#6FC3DF'
        String             = '#D8E1DD'
        Number             = '#FF8C1A'
        Comment            = '#667D94'
        InlinePrediction   = '#667D94'
        ListPrediction     = '#667D94'
        Selection          = "$([char]27)[38;2;216;225;221;48;2;24;60;102m"
        ListPredictionSelected = "$([char]27)[38;2;216;225;221;48;2;24;60;102m"
        Emphasis           = '#FFE600'
        Error              = '#FF6B4A'
    }
}
