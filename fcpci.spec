#
# SMP will proably *never* work.
#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_without	userspace	# don't build userspace programs
%bcond_with	verbose		# verbose build (V=1)
#
%if !%{with kernel}
%undefine	with_dist_kernel
%endif
%define		sub_ver	07
%define		_rel	0.2
Summary:	CAPI 2.0 driver of the AVM FRITZ! controller (ISDN TA)
Summary(pl.UTF-8):	Sterownik CAPI 2.0 do kontrolera AVM FRITZ! (ISDN TA)
Name:		fcpci
Version:	3.11
Release:	%{_rel}
Epoch:		0
License:	Proprietary (non-distributable) with LGPL v2.1+ part
Group:		Base/Kernel
Source0:	ftp://ftp.avm.de/cardware/fritzcrd.pci/linux/suse.93/%{name}-suse93-%{version}-%{sub_ver}.tar.gz
# NoSource0-md5:	3ee301b5d0e8df9e4b915af58b725556
# to be done:
#Source1:	http://www.quiss.org/caiviar/Two-Fritzcards-HOWTO
# Source1-md5:	-
NoSource:	0
Patch0:		%{name}-Makefile.patch
URL:		http://www.avm.de/de/Produkte/FRITZCard/
%if %{with kernel}
%{?with_dist_kernel:BuildRequires:	kernel-module-build >= 3:2.6.7}
BuildRequires:	rpmbuild(macros) >= 1.217
%endif
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is the package "CAPI4Linux" for AVM FRITZ! controlers. In package
you will find following components:
- CAPI 2.0 driver of the controller
- CAPI 2.0 plug-in for the Generic PPP-Stack "pppd" (missing)

This package could attend two controlers simultaneously.

%description -l pl.UTF-8
Ten pakiet zawiera CAPI4Linux dla kontrolerów AVM FRITRZ!. W pakiecie
znajdują się:
- Sterownik CAPI 2.0
- Wtyczka CAPI 2.0 dla pppd (brakująca)

Ten pakiet może obsługiwać dwa kontrolery jednocześnie.

%package -n kernel%{_alt_kernel}-isdn-fcpci
Summary:	Linux driver for fcpci
Summary(pl.UTF-8):	Sterownik dla Linuksa do fcpci
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif

%description -n kernel%{_alt_kernel}-isdn-fcpci
This is driver for fcpci for Linux.

This package contains Linux kernel module.

%description -n kernel%{_alt_kernel}-isdn-fcpci -l pl.UTF-8
Sterownik dla Linuksa do fcpci.

Ten pakiet zawiera moduł jądra Linuksa.

%prep
%setup -q -n fritz
%patch -P0 -p1

%build
%if %{with kernel}
%build_kernel_modules -m fcpci{1,2}
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with kernel}
%install_kernel_modules -m fcpci{1,2} -d isdn/hardware
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel%{_alt_kernel}-isdn-fcpci
%depmod %{_kernel_ver}

%postun	-n kernel%{_alt_kernel}-isdn-fcpci
%depmod %{_kernel_ver}

%if %{with kernel}
%files -n kernel%{_alt_kernel}-isdn-fcpci
%defattr(644,root,root,755)
%doc CAPI20_Errormessages.txt license.txt *.html
/lib/modules/%{_kernel_ver}/isdn/hardware/*.ko*
%endif
