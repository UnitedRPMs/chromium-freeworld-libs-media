#
# spec file for package chromium-freeworld
#
# Copyright (c) 2020 UnitedRPMs.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://goo.gl/zqFJft
#

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
#  [10] http://svnweb.mageia.org/packages/cauldron/chromium-browser-stable/?pathrev=1321923
#  [11] https://gitlab.com/noencoding/OS-X-Chromium-with-proprietary-codecs/wikis/List-of-all-gn-arguments-for-Chromium-build
#  [12] https://operasoftware.github.io/upstreamtools/
#  [13] https://build.opensuse.org/package/show/network:chromium/chromium-beta
#  [14] https://github.com/saiarcot895/chromium-ubuntu-build
#  [15] https://git.exherbo.org/desktop.git/tree/packages/net-www/chromium-stable


%global chromiumdir %{_libdir}/chromium
%global crd_path %{_libdir}/chrome-remote-desktop
# Do not check any ffmpeg or libmedia bundle files in libdir for requires
%global __requires_exclude_from ^%{chromiumdir}/libffmpeg.*$
%global __requires_exclude_from ^%{chromiumdir}/libmedia.*$

#
# Get the version number of latest stable version
# $ curl -s 'https://omahaproxy.appspot.com/all?os=linux&channel=stable' | sed 1d | cut -d , -f 3
%bcond_without normalsource

%global debug_package %{nil}

# clang is necessary for a fast build
%bcond_without clang
# 

# About clang bundle: Necessary in cases where "clang" in system, fails to build chromium.
%if 0%{?fedora} <= 28
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
%bcond_with system_ply

# Require libxml2 > 2.9.4 for XML_PARSE_NOXXE
%if 0%{?fedora} >= 27
%bcond_without system_libxml2
%else
%bcond_with system_libxml2
%endif

# Require harfbuzz >= 1.5.0 for hb_glyph_info_t
# hb-aat.h isn't in system anymore...
%bcond_with system_harfbuzz

# Allow testing whether icu can be unbundled
%bcond_with system_libicu

# Allow disabling unconditional build dependency on clang
%bcond_without require_clang

# In UnitedRPMs, we have openh264
%bcond_without system_openh264

# Now is easy to use the external ffmpeg...
%bcond_with system_ffmpeg

# Jumbo / Unity builds (deprecated)
# https://chromium.googlesource.com/chromium/src/+/lkcr/docs/jumbo.md
%bcond_with jumbo_unity

# Vaapi conditional
%bcond_without vaapi

# Gtk2 conditional
%bcond_with gtk2

# re2 conditional
%bcond_with re2_external

# swiftshader conditional
%bcond_with swiftshader

# 
%define _legacy_common_support 1

# Generally the .spec file is the same of our chromium-freeworld, building only ffmpeg; then we will obtain all possible codecs.

Name:       chromium-freeworld-libs-media
Version:    81.0.4044.138
Release:    189.1
Summary:    Chromium media libraries built with all possible codecs

Group:      Applications/Internet
License:    BSD and LGPLv2+
URL:        https://www.chromium.org
Vendor:     URPMS

%if %{with normalsource}
Source0:    https://commondatastorage.googleapis.com/chromium-browser-official/chromium-%{version}.tar.xz
%endif
Source1:    chromium-latest.py
Source2:    BUILD.gn
# markupsafe
Source22:   https://github.com/pallets/markupsafe/archive/1.1.1.tar.gz
# Clang bundle
%if %{with clang_bundle}
Source23:  https://releases.llvm.org/8.0.0/clang+llvm-8.0.0-x86_64-linux-gnu-ubuntu-18.04.tar.xz 
%endif

#----------------------------------------------------------------------------------------------------------------------------
# Patches 
Patch1: widevine-other-locations.patch
Patch2: widevine-allow-on-linux.patch
Patch3: chromium-nacl-llvm-ar.patch
Patch4: chromium-python2.patch
Patch5: chromium-base-unittests-icu-fix.patch
Patch6: chromium-fix-re2-set_utf8.patch

Patch8: chromium-gl_defines_fix.patch
Patch9: chromium-remove-no-canonical-prefixes.patch
Patch10: chromium-swiftshader-default-visibility.patch
Patch11: chromium-unbundle-zlib.patch
Patch12: chromium-freeworld/chromium-webrtc-r0.patch

Patch22: gtk2.patch

# VAAPI
Patch23: gpu-timeout.patch
Patch24: rebuild-Linux-frame-button-cache-when-activation.patch
Patch25: rename-Relayout-in-DesktopWindowTreeHostPlatform.patch
Patch26: chromium-81-gcc-10.patch

Patch27: vaapi-build-fix.patch
Patch29: eglGetMscRateCHROMIUM.patch

ExclusiveArch: x86_64 


%if %{with clang} || %{with require_clang} 
BuildRequires: clang llvm
%endif
# Basic tools and libraries
BuildRequires: ninja-build 
BuildRequires: bison 
BuildRequires: gperf 
BuildRequires: hwdata 
BuildRequires: gn 
%if 0%{?fedora} >= 29
BuildRequires: java-openjdk-headless
%else
BuildRequires: javapackages-tools
%endif
BuildRequires: xz
#BuildRequires: glibc32
BuildRequires: libgcc(x86-32) 
BuildRequires: glibc(x86-32) 
BuildRequires: redhat-rpm-config
BuildRequires: libatomic
BuildRequires: libcap-devel 
BuildRequires: cups-devel 
BuildRequires: alsa-lib-devel
%if 0%{?fedora} >= 30
BuildRequires:	minizip-compat-devel
%else
BuildRequires:	minizip-devel
%endif
BuildRequires: pkgconfig(libexif) 
BuildRequires: pkgconfig(nss) 
%if %{with gtk2}
BuildRequires: pkgconfig(gtk+-2.0)
%else
BuildRequires: pkgconfig(gtk+-3.0)
%endif
BuildRequires: python2-devel
%if 0%{?fedora} >= 29
BuildRequires:	python-unversioned-command
%endif
BuildRequires: pkgconfig(xtst) 
BuildRequires: pkgconfig(xscrnsaver)
BuildRequires: pkgconfig(dbus-1) 
BuildRequires: pkgconfig(libudev)
#BuildRequires: pkgconfig(gnome-keyring-1)
BuildRequires: pkgconfig(libffi)
# remove_bundled_libraries.py --do-remove
BuildRequires: python2-rpm-macros
#BuildRequires: python2-beautifulsoup4
#BuildRequires: python-html5lib
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
BuildRequires: libvpx-devel
BuildRequires: libwebp-devel
BuildRequires: pkgconfig(libxslt)
BuildRequires: opus-devel
%if %{with system_libxml2}
BuildRequires: pkgconfig(libxml-2.0)
%endif
%if %{with re2_external}
BuildRequires: re2-devel
%endif
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
# install AppData files
BuildRequires: libappstream-glib
# remote desktop needs this
BuildRequires: pam-devel
BuildRequires: systemd
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
# ffmpeg external conditional
%if %{with system_ffmpeg}
BuildRequires: ffmpeg-devel >= 4.1
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
BuildRequires:	google-noto-sans-cjk-jp-fonts
BuildRequires:	google-noto-sans-khmer-fonts
BuildRequires:	google-croscore-tinos-fonts
BuildRequires:	subversion
BuildRequires:	at-spi2-core-devel
%if %{with clang_bundle}
BuildRequires:	ncurses-compat-libs
BuildRequires:  z3-libs
%endif
BuildRequires:	libevent-devel
BuildRequires:  expat-devel
BuildRequires:  mesa-libgbm-devel
%if 0%{?fedora} >= 32
BuildRequires:	pipewire0.2-devel
%else
BuildRequires:	pipewire-devel >= 0.2
%endif

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
%setup -n chromium-%{version} 
%else
wget -c https://commondatastorage.googleapis.com/chromium-browser-official/chromium-%{version}.tar.xz
tar xJf %{_builddir}/chromium-%{version}.tar.xz -C %{_builddir}
%setup -T -D -n chromium-%{version} 
%endif

%if %{with clang_bundle}
tar xJf %{S:23} -C %{_builddir}
pushd %{_builddir}
mv -f clang+llvm-8.0.0-x86_64-linux-gnu-ubuntu-18.04 buclang 
pushd buclang/lib/
ln -sf /usr/lib64/libz3.so.0.0.0 libz3.so.4.8
popd
 popd
%endif


# Copy the toolchain settings
mkdir toolchain
cp %{S:2} toolchain/BUILD.gn

%if %{with system_markupsafe}
pushd third_party/
rm -rf markupsafe/
ln -sf %{python2_sitearch}/markupsafe/ markupsafe
popd
%else
pushd third_party
rm -rf markupsafe/
mkdir -p markupsafe
tar xmzvf %{S:22} -C $PWD/
# git clone --depth 1 https://github.com/pallets/markupsafe.git $PWD/markupsafe
cp -f $PWD/markupsafe-1.1.1/src/markupsafe/*.py $PWD/markupsafe/
cp -f $PWD/markupsafe-1.1.1/src/markupsafe/*.c $PWD/markupsafe/
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


# Allow building against system libraries in official builds
  sed -i 's/OFFICIAL_BUILD/GOOGLE_CHROME_BUILD/' \
    tools/generate_shim_headers/generate_shim_headers.py


# Avoid CFI failures with unbundled libxml
  sed -i -e 's/\<xmlMalloc\>/malloc/' -e 's/\<xmlFree\>/free/' \
    third_party/blink/renderer/core/xml/*.cc \
    third_party/blink/renderer/core/xml/parser/xml_document_parser.cc \
    third_party/libxml/chromium/libxml_utils.cc

# Patches, disabled autosetup

%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1


%patch23 -p1
%patch24 -p1
%patch25 -p1
%patch26 -p1

%if %{with gtk2}
%patch22 -p1
%endif
%if %{with vaapi}
%patch27 -p1

%patch29 -p1
%endif

# Change shebang in all relevant files in this directory and all subdirectories
# See `man find` for how the `-exec command {} +` syntax works
# find -type f -exec sed -iE '1s=^#! */usr/bin/\(python\|env python\)[23]\?=#!%{__python2}=' {} +
find -depth -type f -writable -name "*.py" -exec sed -iE '1s=^#! */usr/bin/\(python\|env python\)[23]\?=#!%{__python2}=' {} +


# python2 fix
mkdir -p "$HOME/bin/"
ln -sfn %{__python2} $HOME/bin/python
export PATH="$HOME/bin/:$PATH"

python2 build/linux/unbundle/remove_bundled_libraries.py --do-remove \
    base/third_party/cityhash \
    base/third_party/double_conversion/double-conversion \
    base/third_party/dynamic_annotations \
    base/third_party/icu \
    base/third_party/nspr \
    base/third_party/superfasthash \
    base/third_party/symbolize \
    base/third_party/valgrind \
    base/third_party/xdg_mime \
    base/third_party/xdg_user_dirs \
    buildtools/third_party/libc++ \
    buildtools/third_party/libc++abi \
    chrome/third_party/mozilla_security_manager \
    courgette/third_party \
    net/third_party/mozilla_security_manager \
    net/third_party/nss \
    net/third_party/quiche \
    net/third_party/uri_template \
    third_party/abseil-cpp \
    third_party/angle \
    third_party/angle/src/common/third_party/base \
    third_party/angle/src/common/third_party/smhasher \
    third_party/angle/src/common/third_party/xxhash \
    third_party/angle/src/third_party/compiler \
    third_party/angle/src/third_party/libXNVCtrl \
    third_party/angle/src/third_party/trace_event \
    third_party/angle/src/third_party/volk \
    third_party/angle/third_party/glslang \
    third_party/angle/third_party/spirv-headers \
    third_party/angle/third_party/spirv-tools \
    third_party/angle/third_party/vulkan-headers \
    third_party/angle/third_party/vulkan-loader \
    third_party/angle/third_party/vulkan-tools \
    third_party/angle/third_party/vulkan-validation-layers \
    third_party/apple_apsl \
    third_party/axe-core \
    third_party/blink \
    third_party/boringssl \
    third_party/boringssl/src/third_party/fiat \
    third_party/breakpad \
    third_party/breakpad/breakpad/src/third_party/curl \
    third_party/brotli \
    third_party/cacheinvalidation \
    third_party/catapult \
    third_party/catapult/common/py_vulcanize/third_party/rcssmin \
    third_party/catapult/common/py_vulcanize/third_party/rjsmin \
    third_party/catapult/third_party/polymer \
    third_party/catapult/tracing/third_party/d3 \
    third_party/catapult/tracing/third_party/gl-matrix \
    third_party/catapult/tracing/third_party/jpeg-js \
    third_party/catapult/tracing/third_party/jszip \
    third_party/catapult/tracing/third_party/mannwhitneyu \
    third_party/catapult/tracing/third_party/oboe \
    third_party/catapult/tracing/third_party/pako \
    third_party/ced \
    third_party/cld_3 \
    third_party/closure_compiler \
    third_party/crashpad \
    third_party/crashpad/crashpad/third_party/lss \
    third_party/crashpad/crashpad/third_party/zlib \
    third_party/crc32c \
    third_party/cros_system_api \
    third_party/dav1d \
    third_party/dawn \
    third_party/depot_tools \
    third_party/devscripts \
    third_party/devtools-frontend \
    third_party/devtools-frontend/src/third_party \
    third_party/dom_distiller_js \
    third_party/emoji-segmenter \
    third_party/flatbuffers \
    third_party/freetype \
    third_party/libgifcodec \
    third_party/google_input_tools \
    third_party/google_input_tools/third_party/closure_library \
    third_party/google_input_tools/third_party/closure_library/third_party/closure \
    third_party/googletest \
    third_party/glslang \
    third_party/hunspell \
    third_party/iccjpeg \
    third_party/icu \
    third_party/inspector_protocol \
    third_party/jsoncpp \
    third_party/jstemplate \
    third_party/khronos \
    third_party/leveldatabase \
    third_party/libXNVCtrl \
    third_party/libaddressinput \
    third_party/libaom \
    third_party/libaom/source/libaom/third_party/vector \
    third_party/libaom/source/libaom/third_party/x86inc \
    third_party/libjingle \
    third_party/libphonenumber \
    third_party/libsecret \
    third_party/libsrtp \
    third_party/libsync \
    third_party/libudev \
    third_party/libwebm \
    third_party/libyuv \
    third_party/llvm \
    third_party/lss \
    third_party/lzma_sdk \
    third_party/metrics_proto \
    third_party/modp_b64 \
    third_party/nasm \
    third_party/node \
    third_party/node/node_modules/polymer-bundler/lib/third_party/UglifyJS2 \
    third_party/one_euro_filter \
    third_party/openscreen \
    third_party/openscreen/src/third_party/tinycbor \
    third_party/ots \
    third_party/perfetto \
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
    third_party/pffft \
    third_party/polymer \
    third_party/private-join-and-compute \
    third_party/protobuf \
    third_party/protobuf/third_party/six \
    third_party/pyjson5/src/json5 \
    third_party/qcms \
    third_party/rnnoise \
    third_party/s2cellid \
    third_party/skia \
    third_party/skia/include/third_party/skcms \
    third_party/skia/include/third_party/vulkan/vulkan \
    third_party/skia/third_party/skcms \
    third_party/skia/third_party/vulkanmemoryallocator \
    third_party/smhasher \
    third_party/spirv-headers \
    third_party/SPIRV-Tools \
    third_party/sqlite \
    third_party/swiftshader \
    third_party/swiftshader/third_party/llvm-7.0 \
    third_party/swiftshader/third_party/llvm-subzero \
    third_party/swiftshader/third_party/marl \
    third_party/swiftshader/third_party/SPIRV-Headers \
    third_party/swiftshader/third_party/subzero \
    third_party/tcmalloc \
    third_party/unrar \
    third_party/usrsctp \
    third_party/vulkan \
    third_party/web-animations-js \
    third_party/webdriver \
    third_party/webrtc \
    third_party/webrtc/common_audio/third_party/fft4g \
    third_party/webrtc/common_audio/third_party/spl_sqrt_floor \
    third_party/webrtc/modules/third_party/fft \
    third_party/webrtc/modules/third_party/g711 \
    third_party/webrtc/modules/third_party/g722 \
    third_party/webrtc/rtc_base/third_party/base64 \
    third_party/webrtc/rtc_base/third_party/sigslot \
    third_party/widevine \
    third_party/woff2 \
    third_party/wuffs \
    third_party/zlib/google \
    url/third_party/mozilla \
    v8/src/third_party/siphash \
    v8/src/third_party/utf8-decoder \
    v8/src/third_party/valgrind \
    v8/third_party/inspector_protocol \
    v8/third_party/v8 \
    third_party/adobe \
    third_party/speech-dispatcher \
    third_party/usb_ids \
    third_party/xdg-utils \
    third_party/yasm/run_yasm.py \
    tools/gn/src/base/third_party/icu \
    third_party/libvpx \
    third_party/libvpx/source/libvpx/third_party/x86inc \
    third_party/catapult/third_party/six \
    third_party/protobuf/third_party/six \
    tools/grit/third_party/six \
    third_party/catapult/third_party/beautifulsoup4 \
    third_party/catapult/third_party/html5lib-python \
%if !%{with re2_external}
		third_party/re2 \
%endif
%if %{with remote_desktop}
		third_party/sinonjs \
		third_party/blanketjs \
		third_party/qunit \
%endif
%if !%{with system_jinja2}
    		third_party/jinja2 \
%endif
%if %{with system_libxml2}
   		third_party/libxml/chromium \
%else
    		third_party/libxml \
%endif
%if !%{with system_markupsafe}
		third_party/markupsafe \
%endif
%if !%{with system_openh264}
    		third_party/openh264 \
%endif
%if !%{with system_ply}
    		third_party/ply \
%endif
%if !%{with system_harfbuzz}
    		third_party/harfbuzz-ng \
%endif
%if !%{with system_ffmpeg} 
		third_party/ffmpeg 
%endif

python2 build/linux/unbundle/replace_gn_files.py --system-libraries \
%if %{with system_ffmpeg}
    ffmpeg \
%endif
    flac \
    libdrm \
    libevent \
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
    snappy \
%if %{with re2_external}
    re2 \
%endif
%if %{with system_libicu}
    icu \
%endif
    yasm \
    opus \
    fontconfig \
    zlib


# Don't use static libstdc++
sed -i '/-static-libstdc++/d' tools/gn/build/gen.py

%if %{with system_jinja2}
rmdir third_party/jinja2 
ln -s %{python2_sitelib}/jinja2 third_party/jinja2
%endif


%if %{with system_ply}
rm -rf third_party/ply
ln -s %{python2_sitelib}/ply third_party/ply
%endif


%if 0%{?fedora} >= 28 || %{with clang_bundle}
sed -i \
    -e '/"--fsplit-lto-unit"/d' build/config/compiler/BUILD.gn

sed -i \
    -e '/"-Wno-defaulted-function-deleted"/d' build/config/compiler/BUILD.gn

sed -i \
    -e '/"-Wextra-semi-stmt"/d' build/config/compiler/BUILD.gn

sed -i \
    -e '/"-Wno-implicit-int-float-conversion"/d' build/config/compiler/BUILD.gn

sed -i \
    -e '/"-Wno-c99-designator"/d' build/config/compiler/BUILD.gn

sed -i \
    -e '/"-Wno-final-dtor-non-final-class"/d' build/config/compiler/BUILD.gn

sed -i \
    -e '/"-Wno-sizeof-array-div"/d' build/config/compiler/BUILD.gn
    
sed -i \
    -e '/"-Wno-bitwise-conditional-parentheses"/d' build/config/compiler/BUILD.gn 
    
sed -i \
    -e '/"-Wno-builtin-assume-aligned-alignment"/d' build/config/compiler/BUILD.gn 
    
    sed -i \
    -e '/"-Wno-deprecated-copy"/d' build/config/compiler/BUILD.gn

sed -i \
    -e '/"-Qunused-arguments"/d' \
    build/config/compiler/BUILD.gn

%endif

# Force script incompatible with Python 3 to use /usr/bin/python2
  sed -i '1s|python$|&2|' third_party/dom_distiller_js/protoc_plugins/*.py

%build

# python2 fix
 export PATH="$HOME/bin/:$PATH"

# some still call gcc/g++
%if %{with clang}
%if %{with clang_bundle}
export CC=%{_builddir}/buclang/bin/clang
export CXX=%{_builddir}/buclang/bin/clang++
export LD_LIBRARY_PATH=%{_builddir}/buclang/lib:%{_libdir}:$LD_LIBRARY_PATH
export CFLAGS="-O4 -I%{_builddir}/buclang/include -fPIC -Wno-builtin-macro-redefined"
export CXXFLAGS="-O4 -I%{_builddir}/buclang/include -fPIC -Wno-builtin-macro-redefined"
export LDFLAGS="-O4 -L%{_builddir}/buclang/lib"

  # Do not warn about unknown warning options
  CFLAGS+='   -Wno-unknown-warning-option'
  CXXFLAGS+=' -Wno-unknown-warning-option'
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
export PNACLPYTHON=%{__python2}

# GN conf
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
    'use_system_freetype=false'
    'use_sysroot=false'
    'enable_hangout_services_extension=true'
    'enable_widevine=true'
    'enable_nacl=false'
%if %{with swiftshader}
    'enable_swiftshader=true'
%else
    'enable_swiftshader=false'
%endif
    "google_api_key=\"AIzaSyD1hTe85_a14kr1Ks8T3Ce75rvbR1_Dx7Q\""
    "google_default_client_id=\"4139804441.apps.googleusercontent.com\""
    "google_default_client_secret=\"KDTRKEZk2jwT_7CDpcmMA--P\""
%if !%{with system_ffmpeg}
    'is_component_ffmpeg=true' 
%endif
    'blink_symbol_level=0'
%if %{with system_harfbuzz}
    'use_system_harfbuzz=true'
%else
    'use_system_harfbuzz=false'
%endif
%if %{with gtk2}
    'gtk_version=2'
%endif
%ifarch x86_64
    'system_libdir="lib64"'
%endif 
    'symbol_level=0'
%if %{with jumbo_unity}
    'use_jumbo_build=true'
    'jumbo_file_merge_limit=8'
%endif
    'rtc_use_pipewire=true'
    'rtc_link_pipewire=true'
    'concurrent_links=1'
)



# Build files for Ninja #
%{_bindir}/gn gen --script-executable=/usr/bin/python2 --args="${_flags[*]}" out/Release 

# SUPER POWER!
jobs=$(grep processor /proc/cpuinfo | tail -1 | grep -o '[0-9]*')


%ninja_build -C out/Release media/ffmpeg -j$jobs

%install

mkdir -p %{buildroot}%{chromiumdir}

install -m 644 out/Release/libffmpeg.so* %{buildroot}%{chromiumdir}/


%files
%{chromiumdir}/libffmpeg.so*

%changelog

* Tue May 12 2020 - David Va <davidva AT tuta DOT io> 81.0.4044.138
- Updated to 81.0.4044.138

* Sun Apr 12 2020 - David Va <davidva AT tuta DOT io> 81.0.4044.92
- Updated to 81.0.4044.92

* Wed Jan 29 2020 - David Va <davidva AT tuta DOT io> 80.0.3987.87
- Updated to 80.0.3987.87

* Thu Nov 28 2019 - David Va <davidva AT tuta DOT io> 78.0.3904.108
- Updated to 78.0.3904.108

* Thu Nov 07 2019 - David Va <davidva AT tuta DOT io> 78.0.3904.97
- Updated to 78.0.3904.97

* Thu Sep 19 2019 - David Va <davidva AT tuta DOT io> 77.0.3865.90
- Updated to 77.0.3865.90

* Fri Aug 09 2019 - David Va <davidva AT tuta DOT io> 75.0.3770.142
- Updated to 75.0.3770.142

* Sat Dec 22 2018 - David Va <davidva AT tuta DOT io> 71.0.3578.98-7
- Updated to 71.0.3578.98

* Tue Dec 11 2018 - David Va <davidva AT tuta DOT io> 70.0.3538.110-7
- Updated to 70.0.3538.110

* Tue Nov 27 2018 - David Va <davidva AT tuta DOT io> 70.0.3538.102-7
- Updated to 70.0.3538.102

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
