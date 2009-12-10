%define name pootle
%define oname Pootle
%define version 2.0.0
%define release %mkrel 1

Summary: Web-based translation
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://downloads.sourceforge.net/translate/%{oname}-%{version}.tar.bz2
License: GPL
Group: Networking/WWW
Url: http://translate.sourceforge.net/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildArch: noarch
BuildRequires: python-devel
Requires: python-jtoolkit
Requires: python-kid
Requires: python-translate >= 1.5.1

%description
Pootle is a web translation and translation management engine.

%prep
%setup -q -n %{oname}-%{version}

%build
./setup.py build

%install
rm -rf %{buildroot}
./setup.py install --root=%{buildroot} --prefix=%{_prefix}

move_in() {
  target=$1
  shift
  install -d %{buildroot}$target
  for p in $*; do
    mv %{buildroot}%{py_puresitedir}/%{oname}/$p %{buildroot}$target
    ln -s $target/$p %{buildroot}%{py_puresitedir}/%{oname}
  done
}

#move_in %{_var}/www/%{name} html templates
#move_in %{_var}/lib/%{name} po
#move_in %{_sysconfdir}/%{name} %{name}.prefs users.prefs

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc ChangeLog README
%{_bindir}/*
%{_datadir}/%{name}
%{py_puresitedir}/*
#{_var}/www/%{name}
%{_var}/lib/%{name}
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/*
