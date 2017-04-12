%{?scl:%scl_package python-setuptools}
%{!?scl:%global pkg_name %{name}}

%global build_wheel 0
%if 0%{?rhel} && 0%{?rhel} < 6
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif

%global srcname pip
%if 0%{?build_wheel}
%global python2_wheelname %{srcname}-%{version}-py2.py3-none-any.whl
%endif

%global bashcompdir %(b=$(pkg-config --variable=completionsdir bash-completion 2>/dev/null); echo ${b:-%{_sysconfdir}/bash_completion.d})
%if "%{bashcompdir}" != "%{_sysconfdir}/bash_completion.d"
%global bashcomp2 1
%endif

Name:           %{?scl_prefix}python-%{srcname}
Version:        8.1.2
Release:        1%{?dist}
Summary:        A tool for installing and managing Python packages

Group:          Development/Libraries
License:        MIT
URL:            http://www.pip-installer.org
Source0:        https://files.pythonhosted.org/packages/source/p/pip/%{srcname}-%{version}.tar.gz
Patch0:         allow-stripping-given-prefix-from-wheel-RECORD-files.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  %{?scl_prefix}python-devel
BuildRequires:  %{?scl_prefix}python-setuptools
%if 0%{?build_wheel}
BuildRequires:  %{?scl_prefix}python-pip
BuildRequires:  %{?scl_prefix}python-wheel
%endif
Requires:       %{?scl_prefix}python-setuptools

%description
Pip is a replacement for `easy_install
<http://peak.telecommunity.com/DevCenter/EasyInstall>`_.  It uses mostly the
same techniques for finding packages, so packages that were made
easy_installable should be pip-installable as well.



%prep
%{?scl:scl enable %{scl} - << \EOF}
%setup -q -n %{srcname}-%{version}

%patch0 -p1

%{__sed} -i '1d' pip/__init__.py
%{?scl:EOF}


%build
%{?scl:scl enable %{scl} - << \EOF}
%if 0%{?build_wheel}
%{__python2} setup.py bdist_wheel
%else
%{__python2} setup.py build
%endif
%{?scl:EOF}


%install
%{__rm} -rf %{buildroot}

%{?scl:scl enable %{scl} - << \EOF}
%if 0%{?build_wheel}
pip2 install -I dist/%{python2_wheelname} --root %{buildroot} --strip-file-prefix %{buildroot}
%else
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}
%endif

mkdir -p %{buildroot}%{bashcompdir}
PYTHONPATH=%{buildroot}%{python_sitelib} \
    %{buildroot}%{_bindir}/pip completion --bash \
    > %{buildroot}%{bashcompdir}/pip
pips2=pip
for pip in %{buildroot}%{_bindir}/pip*; do
    pip=$(basename $pip)
    case $pip in
        pip2*)
            pips2="$pips2 $pip"
%if 0%{?bashcomp2}
            ln -s pip %{buildroot}%{bashcompdir}/$pip
%endif
    esac
done

sed -i -e "s/^\\(complete.*\\) pip\$/\\1 $pips2/" \
    %{buildroot}%{bashcompdir}/pip
%{?scl:EOF}

%clean
%{__rm} -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc README.rst LICENSE.txt docs
%attr(755,root,root) %{_bindir}/pip
%attr(755,root,root) %{_bindir}/pip2*
%{python_sitelib}/pip*
%{bashcompdir}
%if 0%{?bashcomp2}
%dir %(dirname %{bashcompdir})
%endif


%changelog
* Mon Jan 16 2017 Tomas Orsava <torsava@redhat.com> - 8.1.2-1
- Rebased to 8.1.2
- Updated to a new PyPI source URL
- Rebased and renamed prefix-stripping Patch 0
Resolves: rhbz#1344674

* Tue May 10 2016 Charalampos Stratakis <cstratak@redhat.com> - 7.1.0-2
- Change license tag to doc tag so directory is owned by the collection
- Will revert when ownership of directories is defined in scl-utils-build package
Resolves: rhbz#1334447

* Mon Feb 15 2016 Charalampos Stratakis <cstratak@redhat.com> - 7.1.0-1
- Update to 7.1.0 
Resolves: rhbz#1255516

* Tue Jan 20 2015 Slavek Kabrda <bkabrda@redhat.com> - 1.5.6-5
- Rebuild for python27 (not as wheel)
Resolves: rhbz#994189

* Mon Jan 19 2015 Matej Stuchlik <mstuchli@redhat.com> - 1.5.6-4
- Rebuild as wheel

* Tue Nov 18 2014 Matej Stuchlik <mstuchli@redhat.com> - 1.5.6-3
- Added patch for local dos with predictable temp dictionary names
  (http://seclists.org/oss-sec/2014/q4/655)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun May 25 2014 Matej Stuchlik <mstuchli@redhat.com> - 1.5.6-1
- Update to 1.5.6

* Fri Apr 25 2014 Matej Stuchlik <mstuchli@redhat.com> - 1.5.4-4
- Rebuild as wheel for Python 3.4

* Thu Apr 24 2014 Matej Stuchlik <mstuchli@redhat.com> - 1.5.4-3
- Disable build_wheel

* Thu Apr 24 2014 Matej Stuchlik <mstuchli@redhat.com> - 1.5.4-2
- Rebuild as wheel for Python 3.4

* Mon Apr 07 2014 Matej Stuchlik <mstuchli@redhat.com> - 1.5.4-1
- Updated to 1.5.4

* Mon Oct 14 2013 Tim Flink <tflink@fedoraproject.org> - 1.4.1-1
- Removed patch for CVE 2013-2099 as it has been included in the upstream 1.4.1 release
- Updated version to 1.4.1

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 16 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 1.3.1-4
- Fix for CVE 2013-2099

* Thu May 23 2013 Tim Flink <tflink@fedoraproject.org> - 1.3.1-3
- undo python2 executable rename to python-pip. fixes #958377
- fix summary to match upstream

* Mon May 06 2013 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1.3.1-2
- Fix main package Summary, it's for Python 2, not 3 (#877401)

* Fri Apr 26 2013 Jon Ciesla <limburgher@gmail.com> - 1.3.1-1
- Update to 1.3.1, fix for CVE-2013-1888.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Oct 09 2012 Tim Flink <tflink@fedoraproject.org> - 1.2.1-2
- Fixing files for python3-pip

* Thu Oct 04 2012 Tim Flink <tflink@fedoraproject.org> - 1.2.1-1
- Update to upstream 1.2.1
- Change binary from pip-python to python-pip (RHBZ#855495)
- Add alias from python-pip to pip-python, to be removed at a later date

* Tue May 15 2012 Tim Flink <tflink@fedoraproject.org> - 1.1.0-1
- Update to upstream 1.1.0

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Oct 22 2011 Tim Flink <tflink@fedoraproject.org> - 1.0.2-1
- update to 1.0.2 and added python3 subpackage

* Wed Jun 22 2011 Tim Flink <tflink@fedoraproject.org> - 0.8.3-1
- update to 0.8.3 and project home page

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Luke Macken <lmacken@redhat.com> - 0.8.2-1
- update to 0.8.2 of pip
* Mon Aug 30 2010 Peter Halliday <phalliday@excelsiorsystems.net> - 0.8-1
- update to 0.8 of pip
* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.7.2-5
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed Jul 7 2010 Peter Halliday <phalliday@excelsiorsystems.net> - 0.7.2-1
- update to 0.7.2 of pip
* Sun May 23 2010 Peter Halliday <phalliday@excelsiorsystems.net> - 0.7.1-1
- update to 0.7.1 of pip
* Fri Jan 1 2010 Peter Halliday <phalliday@excelsiorsystems.net> - 0.6.1.4
- fix dependency issue
* Fri Dec 18 2009 Peter Halliday <phalliday@excelsiorsystems.net> - 0.6.1-2
- fix spec file 
* Thu Dec 17 2009 Peter Halliday <phalliday@excelsiorsystems.net> - 0.6.1-1
- upgrade to 0.6.1 of pip
* Mon Aug 31 2009 Peter Halliday <phalliday@excelsiorsystems.net> - 0.4-1
- Initial package
