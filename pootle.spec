%define name pootle
%define oname Pootle
%define version 2.0.1
%define release %mkrel 1

Summary: Web-based translation
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://downloads.sourceforge.net/translate/%{oname}-%{version}.tar.bz2
Patch0: pootle-2.0-optimal-settings.patch
License: GPLv2+
Group: Development/Other
Url: http://translate.sourceforge.net/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildArch: noarch
%py_requires -d
Requires(pre): apache-conf >= 2.0.54
Requires(pre): memcached
Requires: python-translate >= 1.5.1
Requires: python-django >= 1.0
Requires: apache-mod_wsgi
Requires: python-memcached
Requires: python-lxml
Suggests: python-levenshtein
Suggests: iso-codes
Suggests: unzip
Suggests: xapian-bindings-python >= 1.0.13
Suggests: xapian-core >= 1.0.13
Suggests: python-mysql
Suggests: mysqlserver
Suggests: apache-mod_deflate


%description
Pootle is a web translation and translation management engine.

Its features include::
  * Translation of Gettext PO and XLIFF files.
  * Submitting to remote version control systems (VCS).
  * Managing groups of translators
  * Online webbased or offline translation
  * Quality checks


%prep
%setup -q -n %{oname}-%{version}
%patch0 -p2

%build
%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --root %{buildroot}

install -d -m 755 %{buildroot}%{_var}/www/%{name}
cp %{buildroot}%{_docdir}/%{name}/wsgi.py %{buildroot}%{_var}/www/%{name}

install -d -m 755 %{buildroot}%{webappconfdir}
cat >> %{buildroot}%{webappconfdir}/%{name}.conf <<EOF
WSGIScriptAlias /%{name} %{_var}/www/%{name}/wsgi.py
<Directory %{_var}/www/%{name}>
    Order deny,allow
    Allow from all
</Directory>

Alias /%{name}/html %{_datadir}/%{name}/html
<Directory "%{_datadir}/%{name}/html">
    Order deny,allow
    Allow from all
</Directory>

Alias /%{name}/export %{_var}/lib/%{name}/po
<Directory "%{_var}/lib/%{name}/po">
    Order deny,allow
    Allow from all
</Directory>

<IfModule mod_deflate.c>
    <location /%{name}/html>
        SetOutputFilter DEFLATE
    </location>
    <location /%{name}/export>
        SetOutputFilter DEFLATE
    </location>
</IfModule>
EOF

%clean
rm -rf %{buildroot}

%post
if [ ! -f %{_var}/lock/subsys/memcached ]; then
    %{__service} memcached start
fi
%{_post_webapp}

%postun
%{_postun_webapp}

%files
%defattr(-,root,root,-)
%doc %{_docdir}/%{name}/*
%{_bindir}/%{oname}Server
%{_bindir}/updatetm
%{_bindir}/import_pootle_prefs
%{_datadir}/%{name}
%{py_puresitedir}/%{name}
%{py_puresitedir}/%{name}_app
%{py_puresitedir}/%{name}_store
%{py_puresitedir}/%{name}_notifications
%{py_puresitedir}/%{name}_autonotices
%{py_puresitedir}/%{name}_misc
%{py_puresitedir}/djblets
%{py_puresitedir}/profiles
%{py_puresitedir}/registration
%{py_puresitedir}/*.egg-info
%{_var}/www/%{name}
%attr(0755,apache,apache) %{_var}/lib/%{name}
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/localsettings.py
%config(noreplace) %{_webappconfdir}/%{name}.conf
