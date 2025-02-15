#!/bin/bash
export c_reset_=$'\e[0m'
c_out_char() (
    set +x
    printf "❱❱"
)
echo.white() (
    set +x
    local white=$'\e[0;97m'
    echo "$white""$*""$c_reset_"
)
echo.red() (
    set +x
    local red=$'\e[0;91m'

    echo "$red""$*""$c_reset_"
)
echo.green() (
    set +x
    local green=$'\e[0;92m'

    echo "$green""$*""$c_reset_"
)
echo.yellow() (
    set +x
    local yellow=$'\e[0;93m'

    echo "$yellow""$*""$c_reset_"
)
echo.blue() (
    set +x
    local blue=$'\e[1;34m'
    echo "$blue""$*""$c_reset_"
)
echo.info() (
    set +x

    echo.green "🟩" "$(c_out_char)" "$*"
)
echo.warn() (
    set +x

    echo.yellow "🟨" "$(c_out_char)" "$*"
)
echo.error() (
    set +x

    echo.red "🟥" "$(c_out_char)" "$*"
)
echo.section() (
    set +x
    local caption="$*"
    local heading="🟦 $(c_out_char) $caption"
    export heading
    local chars="$(echo "$heading" | wc -c)"
    local line="$(printf '═%.0s' $(seq 1 "$chars"))"
    echo
    echo.white "$heading"
    echo.white "$line"
)
