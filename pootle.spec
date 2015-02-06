%define oname Pootle

Summary: Web-based translation
Name:    pootle
Version: 2.1.5
Release: 7
License: GPLv2+
Group: Development/Other
Url: http://translate.sourceforge.net/
Source0: http://downloads.sourceforge.net/translate/%{oname}-%{version}.tar.bz2
BuildRequires: python-devel
Requires: python-translate >= 1.5.1
Requires: python-django >= 1.0
# this one should be relaxed
Requires: apache-mod_wsgi
Requires: python-lxml
Requires: python-djblets
Suggests: python-levenshtein
Suggests: python-memcached
Suggests: iso-codes
Suggests: unzip
Suggests: xapian-bindings-python >= 1.0.13
Suggests: xapian-core >= 1.0.13
Suggests: python-mysql
Suggests: mysqlserver
Suggests: apache-mod_deflate
BuildArch: noarch


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

# do not ship a bundled copy, as this is already packaged
rm -Rf %{buildroot}/%{python_sitelib}/djblets

install -d -m 755 %{buildroot}%{_var}/www/%{name}
cp %{buildroot}%{_docdir}/%{name}/wsgi.py %{buildroot}%{_var}/www/%{name}

install -d -m 755 %{buildroot}%{_webappconfdir}
cat >> %{buildroot}%{_webappconfdir}/%{name}.conf <<EOF
WSGIScriptAlias /%{name} %{_var}/www/%{name}/wsgi.py
<Directory %{_var}/www/%{name}>
    Require all granted
</Directory>

Alias /%{name}/html %{_datadir}/%{name}/html
<Directory "%{_datadir}/%{name}/html">
    Require all granted
</Directory>

Alias /%{name}/export %{_var}/lib/%{name}/po
<Directory "%{_var}/lib/%{name}/po">
    Require all granted
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

# Drop shebang from non-executable scripts to make rpmlint happy
find %{buildroot}%{python_sitelib} -name "*py" -perm 644 -exec sed -i '/#!\/usr\/bin\/env python/d' {} \;

%clean
rm -rf %{buildroot}



%files
%defattr(-,root,root,-)
%doc %{_docdir}/%{name}
%{_bindir}/%{oname}Server
%{_bindir}/updatetm
%{_bindir}/import_pootle_prefs
%{_datadir}/%{name}
%{python_sitelib}/%{name}
%{python_sitelib}/%{name}_app
%{python_sitelib}/%{name}_store
%{python_sitelib}/%{name}_notifications
%{python_sitelib}/%{name}_autonotices
%{python_sitelib}/%{name}_misc
%{python_sitelib}/%{name}_terminology
%{python_sitelib}/%{name}_translationproject
%{python_sitelib}/%{name}_profile
%{python_sitelib}/%{name}_project
%{python_sitelib}/%{name}_language
%{python_sitelib}/%{name}_statistics
%{python_sitelib}/profiles
%{python_sitelib}/registration
%{python_sitelib}/contact_form_i18n
%{python_sitelib}/*.egg-info
%{_var}/www/%{name}
%attr(0755,apache,apache) %{_var}/lib/%{name}
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/localsettings.py
%config(noreplace) %{_webappconfdir}/%{name}.conf


%changelog
* Sat Feb 26 2011 Michael Scherer <misc@mandriva.org> 2.1.5-2mdv2011.0
+ Revision: 640101
- use upstream macro name
- drop requires on memcached, as it can work without it
- drop mdv specific macros
- do not ship a copy of djblets, as it is already in another rpm

* Wed Feb 23 2011 Michael Scherer <misc@mandriva.org> 2.1.5-1
+ Revision: 639457
- update to 2.1.5
- remove patch to force memcached by default, and relax requires on it

* Fri Oct 29 2010 Michael Scherer <misc@mandriva.org> 2.0.1-3mdv2011.0
+ Revision: 590174
- rebuild for python 2.7

* Sun Feb 07 2010 Guillaume Rousse <guillomovitch@mandriva.org> 2.0.1-2mdv2010.1
+ Revision: 501749
- rely on filetrigger for reloading apache configuration begining with 2010.1, rpm-helper macros otherwise

* Tue Jan 12 2010 Jérôme Brenier <incubusss@mandriva.org> 2.0.1-1mdv2010.1
+ Revision: 490116
- new version 2.0.1

* Fri Dec 11 2009 Jérôme Brenier <incubusss@mandriva.org> 2.0.0-2mdv2010.1
+ Revision: 476231
- a lot of specfile modifications to fit the new version, based on the work
  of Alaa Abd el Fattah (upstream) (Bugzilla #56293)
- add pootle-2.0-optimal-settings.patch

* Thu Dec 10 2009 Funda Wang <fwang@mandriva.org> 2.0.0-1mdv2010.1
+ Revision: 476202
- fix build
- Bump version requires
- new version 2.0.0

* Tue Sep 15 2009 Thierry Vignaud <tv@mandriva.org> 1.2.1-2mdv2010.0
+ Revision: 441893
- rebuild

* Tue Jan 06 2009 Funda Wang <fwang@mandriva.org> 1.2.1-1mdv2009.1
+ Revision: 326083
- update to new version 1.2.1

* Tue Jan 06 2009 Funda Wang <fwang@mandriva.org> 1.2.0-2mdv2009.1
+ Revision: 325805
- rebuild

* Sat Nov 08 2008 Funda Wang <fwang@mandriva.org> 1.2.0-1mdv2009.1
+ Revision: 301131
- New version 1.2.0

* Mon Jul 14 2008 Funda Wang <fwang@mandriva.org> 1.1.0-1mdv2009.0
+ Revision: 234423
- New version 1.1.0

* Thu Jan 17 2008 Olivier Blin <oblin@mandriva.com> 1.0.2-1mdv2008.1
+ Revision: 154281
- 1.0.2
- remove ElementTree patch, fixed upstream
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Mon Apr 23 2007 Olivier Blin <oblin@mandriva.com> 0.11-1mdv2008.0
+ Revision: 17489
- 0.11


* Fri Jan 12 2007 Olivier Blin <oblin@mandriva.com> 0.10.1-1mdv2007.0
+ Revision: 108075
- move config files in /etc/pootle
- move data files in webapp locations
- fix elementtree import
- initial pootle package
- Create pootle

