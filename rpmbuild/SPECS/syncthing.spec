Name:           syncthing 
Version:        0.14.43
Release:        1%{?dist} 
Summary:        Syncthing 
 
License:        MIT 
URL:            http://syncthing.net/ 
Source0:        https://github.com/syncthing/syncthing/archive/v%{version}.tar.gz 
Source1:        syncthing
Source2:        syncthinglog
Source3:        syncthing.env
BuildRequires:  gcc 
Requires(pre): /usr/sbin/useradd, /usr/bin/getent 
Requires(postun): /usr/sbin/userdel 

%define AltDir /opt/syncthing 
%define  debug_package %{nil} 
 
%description 
Syncthing replaces Dropbox and BitTorrent Sync with something open, trustworthy and decentralized. Your data is your data alone and you deserve to choose where it is stored, if it is shared with some third party and how it's transmitted over the Internet. 
 
Using syncthing, that control is returned to you. 
 
%prep 
%setup -q -n syncthing-%{version} 

%pre 
id syncthing &> /dev/null || /usr/sbin/useradd -r -u 20000 -G users -d /opt/syncthing syncthing 
 
 
%build 
mkdir -p ./_build/%{AltDir}/bin/ 
mkdir -p ./_build/src/github.com/syncthing 
ln -s $(pwd) ./_build/src/github.com/syncthing/syncthing 
# export GOPATH=$(pwd)/_build/
cd ./_build/src/github.com/syncthing/syncthing 
go run build.go -version v%{version} -no-upgrade 
 
%install 
mkdir -p %{buildroot}%{AltDir}/bin 
mkdir -p %{buildroot}/etc/init.d 
mkdir -p %{buildroot}/etc/logrotate.d/
mkdir -p %{buildroot}/var/log/syncthing/
 
install -d %{buildroot}%{AltDir} 
install -p -m 0755 ./bin/syncthing %{buildroot}%{AltDir}/bin/syncthing 
install -p -m 0644 %{SOURCE1} %{buildroot}/etc/init.d/ 
install -p -m 0644 %{SOURCE2} %{buildroot}/etc/logrotate.d/
install -p -m 0644 %{SOURCE3} %{buildroot}%{AltDir}/syncthing.env 

%post 
/sbin/chkconfig --add syncthing
/sbin/chkconfig syncthing on

%preun
/sbin/service syncthing stop 
/sbin/chkconfig --del syncthing

%files 
%defattr(-,root,root,-) 
#%doc README.txt LICENSE.txt CONTRIBUTORS.txt 
%dir %{AltDir}/bin/*
%attr(755, root, root) /etc/init.d/* 
%attr(755,syncthing,users) %{AltDir} 
%attr(755,syncthing,users) %{AltDir}/* 
%attr(755,syncthing,users) %{AltDir}/bin/*
%attr(755, root, root) /var/log/syncthing/
%attr(755, root, root) /etc/logrotate.d/*
 
%changelog