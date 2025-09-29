source "$PACKE_EXEC_DIR/utils.bash/source-me.bash"

exec > >(
    trap "" INT TERM
    sed "s/^/$(sed -e 's/[&\\/]/\\&/g; s/$/\\/' -e '$s/\\$//' <<<"$PACKE_PREFIX")/"
)
exec 2> >(
    trap "" INT TERM
    sed "s/^/$(sed -e 's/[&\\/]/\\&/g; s/$/\\/' -e '$s/\\$//' <<<"$PACKE_PREFIX")/" >&2
)
if [ -n "$PACKE_BEFORE" ]; then
    source "$PACKE_BEFORE"
fi
if [ -z "$PACKE_TARGET" ]; then
    echo.error "PACKE_TARGET is not set"
    exit 1
fi
source "$PACKE_TARGET"
