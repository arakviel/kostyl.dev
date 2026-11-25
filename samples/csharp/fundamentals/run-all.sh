#!/usr/bin/env bash
# Перезапускає всі file-based приклади лекцій fundamentals і друкує їхній вивід.
# Використання: ./run-all.sh [папка-лекції]   (напр. ./run-all.sh 01-dotnet-platform)
# DOTNET можна перевизначити: DOTNET=/шлях/до/dotnet ./run-all.sh
set -u
cd "$(dirname "$0")"
DOTNET="${DOTNET:-$HOME/.local/share/mise/installs/dotnet/10.0.404/dotnet}"
export DOTNET_CLI_TELEMETRY_OPTOUT=1 DOTNET_NOLOGO=1
# без фонових процесів MSBuild/компілятора, інакше вивід скрипта може «зависнути»
export MSBUILDDISABLENODEREUSE=1 DOTNET_CLI_USE_MSBUILD_SERVER=0 UseSharedCompilation=false
for dir in ${1:-[0-9][0-9]-*}; do
  for file in "$dir"/*.cs "$dir"/tasks/*.cs "$dir"/practice/*.cs; do
    [ -e "$file" ] || continue
    echo "=== $file"
    (cd "$(dirname "$file")" && "$DOTNET" run "$(basename "$file")" 2>&1)
  done
done
