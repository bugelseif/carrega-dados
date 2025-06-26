$exclude = @("venv", "carrega-dados.zip")
$files = Get-ChildItem -Path . -Exclude $exclude
Compress-Archive -Path $files -DestinationPath "carrega-dados.zip" -Force