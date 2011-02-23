%define name pootle
%define oname Pootle
%define version 2.1.5
%define release %mkrel 1

Summary: Web-based translation
Name: %{name}
Version: %{version}
Release: %{release}
License: GPLv2+
Group: Development/Other
Url: http://translate.sourceforge.net/
Source0: http://downloads.sourceforge.net/translate/%{oname}-%{version}.tar.bz2
%py_requires -d
Requires: memcached
Requires: python-translate >= 1.5.1
Requires: python-django >= 1.0
Requires: apache-mod_wsgi
Requires: python-lxml
Suggests: python-levenshtein
Suggests: python-memcached
Suggests: iso-codes
Suggests: unzip
Suggests: xapian-bindings-python >= 1.0.13
Suggests: xapian-core >= 1.0.13
Suggests: python-mysql
Suggests: mysqlserver
Suggests: apache-mod_deflate
%if %mdkversion < 201010
Requires(post):   rpm-helper
Requires(postun):   rpm-helper
%endif
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}


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
    Order allow,deny
    Allow from all
</Directory>

Alias /%{name}/html %{_datadir}/%{name}/html
<Directory "%{_datadir}/%{name}/html">
    Order allow,deny
    Allow from all
</Directory>

Alias /%{name}/export %{_var}/lib/%{name}/po
<Directory "%{_var}/lib/%{name}/po">
    Order allow,deny
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
%if %mdkversion < 201010
%_post_webapp
%endif

%postun
%if %mdkversion < 201010
%_postun_webapp
%endif

%files
%defattr(-,root,root,-)
%doc %{_docdir}/%{name}
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
%{py_puresitedir}/%{name}_terminology
%{py_puresitedir}/%{name}_translationproject
%{py_puresitedir}/%{name}_profile
%{py_puresitedir}/%{name}_project
%{py_puresitedir}/%{name}_language
%{py_puresitedir}/%{name}_statistics
%{py_puresitedir}/djblets
%{py_puresitedir}/profiles
%{py_puresitedir}/registration
%{py_puresitedir}/contact_form_i18n
%{py_puresitedir}/*.egg-info
%{_var}/www/%{name}
%attr(0755,apache,apache) %{_var}/lib/%{name}
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/localsettings.py
%config(noreplace) %{_webappconfdir}/%{name}.conf
