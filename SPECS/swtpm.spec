%global package_speccommit d5884125494924fcadf7ab03add5825b6e6612c0
%global usver 0.7.3
%global xsver 2
%global xsrel %{xsver}%{?xscount}%{?xshash}
%global package_srccommit v0.7.3

Summary: TPM Emulator
Name:           swtpm
Version:        0.7.3
Release: %{?xsrel}%{?dist}
License:        BSD
Source0: swtpm-0.7.3.tar.gz
Patch0: gnutls-compat.patch
Patch1: chroot.patch
Patch2: set-localca-options.patch

BuildRequires:  git-core
BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  libtool
BuildRequires:  libtpms-devel >= 0.6.0
BuildRequires:  glib2-devel
BuildRequires:  json-glib-devel
BuildRequires:  expect
BuildRequires:  net-tools
BuildRequires:  openssl-devel
BuildRequires:  socat
BuildRequires:  trousers >= 0.3.9
BuildRequires:  softhsm
BuildRequires:  gnutls >= 3.1.0
BuildRequires:  gnutls-devel
BuildRequires:  gnutls-utils
BuildRequires:  libtasn1-devel
BuildRequires:  libtasn1
BuildRequires:  gcc
BuildRequires:  libseccomp-devel
BuildRequires:  python3-devel
%{?_cov_buildrequires}

Requires:       %{name}-libs = %{version}-%{release}
Requires:       libtpms >= 0.6.0

%description
TPM emulator built on libtpms providing TPM functionality for QEMU VMs

%package        libs
Summary:        Common libraries for TPM emulators
Group:          System Environment/Libraries
License:        BSD

%description    libs
A library with callback functions for libtpms based TPM emulator

%package        devel
Summary:        Include files for the TPM emulator's CUSE interface for usage by clients
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
Include files for the TPM emulator's CUSE interface.

%package        tools
Summary:        Tools for the TPM emulator
License:        BSD
Group:          Applications/Emulators
Requires:       swtpm = %{version}-%{release}
Requires:       trousers >= 0.3.9 bash gnutls-utils

%description    tools
Tools for the TPM emulator from the swtpm package

%files
%doc LICENSE README
%{_bindir}/swtpm
%{_mandir}/man8/swtpm.8*

%files libs
%doc LICENSE README
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/libswtpm_libtpms.so.0
%{_libdir}/%{name}/libswtpm_libtpms.so.0.0.0

%files devel
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*.h
%{_mandir}/man3/swtpm_ioctls.3*

%files tools
%doc README
%{_bindir}/swtpm_bios
%{_bindir}/swtpm_cert
%{_bindir}/swtpm_setup
%{_bindir}/swtpm_ioctl
%{_bindir}/swtpm_localca
%{_mandir}/man8/swtpm_bios.8*
%{_mandir}/man8/swtpm_cert.8*
%{_mandir}/man8/swtpm_ioctl.8*
%{_mandir}/man8/swtpm-localca.conf.8*
%{_mandir}/man8/swtpm-localca.options.8*
%{_mandir}/man8/swtpm-localca.8*
%{_mandir}/man8/swtpm_localca.8*
%{_mandir}/man8/swtpm_setup.8*
%{_mandir}/man8/swtpm_setup.conf.8*
%config(noreplace) %{_sysconfdir}/swtpm_setup.conf
%config(noreplace) %{_sysconfdir}/swtpm-localca.options
%config(noreplace) %{_sysconfdir}/swtpm-localca.conf
%dir %{_datadir}/swtpm
%{_datadir}/swtpm/swtpm-localca
%{_datadir}/swtpm/swtpm-create-user-config-files
%attr( 750, tss, root) %{_localstatedir}/lib/swtpm-localca

%prep
%autosetup -p1
%{?_cov_prepare}

%build
NOCONFIGURE=1 ./autogen.sh
%configure --with-gnutls --without-cuse CFLAGS="$CFLAGS -DDEBUG"

%{?_cov_wrap} %make_build

%check
make %{?_smp_mflags} check VERBOSE=1

%install

%make_install
rm -f %{buildroot}%{_libdir}/%{name}/*.{a,la,so}
rm -f %{buildroot}%{_mandir}/man8/swtpm-create-tpmca.8*
rm -f %{buildroot}%{_datadir}/%{name}/swtpm-create-tpmca
%{?_cov_install}

%ldconfig_post libs
%ldconfig_postun libs

%{?_cov_results_package}

%changelog
* Tue Aug 23 2022 Ross Lagerwall <ross.lagerwall@citrix.com> - 0.7.3-2
- CP-39549: Configure defaults for swtpm_localca
- CA-363859: Make compatible with GnuTLS 3.3
- Fix debuginfo generation

* Fri May 13 2022 Ross Lagerwall <ross.lagerwall@citrix.com> - 0.7.3-1
- CA-366149: Update to 0.7.3 to fix CVE-2022-23645

* Thu Apr 07 2022 Edwin Török <edvin.torok@citrix.com> - 0.7.0-3
- CP-35054: Add chroot option

* Fri Feb 18 2022 Igor Druzhinin <igor.druzhinin@citrix.com> - 0.7.0-2
- Enable static analysis
- Use python3 for build tests
* Fri Jan 07 2022 Igor Druzhinin <igor.druzhinin@citrix.com> - 0.7.0-1
- Update swtpm to v0.7.0
* Tue Aug 11 2020 Stefan Berger <stefanb@linux.ibm.com> - 0.3.4-1
- Update to v0.3.4 release
