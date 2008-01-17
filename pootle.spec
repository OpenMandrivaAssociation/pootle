%define name pootle
%define oname Pootle
%define version 0.11
%define release %mkrel 1

Summary: Web-based translation
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://downloads.sourceforge.net/translate/%{oname}-%{version}.tar.bz2
Patch0: Pootle-0.10.1-et.patch
License: GPL
Group: Networking/WWW
Url: http://translate.sourceforge.net/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildArch: noarch
BuildRequires: python-devel
Requires: python-jtoolkit
Requires: python-kid
Requires: python-translate

%description
Pootle is a web translation and translation management engine.

%prep
%setup -q -n %{oname}-%{version}
%patch0 -p1 -b .et

%build
./pootlesetup.py build

%install
rm -rf %{buildroot}
./pootlesetup.py install --prefix=%{buildroot}%{_prefix}

move_in() {
  target=$1
  shift
  install -d %{buildroot}$target
  for p in $*; do
    mv %{buildroot}%{py_puresitedir}/%{oname}/$p %{buildroot}$target
    ln -s $target/$p %{buildroot}%{py_puresitedir}/%{oname}
  done
}

move_in %{_var}/www/%{name} html templates
move_in %{_var}/lib/%{name} po
move_in %{_sysconfdir}/%{name} %{name}.prefs users.prefs

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc %{oname}/ChangeLog %{oname}/README
%{_bindir}/%{oname}Server
%{_bindir}/updatetm
%{py_puresitedir}/%{oname}
%{py_puresitedir}/*.egg-info
%{_var}/www/%{name}
%{_var}/lib/%{name}
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/*.prefs
