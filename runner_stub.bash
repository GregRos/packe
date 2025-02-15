my_dir="$(dirname "$0")"
source "$my_dir/utils.bash/source-me.bash"
if [ -n "$PYRUN_PROLOG" ]; then
    source "$PYRUN_PROLOG"
fi
exec > >(
    trap "" INT TERM
    sed "s/^/$PYRUN_PREFIX: /"
)
exec 2> >(
    trap "" INT TERM
    sed "s/^/$PYRUN_PREFIX: /" >&2
)

source "$PYRUN_TARGET"
