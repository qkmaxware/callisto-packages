mkdir -p ./files/usr/share/icons ./files/usr/share/licenses/callisto-tela-icon-theme

# Clone icons and build them
git clone --depth=1 https://github.com/vinceliuice/Tela-icon-theme.git src
./src/install.sh -c -d ./src/output -n "Tela (Callisto)"
rm -rf "./src/output/Tela (Callisto)/icon-theme.cache"
rm -rf "./src/output/Tela (Callisto)-dark/icon-theme.cache"
rm -rf "./src/output/Tela (Callisto)-light/icon-theme.cache"

# Copy compiled icons to root for packaging
cp -r src/output/. ./files/usr/share/icons/    # Copies files
cp src/COPYING  ./files/usr/share/licenses/callisto-tela-icon-theme/LICENSE                   # Copies the original license for packaging too
cp README.md    ./files/usr/share/licenses/callisto-tela-icon-theme/NOTICE # Copies the modifications I've made as well as original author credits

# Apply my icon customizations (replace start-here and fedora-logo)
for dir in 'files/usr/share/icons/Tela (Callisto)/32/status/' 'files/usr/share/icons/Tela (Callisto)/24/panel/' 'files/usr/share/icons/Tela (Callisto)/22/panel/' 'files/usr/share/icons/Tela (Callisto)/16/panel/'; do 
    cp -f ../callisto-logos/start-here.svg "$dir"
done
find files/usr/share/icons -type f -name 'fedora-logo.*' -print -exec cp -f ../callisto-logos/callisto-logo.svg {} \;

copy_icon_tree() {
    local src_dir="$1"
    local dest_dir="$2"

    if [ -L "$dest_dir" ]; then
        echo "Skipping symlink target: $dest_dir"
        return 0
    fi

    if [ -e "$dest_dir" ] && [ ! -d "$dest_dir" ]; then
        echo "Skipping non-directory target: $dest_dir"
        return 0
    fi

    mkdir -p "$dest_dir"

    for entry in "$src_dir"/*; do
        [ -e "$entry" ] || continue

        base_name="$(basename "$entry")"
        dest_entry="$dest_dir/$base_name"

        if [ -d "$entry" ]; then
            if [ -L "$dest_entry" ]; then
                echo "Skipping directory symlink target: $dest_entry"
            elif [ -e "$dest_entry" ] && [ ! -d "$dest_entry" ]; then
                echo "Skipping non-directory target: $dest_entry"
            else
                mkdir -p "$dest_entry"
                copy_icon_tree "$entry" "$dest_entry"
            fi
        else
            if [ -e "$dest_entry" ] && [ -d "$dest_entry" ]; then
                echo "Skipping file overwrite into directory target: $dest_entry"
            else
                rm -f "$dest_entry"
                cp -a "$entry" "$dest_entry"
            fi
        fi
    done
}

for theme_dir in \
    'files/usr/share/icons/Tela (Callisto)' \
    'files/usr/share/icons/Tela (Callisto)-dark' \
    'files/usr/share/icons/Tela (Callisto)-light'; do
    while IFS= read -r src_dir; do
        rel_path="${src_dir#icons/}"
        if [ "$rel_path" = "$src_dir" ]; then
            continue
        fi
        copy_icon_tree "$src_dir" "$theme_dir/$rel_path"
    done < <(find icons -mindepth 1 -type d | sort)
done

# Clean broken symlinks
find ./files -xtype l -print -delete
