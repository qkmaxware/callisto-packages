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

# Apply my icon customizations
for dir in 'files/usr/share/icons/Tela (Callisto)/32/status/' 'files/usr/share/icons/Tela (Callisto)/24/panel/' 'files/usr/share/icons/Tela (Callisto)/22/panel/' 'files/usr/share/icons/Tela (Callisto)/16/panel/'; do 
    cp -f ../callisto-logos/start-here.svg "$dir"
done
cp -rf icons/. 'files/usr/share/icons/Tela (Callisto)/'
cp -rf icons/. 'files/usr/share/icons/Tela (Callisto)-dark/'

# Clean broken symlinks
find ./files -xtype l -print -delete
