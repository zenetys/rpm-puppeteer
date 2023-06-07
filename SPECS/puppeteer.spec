# Supported targets: el9

%define puppeteer_version 18.2.1
%define zplugins_version 1.0.0

# dnf module enable nodejs:18
%define nodejs_major_version 18

Name: puppeteer
Version: %{puppeteer_version}
Release: 1%{?dist}.zenetys
Summary: Node.js API for Chrome
Group: Development/Libraries
License: Apache-2.0
URL: https://pptr.dev

Source0: https://registry.npmjs.org/puppeteer/-/puppeteer-%{puppeteer_version}.tgz

Source100: https://github.com/zenetys/zplugins/archive/refs/tags/v%{zplugins_version}.tar.gz#/zplugins-%{zplugins_version}.tar.gz
Patch100: zplugins-check_puppeteer-default-browser-bin.patch

BuildArch: noarch

BuildRequires: nodejs
BuildRequires: npm

Requires: chromium-headless
Requires: nodejs >= 1:%{nodejs_major_version}

%description
Puppeteer is a Node.js library which provides a high-level API to
control Chrome/Chromium over the DevTools Protocol.

This package is bundled with Nagios plugin check_puppeteer from
ZENETYS zplugins repository.

%prep
# puppeteer
%setup -c -T
tar xvzf %{SOURCE0} --strip-components 1 package/package.json

# zplugins (check_puppeteer)
%setup -T -D -a 100
cd zplugins-%{zplugins_version}
%patch100 -p1 -b .default-browser-bin
cd ..

%build
# puppeteer
mkdir build
cd build
node_modules_cache_txz=%{_sourcedir}/node_modules_puppeteer_%{puppeteer_version}_%{_arch}.tar.xz
if [ -f "$node_modules_cache_txz" ]; then
    tar xvJf "$node_modules_cache_txz"
else
    PUPPETEER_SKIP_DOWNLOAD=1 npm install \
        --loglevel verbose \
        --no-save \
        --no-bin-links \
        --prefix $PWD \
        %{SOURCE0}
    tar cJf "$node_modules_cache_txz" node_modules
fi
cd ..

%install
install -d -m 0755 %{buildroot}/opt/puppeteer
cp -RT --preserve=timestamp build %{buildroot}/opt/puppeteer
install -Dp -m 0755 zplugins-%{zplugins_version}/check_puppeteer %{buildroot}/opt/puppeteer/

%files
/opt/puppeteer
