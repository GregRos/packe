source "$PYRUN_EXEC_DIR/utils.bash/source-me.bash"
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

if [ -z "$PYRUN_TARGET" ]; then
    echo.error "PYRUN_TARGET is not set"
    exit 1
fi
source "$PYRUN_TARGET"
