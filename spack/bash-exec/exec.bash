source "$SPACK_EXEC_DIR/utils.bash/source-me.bash"

exec > >(
    trap "" INT TERM
    sed "s/^/$(sed -e 's/[&\\/]/\\&/g; s/$/\\/' -e '$s/\\$//' <<<"$SPACK_PREFIX")/"
)
exec 2> >(
    trap "" INT TERM
    sed "s/^/$(sed -e 's/[&\\/]/\\&/g; s/$/\\/' -e '$s/\\$//' <<<"$SPACK_PREFIX")/" >&2
)
if [ -n "$SPACK_BEFORE" ]; then
    source "$SPACK_BEFORE"
fi
if [ -z "$SPACK_TARGET" ]; then
    echo.error "SPACK_TARGET is not set"
    exit 1
fi
source "$SPACK_TARGET"
