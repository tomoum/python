#Requires -PSEdition Core

<#
.SYNOPSIS
This script will generate the .env file then launch the python virtual
environment thats used to run scripts.
.DESCRIPTION
.EXAMPLE
.\repo_env.ps1
#>

# Developer Note: This scripts assumes its placed in the root directory of the repo.

if ($env:PIPENV_ACTIVE) {
    Write-Host 'You are already in a pipenv virtual env enter exit to quite' -ForegroundColor Green
    exit 0
}

# Force pipenv to launch in powershell rather than cmd prompt
$Env:PIPENV_SHELL = 'pwsh'
# Force pipenv to create venv in current folder rather than ~\.virtualenvs
$Env:PIPENV_VENV_IN_PROJECT = 1


function Initialize-DotEnvFile {
    Write-Host 'Initializing .env file' -ForegroundColor Green
    $dot_env_file = "$PSScriptRoot\.env"
    if (Test-Path -Path $dot_env_file -PathType Leaf) {
        Remove-Item -Force $dot_env_file -Confirm:$false
    }
    $venv_path = pyenv exec python -m pipenv --venv

    $python_path = 'PYTHONPATH=' + '"' + "$PSScriptRoot;$PSScriptRoot\src\common;$PSScriptRoot\external_dependencies;$venv_path\Lib\site-packages" + '"'
    $python_path = $python_path.Replace(' ', '')
    # Replace all single slash with double
    $python_path = $python_path -replace '\\', '\\'
    $python_path >> $dot_env_file
}

function Start-Main {
    Set-Location $PSScriptRoot
    pipenv sync -d
    Initialize-DotEnvFile
    pipenv shell
}

Start-Main

