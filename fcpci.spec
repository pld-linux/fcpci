#
# SMP will proably *never* work.
#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_with	smp		# build SMP module
%bcond_without	userspace	# don't build userspace programs
%bcond_with	verbose		# verbose build (V=1)
#
%if %{without kernel}
%undefine	with_dist_kernel
%endif
%define		sub_ver	07
%define		_rel	0.1
Summary:	CAPI 2.0 driver of the AVM FRITZ! controller (ISDN TA)
Summary(pl):	Sterownik CAPI 2.0 do kontrolera AVM FRITZ! (ISDN TA)
Name:		kernel-isdn-fcpci
Version:	3.11
Release:	%{_rel}
Epoch:		0
License:	Proprietary, use is permited. Copyright (C) 2002, AVM GmbH. All rights reserved.
Group:		Base/Kernel
Source0:	ftp://ftp.avm.de/cardware/fritzcrd.pci/linux/suse.93/fcpci-suse93-%{version}-%{sub_ver}.tar.gz
# Source0-md5:	3ee301b5d0e8df9e4b915af58b725556
# to be done:
#Source1:	http://www.quiss.org/caiviar/Two-Fritzcards-HOWTO
# Source1-md5:	-
URL:		http://www.avm.de/de/Produkte/FRITZCard/
%if %{with kernel}
%{?with_dist_kernel:BuildRequires:	kernel-module-build >= 2.6.7}
BuildRequires:	rpmbuild(macros) >= 1.217
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is the package "CAPI4Linux" for AVM FRITZ! controlers. In package
you will find following components:
- CAPI 2.0 driver of the controller
- CAPI 2.0 plug-in for the Generic PPP-Stack "pppd"
This package could attend two controlers simultaneously.

%description -l pl
Ten pakiet zawiera CAPI4Linux dla kontrolerów AVM FRITRZ!. W pakiecie
znajduj± siê:
- Sterownik CAPI 2.0
- Wtyczka CAPI 2.0 dla pppd
Ten pakiet mo¿e obs³ugiwaæ dwa kontrolery jednocze¶nie.

%package -n kernel-up-isdn-fcpci
Summary:	Linux driver for fcpci
Summary(pl):	Sterownik dla Linuksa do fcpci
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_up
Requires(postun):	%releq_kernel_up
%endif

%description -n kernel-up-isdn-fcpci
This is driver for fcpci for Linux.

This package contains Linux module.

%description -n kernel-up-isdn-fcpci -l pl
Sterownik dla Linuksa do fcpci.

Ten pakiet zawiera modu³ j±dra Linuksa.

%package -n kernel-smp-isdn-fcpci
Summary:	Linux SMP driver for fcpci
Summary(pl):	Sterownik dla Linuksa SMP do fcpci
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_smp
Requires(postun):	%releq_kernel_smp
%endif

%description -n kernel-smp-isdn-fcpci
This is driver for fcpci for Linux.

This package contains Linux SMP module.

%description -n kernel-smp-isdn-fcpci -l pl
Sterownik dla Linuksa do fcpci.

Ten pakiet zawiera modu³ j±dra Linuksa SMP.

%prep
%setup -q -n fritz

%build
%if %{with userspace}

%endif

%if %{with kernel}
# kernel module(s)
for cfg in %{?with_dist_kernel:%{?with_smp:smp} up}%{!?with_dist_kernel:nondist}; do
	if [ ! -r "%{_kernelsrcdir}/config-$cfg" ]; then
		exit 1
	fi
	rm -rf include
	install -d include/{linux,config}
	ln -sf %{_kernelsrcdir}/config-$cfg .config
	ln -sf %{_kernelsrcdir}/include/linux/autoconf-$cfg.h include/linux/autoconf.h
%ifarch ppc
	if [ -d "%{_kernelsrcdir}/include/asm-powerpc" ]; then
		install -d include/asm
		cp -a %{_kernelsrcdir}/include/asm-%{_target_base_arch}/* include/asm
		cp -a %{_kernelsrcdir}/include/asm-powerpc/* include/asm
	else
		ln -sf %{_kernelsrcdir}/include/asm-%{_target_base_arch} include/asm
	fi
%else
	ln -sf %{_kernelsrcdir}/include/asm-%{_target_base_arch} include/asm
%endif
	ln -sf %{_kernelsrcdir}/Module.symvers-$cfg Module.symvers
	touch include/config/MARKER
	%{__make} -C %{_kernelsrcdir} clean \
		RCS_FIND_IGNORE="-name '*.ko' -o" \
		M=$PWD O=$PWD \
		%{?with_verbose:V=1}
	%{__make} -C %{_kernelsrcdir} modules \
		CC="%{__cc}" CPP="%{__cpp}" \
		M=$PWD O=$PWD \
		%{?with_verbose:V=1}

	mv fcpci1{,-$cfg}.ko
	mv fcpci2{,-$cfg}.ko
done
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with userspace}

%endif

%if %{with kernel}
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/isdn/hardware

install fcpci1-%{?with_dist_kernel:up}%{!?with_dist_kernel:nondist}.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/isdn/hardware/fcpci1.ko

install fcpci2-%{?with_dist_kernel:up}%{!?with_dist_kernel:nondist}.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/isdn/hardware/fcpci2.ko

%if %{with smp} && %{with dist_kernel}
install fcpci-smp.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/isdn/hardware/fcpci.ko
%endif
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel-up-isdn-fcpci
%depmod %{_kernel_ver}

%postun	-n kernel-up-isdn-fcpci
%depmod %{_kernel_ver}

%post	-n kernel-smp-isdn-fcpci
%depmod %{_kernel_ver}smp

%postun	-n kernel-smp-isdn-fcpci
%depmod %{_kernel_ver}smp

%if %{with userspace}
%endif


%if %{with kernel}
%files -n kernel-isdn-fcpci
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/isdn/hardware/*.ko*
%doc CAPI20_Errormessages.txt license.txt *.html

%if %{with smp} && %{with dist_kernel}
%files -n kernel-smp-isdn-fcpci
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/isdn/hardware/*.ko*
%endif
%endif
