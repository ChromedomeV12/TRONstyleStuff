# TRON input roles: white text/references, blue commands/keywords, orange numbers/types.
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
