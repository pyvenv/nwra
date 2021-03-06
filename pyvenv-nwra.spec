%global envname nwra

Name:		pyvenv-%{envname}
Version:	1.0
Release:	5%{?dist}
Summary:	NWRA python environment
License:	GPLv3+

%if 0%{?rhel} && 0%{?rhel} == 6
Requires:       environment-modules
%else
BuildRequires:  python-virtualenv
Requires:       environment(modules)
%endif

%description
NWRA python environment.

%package devel
Summary:	NWRA python environment development files
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
NWRA python environment development files.

%install
mkdir -p %{buildroot}/opt/pyvenv/%{envname}-%{version}
virtualenv --system-site-packages --no-setuptools %{buildroot}/opt/pyvenv/%{envname}-%{version}
virtualenv --relocatable %{buildroot}/opt/pyvenv/%{envname}-%{version}
# Fixup buildroot
find %{buildroot} -type f -exec sed -i -e 's|%{buildroot}||g' '{}' +

# Needs to be in /etc to override EL python macros
mkdir -p %{buildroot}/etc/rpm
cat > %{buildroot}/etc/rpm/macros.zz-nwra-pyvenv << 'EOF'
# Maybe set _exec_prefix which also sets _libexecdir, _sbindir
# Setting _prefix breaks ipython build which links in files from _jsdir and _datadir
%%_bindir /opt/pyvenv/%{envname}-%{version}/bin
%%_mandir /opt/pyvenv/%{envname}-%{version}/share/man
%%__python /opt/pyvenv/%{envname}-%{version}/bin/python
%%__python2 /opt/pyvenv/%{envname}-%{version}/bin/python2
%%pyvenv_name_prefix pyvenv-%{envname}-
EOF

mkdir -p %{buildroot}/usr/share/Modules/modulefiles/pyvenv/%{envname}
cat > %{buildroot}/usr/share/Modules/modulefiles/pyvenv/%{envname}/%{version} << 'EOF'
#%Module 1.0

set prefix /opt/pyvenv/%{envname}-%{version}

prepend-path    PATH    $prefix/bin
prepend-path    PYTHONPATH    $prefix/lib/python2.7/site-packages
EOF


%files
/usr/share/Modules/modulefiles/pyvenv/%{envname}/%{version}
/opt/pyvenv/%{envname}-%{version}

%files devel
/etc/rpm/macros.zz-nwra-pyvenv


%changelog
* Mon May 11 2015 Orion Poplawski <orion@cora.nwra.com> - 1.0-5
- Set %%_mandir

* Mon May 11 2015 Orion Poplawski <orion@cora.nwra.com> - 1.0-4
- Set %%_bindir instead of %%_prefix

* Mon May 11 2015 Orion Poplawski <orion@cora.nwra.com> - 1.0-3
- Add %%_prefix, %%__python to rpm macros

* Fri May 8 2015 Orion Poplawski <orion@cora.nwra.com> - 1.0-2
- Drop base, add -devel package

* Thu May 7 2015 Orion Poplawski <orion@cora.nwra.com> - 1.0-1
- Initial package
