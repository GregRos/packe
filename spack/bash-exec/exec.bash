source "$PYRUN_EXEC_DIR/utils.bash/source-me.bash"

exec > >(
    trap "" INT TERM
    sed "s/^/$(sed -e 's/[&\\/]/\\&/g; s/$/\\/' -e '$s/\\$//' <<<"$PYRUN_PREFIX")/"
)
exec 2> >(
    trap "" INT TERM
    sed "s/^/$(sed -e 's/[&\\/]/\\&/g; s/$/\\/' -e '$s/\\$//' <<<"$PYRUN_PREFIX")/" >&2
)
if [ -n "$PYRUN_BEFORE" ]; then
    source "$PYRUN_BEFORE"
fi
if [ -z "$PYRUN_TARGET" ]; then
    echo.error "PYRUN_TARGET is not set"
    exit 1
fi
source "$PYRUN_TARGET"
