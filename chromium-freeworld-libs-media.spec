# These spec file includes some tips and patches thanks to:
#  [1] https://www.archlinux.org/packages/extra/x86_64/chromium/
#  [2] https://packages.gentoo.org/packages/www-client/chromium
#  [3] https://build.opensuse.org/package/show/openSUSE:Factory/chromium
#  [4] https://pkgs.fedoraproject.org/cgit/rpms/chromium.git 
#  [5] http://copr-dist-git.fedorainfracloud.org/cgit/lantw44/chromium/chromium.git
#  [6] https://salsa.debian.org/chromium-team/chromium/tree/master/debian
#  [7] http://www.linuxfromscratch.org/blfs/view/cvs/xsoft/chromium.html
#  [8] https://aur.archlinux.org/packages/chromium-gtk2/
#  [9] https://github.com/RussianFedora/chromium/


%global chromiumdir %{_libdir}/chromium
%global crd_path %{_libdir}/chrome-remote-desktop
# Do not check any ffmpeg or libmedia bundle files in libdir for requires
%global __requires_exclude_from ^%{chromiumdir}/libffmpeg.*$
%global __requires_exclude_from ^%{chromiumdir}/libmedia.*$

#
# Get the version number of latest stable version
# $ curl -s 'https://omahaproxy.appspot.com/all?os=linux&channel=stable' | sed 1d | cut -d , -f 3
%bcond_with normalsource

%global debug_package %{nil}

# vpx
%bcond_with system_libvpx

# clang is necessary for a fast build
%bcond_without clang
# 
%if 0%{?fedora} <= 27
%bcond_without clang_bundle
%else
%bcond_with clang_bundle
%endif

# jinja conditional
%if 0%{?fedora} < 26
%bcond_without system_jinja2
%else
%bcond_with system_jinja2
%endif

# markupsafe
%bcond_with system_markupsafe


# https://github.com/dabeaz/ply/issues/66
%if 0%{?fedora} >= 24
%bcond_without system_ply
%else
%bcond_with system_ply
%endif

# Require libxml2 > 2.9.4 for XML_PARSE_NOXXE
%if 0%{?fedora} >= 27
%bcond_without system_libxml2
%else
%bcond_with system_libxml2
%endif

# Require harfbuzz >= 1.5.0 for hb_glyph_info_t
%bcond_with system_harfbuzz

# Allow testing whether icu can be unbundled
%bcond_with system_libicu

# Allow disabling unconditional build dependency on clang
%bcond_without require_clang

# Gtk conditional
%bcond_without _gtk3

# In UnitedRPMs, we have openh264
%bcond_without system_openh264

# Now is easy to use the external ffmpeg...
%bcond_with system_ffmpeg

# Jumbo / Unity builds
# https://chromium.googlesource.com/chromium/src/+/lkcr/docs/jumbo.md
%bcond_without jumbo_unity

# Vaapi conditional
%bcond_with vaapi

# Generally the .spec file is the same of our chromium-freeworld, building only ffmpeg; then we will obtain all possible codecs.

Name:       chromium-freeworld-libs-media
Version:    68.0.3440.75
Release:    7%{?dist}
Summary:    Chromium media libraries built with all possible codecs

Group:      Applications/Internet
License:    BSD and LGPLv2+
URL:        https://www.chromium.org
Vendor:     URPMS

%if %{with normalsource}
Source0:    https://commondatastorage.googleapis.com/chromium-browser-official/chromium-%{version}.tar.xz
%endif
Source1:    chromium-latest.py
Source997:  https://github.com/UnitedRPMs/chromium-freeworld/raw/master/depot_tools.tar.xz
Source998:  https://github.com/UnitedRPMs/chromium-freeworld/raw/master/gn-binaries.tar.xz

# The following two source files are copied and modified from
# https://repos.fedorapeople.org/repos/spot/chromium/
Source10:   chromium-wrapper.txt
Source11:   chromium-freeworld.desktop

# The following two source files are copied verbatim from
# http://pkgs.fedoraproject.org/cgit/rpms/chromium.git/tree/
Source12:   chromium-freeworld.xml
Source13:   chromium-freeworld.appdata.xml

# Unpackaged fonts
Source15:	https://fontlibrary.org/assets/downloads/gelasio/4d610887ff4d445cbc639aae7828d139/gelasio.zip
Source16:	http://download.savannah.nongnu.org/releases/freebangfont/MuktiNarrow-0.94.tar.bz2
Source17:	https://chromium.googlesource.com/chromium/src.git/+archive/refs/heads/master/third_party/test_fonts.tar.gz
Source18:	https://github.com/web-platform-tests/wpt/raw/master/fonts/Ahem.ttf
Source19:	https://chromium.googlesource.com/chromium/src/+archive/66.0.3359.158/third_party/gardiner_mod.tar.gz

# Add a patch from Fedora to fix GN build
# https://src.fedoraproject.org/cgit/rpms/chromium.git/commit/?id=0df9641
Patch:    chromium-last-commit-position.patch

Patch1:   llvm-fix.patch

# Thanks openSuse
Patch2:    chromium-prop-codecs.patch
Patch3:    chromium-non-void-return.patch

# Thanks Debian
# Fix warnings
Patch4:    comment.patch   
Patch5:    enum-boolean.patch		
Patch6:    unused-typedefs.patch
# Fix gn
Patch7:    buildflags.patch
Patch8:    narrowing.patch
# fixes
Patch09:   optimize.patch
Patch10:   gpu-timeout.patch
Patch11:   namespace.patch
Patch12:   ambiguous-aliases.patch
#Patch14:   mojo.patch
Patch13:   dma.patch
Patch14:   widevine-allow-on-linux.patch

# Thanks Gentoo
Patch15:   chromium-ffmpeg-r1.patch
Patch16:   chromium-libwebp-shim-r0.patch
Patch17:   chromium-cors-string-r0.patch
Patch18:   chromium-libjpeg-r0.patch
# Thanks Intel
%if %{with vaapi}
Patch19:   vaapi.patch
%endif

ExclusiveArch: i686 x86_64 armv7l

# Make sure we don't encounter GCC 5.1 bug
%if 0%{?fedora} >= 22
BuildRequires: gcc >= 5.1.1-2
%endif

%if %{with clang} || %{with require_clang} 
BuildRequires: clang 
BuildRequires: llvm 
%endif
# Basic tools and libraries
BuildRequires: ninja-build, bison, gperf, hwdata
BuildRequires: libgcc(x86-32), glibc(x86-32), libatomic
BuildRequires: libcap-devel, cups-devel, minizip-devel, alsa-lib-devel
BuildRequires: pkgconfig(libexif), pkgconfig(nss)
%if %{with _gtk3}
BuildRequires: pkgconfig(gtk+-3.0)
%else
BuildRequires: pkgconfig(gtk+-2.0)
%endif
BuildRequires: python2-devel
BuildRequires: pkgconfig(xtst), pkgconfig(xscrnsaver)
BuildRequires: pkgconfig(dbus-1), pkgconfig(libudev)
BuildRequires: pkgconfig(gnome-keyring-1)
BuildRequires: pkgconfig(libffi)
# remove_bundled_libraries.py --do-remove
BuildRequires: python2-rpm-macros
BuildRequires: python-beautifulsoup4
BuildRequires: python-html5lib
%if %{with system_jinja2}
%if 0%{?fedora} >= 24
BuildRequires: python2-jinja2
%else
BuildRequires: python-jinja2
%endif
%endif

%if %{with system_markupsafe}
%if 0%{?fedora} >= 26
BuildRequires: python2-markupsafe
%else
BuildRequires: python-markupsafe
%endif
%endif

%if %{with system_ply}
BuildRequires: python2-ply
%endif
# replace_gn_files.py --system-libraries
BuildRequires: flac-devel
%if %{with system_harfbuzz}
BuildRequires: harfbuzz-devel
%endif
BuildRequires: libjpeg-turbo-devel
BuildRequires: libpng-devel
# Chromium requires libvpx 1.5.0 and some non-default options
%if %{with system_libvpx}
BuildRequires: libvpx-devel
%endif
BuildRequires: libwebp-devel
BuildRequires: pkgconfig(libxslt)
BuildRequires: opus-devel
%if %{with system_libxml2}
BuildRequires: pkgconfig(libxml-2.0)
%endif
BuildRequires: re2-devel
%if %{with system_openh264}
BuildRequires: openh264-devel
%endif
BuildRequires: snappy-devel
BuildRequires: yasm
BuildRequires: zlib-devel
# use_*
BuildRequires: pciutils-devel
BuildRequires: speech-dispatcher-devel
BuildRequires: pulseaudio-libs-devel
# Only for non-normal source
BuildRequires: wget
# install desktop files
BuildRequires: desktop-file-utils
# CLANG
%if %{with clang}
BuildRequires: clang
%endif
# markupsafe missed
BuildRequires: git
BuildRequires: nodejs
BuildRequires: libdrm-devel
BuildRequires: mesa-libGL-devel
BuildRequires: mesa-libEGL-devel
# vulcan
BuildRequires: vulkan-devel
%if %{with system_libicu}
BuildRequires: libicu-devel
%endif

%if %{with vaapi}
BuildRequires:	libva-devel 
%endif
BuildRequires:  pkgconfig(libtcmalloc)
#unbundle fontconfig avoid fails in start
BuildRequires:	fontconfig-devel
# fonts
BuildRequires:	google-croscore-arimo-fonts
BuildRequires:	google-croscore-cousine-fonts
BuildRequires:	dejavu-sans-fonts
BuildRequires:	thai-scalable-garuda-fonts
BuildRequires:	lohit-devanagari-fonts
BuildRequires:	lohit-gurmukhi-fonts
BuildRequires:	lohit-tamil-fonts
%if 0%{?fedora} >= 27
BuildRequires:	google-noto-sans-cjk-jp-fonts
BuildRequires:	google-noto-sans-khmer-fonts
BuildRequires:	google-croscore-tinos-fonts
%endif
BuildRequires:	subversion

Provides: %{name}%{_isa} = %{version}-%{release}
Provides: libffmpeg.so()(64bit)
Provides: chromium-libs-media-freeworld = %{version}

%description 
Chromium media libraries built with all possible codecs. Chromium is an
open-source web browser, powered by WebKit (Blink). This package replaces
the default chromium-libs-media package, which is limited in what it
can include.


%prep
%if %{with normalsource}
%autosetup -n chromium-%{version} -p1
%else
wget -c https://commondatastorage.googleapis.com/chromium-browser-official/chromium-%{version}.tar.xz
tar xJf %{_builddir}/chromium-%{version}.tar.xz -C %{_builddir}
%autosetup -T -D -n chromium-%{version} -p1
%endif

# fix debugedit: canonicalization unexpectedly shrank by one character
#sed -i 's@gpu//@gpu/@g' content/renderer/gpu/compositor_forwarding_message_filter.cc
sed -i 's@audio_processing//@audio_processing/@g' third_party/webrtc/modules/audio_processing/utility/ooura_fft.cc
sed -i 's@audio_processing//@audio_processing/@g' third_party/webrtc/modules/audio_processing/utility/ooura_fft_sse2.cc

# Render fix
sed -i 's|public Path,|public blink::Path,|g' third_party/blink/renderer/platform/graphics/path.h

%if %{with clang_bundle}
wget -c http://releases.llvm.org/6.0.0/clang+llvm-6.0.0-x86_64-linux-gnu-Fedora27.tar.xz
tar xJf clang+llvm-6.0.0-x86_64-linux-gnu-Fedora27.tar.xz -C %{_builddir} 
pushd %{_builddir}
mv -f clang+llvm-6.0.0-x86_64-linux-gnu-Fedora27 buclang
popd
%endif

# Unpack fonts
# Chromium why does not include it?
rm -rf third_party/test_fonts
mkdir -p third_party/test_fonts/test_fonts
tar xmzvf %{S:17} -C third_party/test_fonts
tar xmzvf %{S:19} -C third_party/test_fonts/test_fonts
pushd third_party/test_fonts/test_fonts
unzip %{S:15}
tar xf %{S:16}
mv MuktiNarrow0.94/MuktiNarrow.ttf .
rm -rf MuktiNarrow0.94
rm -f *.html *.txt
cp -a /usr/share/fonts/dejavu/DejaVuSans.ttf /usr/share/fonts/dejavu/DejaVuSans-Bold.ttf .
cp -a /usr/share/fonts/thai-scalable/Garuda.ttf .
cp -a /usr/share/fonts/lohit-devanagari/Lohit-Devanagari.ttf /usr/share/fonts/lohit-gurmukhi/Lohit-Gurmukhi.ttf /usr/share/fonts/lohit-tamil/Lohit-Tamil.ttf .
cp -a /usr/share/fonts/google-noto-cjk/NotoSansCJKjp-Regular.otf /usr/share/fonts/google-noto/NotoSansKhmer-Regular.ttf .
cp -a /usr/share/fonts/google-croscore/Tinos-*.ttf .
cp -f %{S:18} .
svn checkout https://github.com/google/fonts/trunk/apache/arimo . && rm -rf .svn 
rm -f *.html && rm -f *.txt
svn checkout https://github.com/google/fonts/trunk/apache/cousine . && rm -rf .svn
popd
#

tar xJf %{S:998} -C %{_builddir}
tar xJf %{S:997} -C %{_builddir}

%if %{with system_markupsafe}
pushd third_party/
rm -rf markupsafe/
ln -sf %{python2_sitearch}/markupsafe/ markupsafe
popd
%else
pushd third_party
rm -rf markupsafe/
git clone --depth 1 https://github.com/pallets/markupsafe.git 
cp -f $PWD/markupsafe/markupsafe/*.py $PWD/markupsafe/
cp -f $PWD/markupsafe/markupsafe/*.c $PWD/markupsafe/
popd
%endif

# node fix
mkdir -p third_party/node/linux/node-linux-x64/bin/
pushd third_party/node/linux/node-linux-x64/bin/
rm -f node
ln -sf /usr/bin/node node
popd

# https://groups.google.com/a/chromium.org/d/msg/chromium-packagers/wuInaKJkosg/kMfIV_7wDgAJ
#rm -rf third_party/freetype/src
#git clone https://chromium.googlesource.com/chromium/src/third_party/freetype2 third_party/freetype/src 

# xlocale.h is gone in F26/RAWHIDE
sed -r -i 's/xlocale.h/locale.h/' buildtools/third_party/libc++/trunk/include/__locale

# https://fedoraproject.org/wiki/Changes/Avoid_usr_bin_python_in_RPM_Build#Quick_Opt-Out
export PYTHON_DISALLOW_AMBIGUOUS_VERSION=0

### build with widevine support

# Patch from crbug (chromium bugtracker)
# fix the missing define (if not, fail build) (need upstream fix) (https://crbug.com/473866)
sed '14i#define WIDEVINE_CDM_VERSION_STRING "Something fresh"' -i "third_party/widevine/cdm/stub/widevine_cdm_version.h"

# Allow building against system libraries in official builds
  sed -i 's/OFFICIAL_BUILD/GOOGLE_CHROME_BUILD/' \
    tools/generate_shim_headers/generate_shim_headers.py

# Work around broken screen sharing in Google Meet
  # https://crbug.com/829916#c16
  sed -i 's/"Chromium/"Chrome/' chrome/common/chrome_content_client_constants.cc

python2 build/linux/unbundle/remove_bundled_libraries.py --do-remove \
    buildtools/third_party/libc++ \
buildtools/third_party/libc++abi \
%if !%{with system_libicu}
    third_party/icu \
    base/third_party/icu/ \
%endif
    base/third_party/dmg_fp \
    base/third_party/dynamic_annotations \
    base/third_party/libevent \
    base/third_party/nspr \
    base/third_party/superfasthash \
    base/third_party/symbolize \
    base/third_party/valgrind \
    base/third_party/xdg_mime \
    base/third_party/xdg_user_dirs \
    chrome/third_party/mozilla_security_manager \
    courgette/third_party \
    native_client/src/third_party/dlmalloc \
    native_client/src/third_party/valgrind \
    net/third_party/http2 \
    net/third_party/mozilla_security_manager \
    net/third_party/nss \
    net/third_party/quic \
    net/third_party/spdy \
    third_party/node \
    third_party/adobe \
    third_party/analytics \
    third_party/swiftshader \
    third_party/swiftshader/third_party/subzero \
    third_party/swiftshader/third_party/llvm-subzero \
    third_party/angle \
    third_party/angle/src/common/third_party/base \
    third_party/angle/src/common/third_party/smhasher \
    third_party/angle/src/third_party/compiler \
    third_party/angle/src/third_party/libXNVCtrl \
    third_party/angle/src/third_party/trace_event \
    third_party/angle/third_party/glslang \
    third_party/angle/third_party/spirv-headers \
    third_party/boringssl \
    third_party/boringssl/src/third_party/fiat \
    third_party/blink \
    third_party/apple_apsl \
    third_party/breakpad \
    third_party/breakpad/breakpad/src/third_party/curl \
    third_party/brotli \
    third_party/cacheinvalidation \
    third_party/catapult \
    third_party/catapult/common/py_vulcanize/third_party/rcssmin  \
    third_party/catapult/common/py_vulcanize/third_party/rjsmin  \
    third_party/catapult/third_party/polymer \
    third_party/catapult/tracing/third_party/d3 \
    third_party/catapult/tracing/third_party/gl-matrix \
    third_party/catapult/tracing/third_party/jszip \
    third_party/catapult/tracing/third_party/mannwhitneyu \
    third_party/catapult/tracing/third_party/oboe \
    third_party/catapult/tracing/third_party/pako \
    third_party/ced \
    third_party/cld_3 \
    third_party/crashpad \
    third_party/crashpad/crashpad/third_party/zlib \
    third_party/crc32c \
    third_party/cros_system_api \
    third_party/devscripts \
    third_party/dom_distiller_js \
    third_party/ffmpeg \
    third_party/fontconfig \
    third_party/s2cellid \
    third_party/fips181 \
    third_party/flatbuffers \
    third_party/flot \
    third_party/google_input_tools \
    third_party/google_input_tools/third_party/closure_library \
    third_party/google_input_tools/third_party/closure_library/third_party/closure \
    third_party/hunspell \
    third_party/iccjpeg \
%if !%{with system_jinja2}
    third_party/jinja2 \
%endif
    third_party/jstemplate \
    third_party/khronos \
    third_party/leveldatabase \
    third_party/libaddressinput \
    third_party/libaom \
    third_party/libjingle \
    third_party/libphonenumber \
    third_party/libsecret \
    third_party/libsrtp \
    third_party/libsync \
    third_party/libudev \
    third_party/libusb \
%if !%{with system_libvpx}
    third_party/libvpx \
    third_party/libvpx/source/libvpx/third_party/googletest \
    third_party/libvpx/source/libvpx/third_party/libwebm \
    third_party/libvpx/source/libvpx/third_party/libyuv \
    third_party/libvpx/source/libvpx/third_party/x86inc \
%endif
    third_party/libwebm \
%if %{with system_libxml2}
    third_party/libxml/chromium \
%else
    third_party/libxml \
%endif
    third_party/libXNVCtrl \
    third_party/libyuv \
third_party/llvm \
    third_party/lss \
    third_party/lzma_sdk \
%if !%{with system_markupsafe}
third_party/markupsafe \
%endif
    third_party/mesa \
    third_party/metrics_proto \
    third_party/modp_b64 \
%if !%{with system_openh264}
    third_party/openh264 \
%endif
    third_party/openmax_dl \
    third_party/opus \
    third_party/ots \
    third_party/freetype \
    third_party/test_fonts \
%if !%{with system_ply}
    third_party/ply \
%endif
    third_party/polymer \
    third_party/protobuf \
    third_party/protobuf/third_party/six \
    third_party/qcms \
    third_party/pyjson5 \
    third_party/rnnoise \
    third_party/sfntly \
    third_party/skia \
    third_party/skia/third_party/vulkan \
    third_party/skia/third_party/gif \
    third_party/skia/third_party/skcms \
    third_party/node/node_modules/polymer-bundler/lib/third_party/UglifyJS2 \
    third_party/smhasher \
    third_party/speech-dispatcher \
    third_party/sqlite \
    third_party/expat \
    third_party/tcmalloc \
    third_party/usb_ids \
    third_party/usrsctp \
    third_party/web-animations-js \
    third_party/webdriver \
    third_party/WebKit \
    third_party/webrtc \
    third_party/widevine \
    third_party/inspector_protocol \
    v8/third_party/antlr4 \
    v8/third_party/inspector_protocol \
    third_party/woff2 \
    third_party/xdg-utils \
    third_party/yasm/run_yasm.py \
    third_party/zlib/google \
    third_party/sinonjs \
    third_party/blanketjs \
    third_party/qunit \
    url/third_party/mozilla \
    third_party/pdfium \
    third_party/pdfium/third_party/agg23 \
    third_party/pdfium/third_party/base \
    third_party/pdfium/third_party/bigint \
    third_party/pdfium/third_party/freetype \
    third_party/pdfium/third_party/lcms \
    third_party/pdfium/third_party/libopenjpeg20 \
    third_party/pdfium/third_party/libpng16 \
    third_party/pdfium/third_party/libtiff \
    third_party/pdfium/third_party/skia_shared \
    third_party/perfetto \
    third_party/googletest \
    third_party/glslang-angle \
    third_party/unrar \
    third_party/vulkan \
    third_party/vulkan-validation-layers \
    third_party/angle/third_party/vulkan-validation-layers \
    third_party/spirv-tools-angle \
    third_party/spirv-headers \
    third_party/angle/third_party/spirv-tools \
%if !%{with system_harfbuzz}
    third_party/harfbuzz-ng \
%endif
    v8/src/third_party/utf8-decoder \
    v8/src/third_party/valgrind 

python2 build/linux/unbundle/replace_gn_files.py --system-libraries \
%if %{with system_ffmpeg}
    ffmpeg \
%endif
    flac \
    libdrm \
%if %{with system_harfbuzz}
    harfbuzz-ng \
%endif
    libjpeg \
    libpng \
    libwebp \
%if %{with system_libxml2}
    libxml \
%endif
    libxslt \
%if %{with system_openh264}
    openh264 \
%endif
    re2 \
    snappy \
%if %{with system_libicu}
    icu \
%endif
    yasm \
    fontconfig \
    zlib

python2 build/download_nacl_toolchains.py --packages \
    nacl_x86_glibc,nacl_x86_newlib,pnacl_newlib,pnacl_translator sync --extract


sed -i 's|//third_party/usb_ids|/usr/share/hwdata|g' device/usb/BUILD.gn

# Workaround build error caused by debugedit
# https://bugzilla.redhat.com/show_bug.cgi?id=304121
sed -i "/relpath/s|/'$|'|" tools/metrics/ukm/gen_builders.py
sed -i 's|^\(#include "[^"]*\)//\([^"]*"\)|\1/\2|' \
    third_party/webrtc/modules/audio_processing/utility/ooura_fft.cc \
    third_party/webrtc/modules/audio_processing/utility/ooura_fft_sse2.cc

%if %{with system_jinja2}
rmdir third_party/jinja2 
ln -s %{python2_sitelib}/jinja2 third_party/jinja2
%endif


%if %{with system_ply}
rmdir third_party/ply
ln -s %{python2_sitelib}/ply third_party/ply
%endif


# Remove compiler flags not supported by our system clang
%if 0%{?fedora} <= 27
  sed -i \
    -e '/"-Wno-enum-compare-switch"/d' \
    -e '/"-Wno-null-pointer-arithmetic"/d' \
    -e '/"-Wno-enum-compare-switch"/d' \
    -e '/"-Wno-tautological-unsigned-zero-compare"/d' \
    -e '/"-Wno-tautological-constant-compare"/d' \
    -e '/"-Wno-unused-lambda-capture"/d' \
    -e '/"-Wunused-lambda-capture"/d' \
    build/config/compiler/BUILD.gn
%endif

%if 0%{?fedora} >= 28 || %{with clang_bundle}
sed -i \
    -e '/"-Wno-ignored-pragma-optimize"/d' build/config/compiler/BUILD.gn
%endif

# Force script incompatible with Python 3 to use /usr/bin/python2
  sed -i '1s|python$|&2|' third_party/dom_distiller_js/protoc_plugins/*.py

%build

# https://fedoraproject.org/wiki/Changes/Avoid_usr_bin_python_in_RPM_Build#Quick_Opt-Out
export PYTHON_DISALLOW_AMBIGUOUS_VERSION=0

# some still call gcc/g++
%if %{with clang}
%if %{with clang_bundle}
export CC=%{_builddir}/buclang/bin/clang
export CXX=%{_builddir}/buclang/bin/clang++
%else
export CC=clang
export CXX=clang++
%endif
mkdir -p "$HOME/bin/"
ln -sfn $CC $HOME/bin/gcc
ln -sfn $CXX $HOME/bin/g++
export PATH="$HOME/bin/:$PATH"
%else
export CC="gcc"
export CXX="g++"
export CXXFLAGS="$CXXFLAGS -fno-delete-null-pointer-checks"
%endif

export AR=ar NM=nm

_flags+=(
    'is_debug=false'
%if %{with clang}
    'is_clang=true' 
%else
    'is_clang=false' 
%endif
%if %{with clang_bundle}
    'clang_base_path="%{_builddir}/buclang"'
    'clang_use_chrome_plugins=false'
%else
    'clang_base_path="/usr"'
    'clang_use_chrome_plugins=false'
%endif
    'fatal_linker_warnings=false'
    'treat_warnings_as_errors=false'
    'fieldtrial_testing_like_official_build=true'
    'remove_webcore_debug_symbols=true'
    'ffmpeg_branding="Chrome"'
    'proprietary_codecs=true'
%if %{with vaapi}
    'use_vaapi=true'
%else
    'use_vaapi=false'
%endif
    'use_aura=true'
    'link_pulseaudio=true'
    'linux_use_bundled_binutils=false'
    'use_custom_libcxx=false'
    'use_lld=false'
    'use_debug_fission=false'
    'use_allocator="none"'
    'use_ozone=false'
    'optimize_webui=false'
    'enable_iterator_debugging=false'
    'use_cups=true'
    'use_gnome_keyring=false'
    'use_gio=true'
    'use_gold=false'
    'use_kerberos=true'
    'use_pulseaudio=true'
    'use_system_freetype=true'
    'use_sysroot=false'
    'enable_hangout_services_extension=true'
    'enable_widevine=true'
    'enable_nacl=false'
    'enable_swiftshader=true'
    "google_api_key=\"AIzaSyD1hTe85_a14kr1Ks8T3Ce75rvbR1_Dx7Q\""
    "google_default_client_id=\"4139804441.apps.googleusercontent.com\""
    "google_default_client_secret=\"KDTRKEZk2jwT_7CDpcmMA--P\""
%ifarch x86_64
    'system_libdir="lib64"'
%endif
    'is_component_ffmpeg=true' 
    'is_component_build=false'
    'symbol_level=0'
%if %{with jumbo_unity}
    'use_jumbo_build=true'
    'jumbo_file_merge_limit=9'
%endif
    'concurrent_links=1'
    'optimize_for_size=true'
    'remove_webcore_debug_symbols=true'
%if %{with _gtk3}
    'use_gtk3=true'
%else
    'use_gtk3=false'
%endif
)


export PATH=%{_builddir}/tools/depot_tools/:"$PATH"

./tools/gn/bootstrap/bootstrap.py -v --gn-gen-args "${_flags[*]}"


./out/Release/gn gen --args="${_flags[*]}" out/Release 

# SUPER POWER!
jobs=$(grep processor /proc/cpuinfo | tail -1 | grep -o '[0-9]*')

ninja-build -C out/Release media/ffmpeg -j$jobs

%install

mkdir -p %{buildroot}%{chromiumdir}

install -m 644 out/Release/*.so %{buildroot}%{chromiumdir}/


%files

%{chromiumdir}/libffmpeg.so*

%changelog

* Thu Jul 26 2018 - David Va <davidva AT tuta DOT io> 68.0.3440.75-7
- Updated to 68.0.3440.75-7

* Thu Jun 14 2018 - David Vasquez <davidjeremias82 AT gmail DOT com>  67.0.3396.87-3
- Updated to 67.0.3396.87

* Wed May 16 2018 - David Vasquez <davidjeremias82 AT gmail DOT com>  66.0.3359.181-2
- Updated to 66.0.3359.181

* Wed May 09 2018 - David Vasquez <davidjeremias82 AT gmail DOT com>  66.0.3359.170-7
- Updated to 66.0.3359.170

* Wed Mar 21 2018 - David Vasquez <davidjeremias82 AT gmail DOT com>  65.0.3325.181-2
- Updated to 65.0.3325.181

* Thu Dec 14 2017 - David Vasquez <davidjeremias82 AT gmail DOT com>  63.0.3239.108-2
- Updated to 63.0.3239.108

* Tue Nov 21 2017 - David Vasquez <davidjeremias82 AT gmail DOT com>  62.0.3202.94-2
- Updated to 62.0.3202.94

* Wed Oct 18 2017 - David Vasquez <davidjeremias82 AT gmail DOT com>  62.0.3202.62-2
- Updated to 62.0.3202.62

* Fri Sep 15 2017 - David Vasquez <davidjeremias82 AT gmail DOT com>  61.0.3163.91-2
- Updated to 61.0.3163.91

* Wed Aug 30 2017 - David Vasquez <davidjeremias82 AT gmail DOT com>  60.0.3112.113-2
- Updated to 60.0.3112.113
- LD_PRELOAD fix thanks to domo141

* Wed Aug 16 2017 - David Vasquez <davidjeremias82 AT gmail DOT com>  60.0.3112.101-2
- Updated to 60.0.3112.101

* Thu Aug 03 2017 - David Vasquez <davidjeremias82 AT gmail DOT com>  60.0.3112.90-2
- Updated to 60.0.3112.90-2

* Sat Jul 08 2017 - David Vasquez <davidjeremias82 AT gmail DOT com>  59.0.3071.115-2
- Updated to 59.0.3071.115

* Tue Jun 20 2017 - David Vasquez <davidjeremias82 AT gmail DOT com>  59.0.3071.109-2
- Updated to 59.0.3071.109

* Wed May 10 2017 - David Vasquez <davidjeremias82 AT gmail DOT com>  58.0.3029.110-2
- Updated to 58.0.3029.110

* Fri May 05 2017 - David Vasquez <davidjeremias82 AT gmail DOT com>  58.0.3029.96-2
- Updated to 58.0.3029.96

* Sat Apr 08 2017 - David Vasquez <davidjeremias82 AT gmail DOT com>  57.0.2987.133-2
- Updated to 57.0.2987.133

* Tue Mar 28 2017 - David Vasquez <davidjeremias82 AT gmail DOT com>  57.0.2987.98-2
- Updated to 57.0.2987.110

* Fri Mar 10 2017 - David Vasquez <davidjeremias82 AT gmail DOT com>  57.0.2987.98-2
- Updated to 57.0.2987.98-2

* Thu Mar 02 2017 - David Vasquez <davidjeremias82 AT gmail DOT com>  56.0.2924.87-4
- Fix issue with compilation on gcc7, Thanks to Ben Noordhuis

* Mon Feb 06 2017 - David Vasquez <davidjeremias82 AT gmail DOT com>  56.0.2924.87-2
- Updated to 56.0.2924.87

* Thu Jan 26 2017 - David Vasquez <davidjeremias82 AT gmail DOT com>  56.0.2924.76-2
- Updated to 56.0.2924.76
- Renamed to chromium-freeworld

* Sun Dec 18 2016 - David Vasquez <davidjeremias82 AT gmail DOT com>  55.0.2883.87-2
- Updated to 55.0.2883.87

* Fri Dec 02 2016 - David Vasquez <davidjeremias82 AT gmail DOT com>  55.0.2883.75-2
- Updated to 55.0.2883.75

* Thu Dec 01 2016 - David Vasquez <davidjeremias82 AT gmail DOT com>  54.0.2840.100-3
- Conditional task

* Sat Nov 12 2016 - David Vasquez <davidjeremias82 AT gmail DOT com>  54.0.2840.100-2
- Updated to 54.0.2840.100

* Mon Nov 07 2016 - David Vasquez <davidjeremias82 AT gmail DOT com>  54.0.2840.90-2
- Updated to 54.0.2840.90

* Mon Oct 31 2016 - David Vasquez <davidjeremias82 AT gmail DOT com>  54.0.2840.71-3
- Initial build
