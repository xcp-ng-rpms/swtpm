%global package_speccommit 5c91a9b4792948b5155dd73c01a65a5272aded2e
%global usver 0.7.3
%global xsver 12
%global xsrel %{xsver}%{?xscount}%{?xshash}
%global package_srccommit v0.7.3

Summary: TPM Emulator
Name:           swtpm
Version:        0.7.3
Release: %{?xsrel}.1~XCPNG2710.4%{?dist}
License:        BSD
Source0: swtpm-0.7.3.tar.gz
Patch0: swtpm_setup-Configure-swtpm-to-log-to-stdout-err-if-.patch
Patch1: swtpm-Add-a-chroot-option.patch
Patch2: tests-If-filesystem-is-mounted-with-nodev-opt-skip-C.patch
Patch3: swtpm-Advertise-the-chroot-option-with-cmdarg-chroot.patch
Patch4: 0001-Make-stdout-unbuffered-in-swtpm_-setup-localca.patch
Patch5: 0001-swtpm-Remove-assignment-to-unused-variable.patch
Patch6: 0001-swtpm-Fix-memory-leak-in-case-realloc-fails.patch
Patch7: 0001-swtpm_cert-Test-for-NULL-pointer-returned-by-malloc.patch
Patch8: 0001-swtpm-Close-fd-after-main-loop.patch
Patch9: 0002-swtpm-Fix-double-free-in-error-path.patch
Patch10: gnutls-compat.patch
Patch11: set-localca-options.patch
Patch12: add-http-backend.patch

%if 0%{?xenserver} >= 9
# Prevent crypto policies disabling SHA-1.
# swtpm algorithm list is unconditional. Since it advertizes
# SHA-1, we MUST always provide a working SHA-1 impl
Source1:        openssl-swtpm.cnf
%endif

BuildRequires:  git-core
BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  libtool
BuildRequires:  libtpms-devel >= 0.6.0
BuildRequires:  glib2-devel
BuildRequires:  json-glib-devel
BuildRequires:  expect
BuildRequires:  iproute
BuildRequires:  openssl-devel
BuildRequires:  socat
BuildRequires:  gnutls >= 3.1.0
BuildRequires:  gnutls-devel
BuildRequires:  gnutls-utils
BuildRequires:  libtasn1-devel
BuildRequires:  libtasn1
BuildRequires:  gcc
BuildRequires:  libseccomp-devel
BuildRequires:  python3-devel
BuildRequires:  libcurl-devel
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
Requires:       bash gnutls-utils

%description    tools
Tools for the TPM emulator from the swtpm package

%files
%doc LICENSE README
%{_bindir}/swtpm
%{_mandir}/man8/swtpm.8*
%if 0%{?xenserver} >= 9
%{_sysconfdir}/ssl/openssl-swtpm.cnf
%endif

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
# RPM uses patch which doesn't apply file permissions for these new files so
# add the execute bit here.
chmod 755 tests/test_tpm2_chroot_chardev
chmod 755 tests/test_tpm2_chroot_cuse
chmod 755 tests/test_tpm2_chroot_socket

make %{?_smp_mflags} check VERBOSE=1

%install

%make_install
rm -f %{buildroot}%{_libdir}/%{name}/*.{a,la,so}
rm -f %{buildroot}%{_mandir}/man8/swtpm-create-tpmca.8*
rm -f %{buildroot}%{_datadir}/%{name}/swtpm-create-tpmca

%if 0%{?xenserver} >= 9
%__install -d %{buildroot}%{_sysconfdir}/ssl
cp %{SOURCE1} %{buildroot}/%{_sysconfdir}/ssl/
%endif

%{?_cov_install}

%ldconfig_post libs
%ldconfig_postun libs

%{?_cov_results_package}

%changelog
* Mon Jan 26 2026 Philippe Coval <philippe.coval@vates.tech> - 0.7.3-12.1
- Rebuild on openssl-3

* Wed Mar 19 2025 Ross Lagerwall <ross.lagerwall@citrix.com> - 0.7.3-12
- CA-407177: Prevent crypto-policies disabling SHA1

* Fri Jan 31 2025 Ross Lagerwall <ross.lagerwall@citrix.com> - 0.7.3-11
- CA-405654: Fix running with newer versions of cURL

* Wed Jan 22 2025 Alex Brett <alex.brett@cloud.com> - 0.7.3-10
- CP-53343: Replace net-tools with iproute

* Thu Oct 10 2024 Stephen Cheng <stephen.cheng@cloud.com> - 0.7.3-9
- CP-51608: Removed softhsm from BuildRequres

* Thu Mar 14 2024 Ross Lagerwall <ross.lagerwall@citrix.com> - 0.7.3-8
- Add gnutls-compat.patch back to make compatible with xs8/xs9
- CA-377995: Fix static analysis warnings

* Thu Nov 23 2023 Ross Lagerwall <ross.lagerwall@citrix.com> - 0.7.3-7
- CA-383866: Retry HTTP requests to avoid a failure

* Mon Sep 11 2023 Lin Liu <Lin.Liu01@citrix.com> - 0.7.3-6
- CP-45247: Remove gnutls-compat.patch and build for xs9

* Wed Aug 02 2023 Ross Lagerwall <ross.lagerwall@citrix.com> - 0.7.3-5
- CA-380178: Make stdout unbuffered in swtpm_{setup,localca}

* Wed Jun 07 2023 Edwin Török <edvin.torok@citrix.com> - 0.7.3-4
- Fix http method and parameter mismatch
- fix missing \n in logprintf

* Wed May 31 2023 Edwin Török <edwin.torok@cloud.com> - 0.7.3-3
- CA-371900: Capture output from swtpm during setup
- Replace patch with upstream backports
- CP-43409: update TPM manufacturer
- CP-42059: Use simpler HTTP based REST API

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
