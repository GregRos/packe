function __add-startup() {
    local name="$1"
    local command="$2"
    local user="$3"
    local home_dir
    home_dir=$(getent passwd "$user" | cut -d: -f6)
    target_path="$home_dir/.config/fish/conf.d/$name.fish"
    echo "$command" >"$target_path"
    chown "$user:$user" "$target_path"
}
function add-startup() {
    local name="$1"
    local command="$2"
    for user in root gr; do
        __add-startup "$name" "$command" "$user"
    done
}
