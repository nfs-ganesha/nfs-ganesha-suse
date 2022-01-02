
%global _hardened_build 1

%if ( 0%{?suse_version} )
BuildRequires: distribution-release
%if ( ! 0%{?is_opensuse} )
BuildRequires: sles-release >= 12
Requires: sles-release >= 12
%else
BuildRequires: openSUSE-release
Requires: openSUSE-release
%endif
%endif

# Conditionally enable some FSALs, disable others.
#
# 1. rpmbuild accepts these options (gpfs as example):
#    --with gpfs
#    --without gpfs

%define on_off_switch() %%{?with_%1:ON}%%{!?with_%1:OFF}

# A few explanation about %%bcond_with and %%bcond_without
# /!\ be careful: this syntax can be quite messy
# %%bcond_with means you add a "--with" option, default = without this feature
# %%bcond_without adds a"--without" so the feature is enabled by default

%bcond_without nullfs
%global use_fsal_null %{on_off_switch nullfs}

%bcond_with mem
%global use_fsal_mem %{on_off_switch mem}

%bcond_without gpfs
%global use_fsal_gpfs %{on_off_switch gpfs}

%bcond_with xfs
%global use_fsal_xfs %{on_off_switch xfs}

%bcond_with lustre
%global use_fsal_lustre %{on_off_switch lustre}

%ifarch x86_64
%bcond_without ceph
%else
%bcond_with ceph
%endif
%global use_fsal_ceph %{on_off_switch ceph}

%ifarch x86_64
%bcond_with rgw
%else
%bcond_with rgw
%endif
%global use_fsal_rgw %{on_off_switch rgw}

%bcond_without gluster
%global use_fsal_gluster %{on_off_switch gluster}

%bcond_with kvsfs
%global use_fsal_kvsfs %{on_off_switch kvsfs}

%bcond_with rdma
%global use_rdma %{on_off_switch rdma}

%bcond_with 9P
%global use_9P %{on_off_switch 9P}

%bcond_with jemalloc

%bcond_with lttng
%global use_lttng %{on_off_switch lttng}

%bcond_without utils
%global use_utils %{on_off_switch utils}

%bcond_without gui_utils
%global use_gui_utils %{on_off_switch gui_utils}

%bcond_without system_ntirpc
%global use_system_ntirpc %{on_off_switch system_ntirpc}

%bcond_without man_page
%global use_man_page %{on_off_switch man_page}

%ifarch x86_64
%bcond_without rados_recov
%else
%bcond_with rados_recov
%endif
%global use_rados_recov %{on_off_switch rados_recov}
 
%ifarch x86_64
%bcond_without rados_urls
%else
%bcond_with rados_urls
%endif
%global use_rados_urls %{on_off_switch rados_urls}

%bcond_without rpcbind
%global use_rpcbind %{on_off_switch rpcbind}

%bcond_without mspac_support
%global use_mspac_support %{on_off_switch mspac_support}

%if ( 0%{?rhel} && 0%{?rhel} < 7 )
%global _rundir %{_localstatedir}/run
%endif

%global dev_version %{lua: s = string.gsub('@GANESHA_EXTRA_VERSION@', '^%-', ''); s2 = string.gsub(s, '%-', '.'); print(s2) }
# %%global	dev final
# %%global	dash_dev_version 2.5-final

Name:		nfs-ganesha
Version:	4.0
Release:	1%{?dev:%{dev}}%{?dist}
Summary:	NFS-Ganesha is a NFS Server running in user space
Group:		System/Filesystems
License:	LGPL-3.0+
Url:		https://github.com/nfs-ganesha/nfs-ganesha/wiki

Source0:	https://github.com/%{name}/%{name}/archive/V%{version}/%{name}-%{version}.tar.gz
Patch2:		0002-CMakeLists.txt.patch

BuildRequires:	cmake
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	pkgconfig
BuildRequires:	liburcu-devel
BuildRequires:	krb5-devel
%if ( 0%{?suse_version} >= 1330 )
BuildRequires:  libnsl-devel
%endif
%if ( 0%{?suse_version} )
BuildRequires:	dbus-1-devel
Requires:	dbus-1
BuildRequires:	systemd-rpm-macros
#!BuildIgnore:	openssl
%else
BuildRequires:	dbus-devel
Requires:	dbus
%endif
BuildRequires:	libcap-devel
BuildRequires:	libblkid-devel
BuildRequires:	libuuid-devel
BuildRequires:	gcc-c++
%if ( 0%{?with_mspac_support} )
BuildRequires: libwbclient-devel
%endif
%if ( %{with_system_ntirpc} )
BuildRequires:	libntirpc-devel >= 4.0
%endif
%if ( 0%{?fedora} )
# this should effectively be a no-op, as all Fedora installs should have it
# with selinux.
Requires:	policycoreutils-python
%endif
Requires:	nfs-utils
%if ( 0%{?with_rpcbind} )
%if ( 0%{?fedora} ) || ( 0%{?rhel} && 0%{?rhel} >= 6 ) || ( 0%{?suse_version} )
Requires:	rpcbind
%else
Requires:	portmap
%endif
%endif
%if ( 0%{?suse_version} )
BuildRequires:	nfsidmap-devel
%else
BuildRequires:	libnfsidmap-devel
%endif
%if %{with rdma}
BuildRequires:	libmooshika-devel >= 0.6-0
%endif
%if %{with jemalloc}
BuildRequires:	jemalloc-devel
%endif
BuildRequires: systemd-mini
Requires(post): systemd-mini
Requires(preun): systemd-mini
Requires(postun): systemd-mini
%if %{with man_page}
BuildRequires: python38-Sphinx
%endif
Requires(post): psmisc
Requires(pre): /usr/sbin/useradd
Requires(pre): /usr/sbin/groupadd

# Use CMake variables

%description
nfs-ganesha : NFS-GANESHA is a NFS Server running in user space.
It comes with various back-end modules (called FSALs) provided as
shared objects to support different file systems and name-spaces.

%if %{with 9P}
%package mount-9P
Summary:	A 9p mount helper
Group:		System/Filesystems

%description mount-9P
This package contains the mount.9P script that clients can use
to simplify mounting to NFS-GANESHA. This is a 9p mount helper.
%endif

%package vfs
Summary:	The NFS-GANESHA's VFS FSAL
Group:		System/Filesystems
BuildRequires:	libattr-devel
Obsoletes:	%{name}-xfs <= %{version}
Requires:	nfs-ganesha = %{version}-%{release}

%description vfs
This package contains a FSAL shared object to
be used with NFS-Ganesha to support VFS based filesystems

%package proxy-v4
Summary:	The NFS-GANESHA's PROXY_V4 FSAL
Group:		System/Filesystems
BuildRequires:	libattr-devel
Requires:	nfs-ganesha = %{version}-%{release}

%description proxy-v4
This package contains a FSAL shared object to
be used with NFS-Ganesha to support PROXY_V4 based filesystems

%if %{with utils}
%package utils
Summary:	The NFS-GANESHA's util scripts
Group:		System/Filesystems
%if ( 0%{?suse_version} )
BuildRequires:	python3-devel
Requires:	dbus-1-python, python3-gobject2 python3-pyparsing
Requires:	gpfs.nfs-ganesha = %{version}-%{release}, python3
%else
Requires:	dbus-python, pygobject2, pyparsing
%endif
%if %{with gui_utils}
%if ( 0%{?suse_version} )
BuildRequires:	python-qt5-devel
Requires:	python-qt5
%else
BuildRequires:	PyQt5-devel
Requires:	PyQt5
%endif
%endif

%description utils
This package contains utility scripts for managing the NFS-GANESHA server
%endif

%if %{with lttng}
%package lttng
Summary:	The NFS-GANESHA's library for use with LTTng
Group:		System/Filesystems
BuildRequires:	lttng-ust-devel >= 2.3
BuildRequires:	lttng-tools-devel >= 2.3
Requires:	nfs-ganesha = %{version}-%{release}

%description lttng
This package contains the libganesha_trace.so library. When preloaded
to the ganesha.nfsd server, it makes it possible to trace using LTTng.
%endif

%if %{with rados_recov}
%package rados-grace
Summary:	The NFS-GANESHA's command for managing the RADOS grace database
Group:		System/Filesystems
BuildRequires:	librados-devel >= 14.2.1
Requires:	nfs-ganesha = %{version}-%{release}

%description rados-grace
This package contains the ganesha-rados-grace tool for interacting with the
database used by the rados_cluster recovery backend and the
libganesha_rados_grace shared library for using RADOS storage for
recovery state.
%endif
 
%if %{with rados_urls}
%package rados-urls
Summary: The NFS-GANESHA library for use with RADOS URLs
Group: Applications/System
Requires: nfs-ganesha = %{version}-%{release}

%description rados-urls
This package contains the libganesha_rados_urls library used for
handling RADOS URL configurations.
%endif

# Option packages start here. use "rpmbuild --with gpfs" (or equivalent)
# for activating this part of the spec file

# NULL
%if %{with nullfs}
%package nullfs
Summary:	The NFS-GANESHA's NULLFS Stackable FSAL
Group:		System/Filesystems
Requires:	nfs-ganesha = %{version}-%{release}

%description nullfs
This package contains a Stackable FSAL shared object to
be used with NFS-Ganesha. This is mostly a template for future (more sophisticated) stackable FSALs
%endif

# MEM
%if %{with mem}
%package mem
Summary:	The NFS-GANESHA's Memory backed testing FSAL
Group:		System/Filesystems
Requires:	nfs-ganesha = %{version}-%{release}

%description mem
This package contains a FSAL shared object to be used with NFS-Ganesha. This
is used for speed and latency testing.
%endif

# GPFS
%if %{with gpfs}
%package gpfs
Summary:	The NFS-GANESHA's GPFS FSAL
Group:		System/Filesystems
Requires:	nfs-ganesha = %{version}-%{release}

%description gpfs
This package contains a FSAL shared object to
be used with NFS-Ganesha to support GPFS backend
%endif

# CEPH
%ifnarch i686 armv7hl ppc64
%if %{with ceph}
%package ceph
Summary:	The NFS-GANESHA's CephFS FSAL
Group:		System/Filesystems
Requires:	nfs-ganesha = %{version}-%{release}
BuildRequires:	libcephfs-devel >= 14.2.1
BuildRequires:	libacl-devel

%description ceph
This package contains a FSAL shared object to
be used with NFS-Ganesha to support CephFS
%endif

# RGW
%if %{with rgw}
%package rgw
Summary:	The NFS-GANESHA's Ceph RGW FSAL
Group:		System/Filesystems
Requires:	nfs-ganesha = %{version}-%{release}
BuildRequires:	librgw-devel >= 14.2.1

%description rgw
This package contains a FSAL shared object to
be used with NFS-Ganesha to support Ceph RGW
%endif
%endif

# XFS
%if %{with xfs}
%package xfs
Summary:	The NFS-GANESHA's XFS FSAL
Group:		System/Filesystems
Requires:	nfs-ganesha = %{version}-%{release}
BuildRequires:	libattr-devel xfsprogs-devel

%description xfs
This package contains a shared object to be used with FSAL_VFS
to support XFS correctly
%endif

#LUSTRE
%if %{with lustre}
%package lustre
Summary:	The NFS-GANESHA's LUSTRE FSAL
Group:		System/Filesystems
BuildRequires: libattr-devel
BuildRequires: lustre-client
Requires: nfs-ganesha = %{version}-%{release}
Requires: lustre-client

%description lustre
This package contains a FSAL shared object to
be used with NFS-Ganesha to support LUSTRE based filesystems
%endif

# KVSFS
%if %{with kvsfs}
%package kvsfs
Summary:	The NFS-GANESHA's KVSFS FSAL
Group:		System/Filesystems
Requires:	nfs-ganesha = %{version}-%{release}

%description kvsfs
This package contains a FSAL shared object to
be used with NFS-Ganesha to support KVSFS
%endif

# GLUSTER
%if %{with gluster}
%package gluster
Summary:	The NFS-GANESHA's GLUSTER FSAL
Group:		System/Filesystems
Requires:	nfs-ganesha = %{version}-%{release}
BuildRequires:	libgfapi-devel >= 9.0
BuildRequires:	libglusterfs-devel >= 9.0
BuildRequires:	libgfrpc-devel >= 9.0
BuildRequires:	libgfxdr-devel >= 9.0
BuildRequires:	libattr-devel, libacl-devel

%description gluster
This package contains a FSAL shared object to
be used with NFS-Ganesha to support Gluster
%endif

# NTIRPC (if built-in)
%if ! %{with system_ntirpc}
%package -n libntirpc
Summary:	New Transport Independent RPC Library
Group:		System/Filesystems
License:	BSD
Version:	@NTIRPC_VERSION_EMBED@
Url:		https://github.com/nfs-ganesha/ntirpc

# libtirpc has /etc/netconfig, most machines probably have it anyway
# for NFS client
Requires:      libtirpc

%description -n libntirpc
This package contains a new implementation of the original libtirpc,
transport-independent RPC (TI-RPC) library for NFS-Ganesha. It has
the following features not found in libtirpc:
 1. Bi-directional operation
 2. Full-duplex operation on the TCP (vc) transport
 3. Thread-safe operating modes
 3.1 new locking primitives and lock callouts (interface change)
 3.2 stateless send/recv on the TCP transport (interface change)
 4. Flexible server integration support
 5. Event channels (remove static arrays of xprt handles, new EPOLL/KEVENT
    integration)

%package -n libntirpc-devel
Summary:	Development headers for libntirpc
Requires:	libntirpc = @NTIRPC_VERSION_EMBED@
Group:		System/Filesystems
License:	BSD
Version:	@NTIRPC_VERSION_EMBED@
Url:		https://github.com/nfs-ganesha/ntirpc

%description -n libntirpc-devel
Development headers and auxiliary files for developing with %{name}.
%endif

%prep
%setup -q
rm -rf contrib/libzfswrapper
%patch2 -p1

%build
export VERBOSE=1
cd src && %cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo	\
	-DBUILD_CONFIG=rpmbuild				\
	-DDSANITIZE_ADDRESS=OFF				\
	-DUSE_FSAL_NULL=%{use_fsal_null}		\
	-DUSE_FSAL_MEM=%{use_fsal_mem}			\
	-DUSE_FSAL_XFS=%{use_fsal_xfs}			\
	-DUSE_FSAL_LUSTRE=%{use_fsal_lustre}		\
	-DUSE_FSAL_CEPH=%{use_fsal_ceph}		\
	-DUSE_FSAL_RGW=%{use_fsal_rgw}			\
	-DUSE_FSAL_GPFS=%{use_fsal_gpfs}		\
	-DUSE_FSAL_KVSFS=%{use_fsal_kvsfs}		\
	-DUSE_FSAL_GLUSTER=%{use_fsal_gluster}		\
	-DUSE_SYSTEM_NTIRPC=%{use_system_ntirpc}	\
	-DUSE_9P_RDMA=%{use_rdma}			\
	-DUSE_LTTNG=%{use_lttng}			\
	-DUSE_ADMIN_TOOLS=%{use_utils}			\
	-DUSE_GUI_ADMIN_TOOLS=%{use_gui_utils}		\
	-DUSE_RADOS_RECOV=%{use_rados_recov}		\
	-DRADOS_URLS=%{use_rados_urls}			\
	-DUSE_FSAL_VFS=ON				\
	-DUSE_FSAL_PROXY_V4=ON				\
	-DUSE_FSAL_PROXY_V3=OFF				\
	-DUSE_DBUS=ON					\
	-DUSE_9P=%{use_9P}				\
	-DDISTNAME_HAS_GIT_DATA=OFF			\
	-DCMAKE_C_FLAGS="-fmessage-length=0 -grecord-gcc-switches -fstack-protector -O2 -Wall -D_FORTIFY_SOURCE=2 -funwind-tables -fasynchronous-unwind-tables -DNDEBUG -fPIC" \
	-DCMAKE_EXE_LINKER_FLAGS="-Wl,-z,relro"		\
	-DCMAKE_MODULE_LINKER_FLAGS=			\
	-DCMAKE_SHARED_LINKER_FLAGS="-fPIC -Wl,-z,relro"\
	-DUSE_MAN_PAGE=%{use_man_page}			\
%if %{with jemalloc}
	-DALLOCATOR=jemalloc
%endif

make VERBOSE=1 %{?_smp_mflags} || make %{?_smp_mflags} || make

%install
mkdir -p %{buildroot}%{_sysconfdir}/ganesha/
mkdir -p %{buildroot}%{_sysconfdir}/dbus-1/system.d
mkdir -p %{buildroot}%{_fillupdir}
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_libdir}/ganesha
mkdir -p %{buildroot}%{_rundir}/ganesha
mkdir -p %{buildroot}%{_libexecdir}/ganesha
cd src
install -m 644 config_samples/logrotate_ganesha	%{buildroot}%{_sysconfdir}/logrotate.d/ganesha
install -m 644 scripts/ganeshactl/org.ganesha.nfsd.conf	%{buildroot}%{_sysconfdir}/dbus-1/system.d
install -m 755 scripts/nfs-ganesha-config.sh	%{buildroot}%{_libexecdir}/ganesha
%if %{with 9P}
install -m 755 tools/mount.9P	%{buildroot}%{_sbindir}/mount.9P
%endif
install -m 644 config_samples/vfs.conf %{buildroot}%{_sysconfdir}/ganesha
%if %{with rgw}
install -m 644 config_samples/rgw.conf %{buildroot}%{_sysconfdir}/ganesha
%endif

mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_sysconfdir}/systemd/system/nfs-ganesha-lock.service.d
install -m 644 scripts/systemd/nfs-ganesha.service.el7	%{buildroot}%{_unitdir}/nfs-ganesha.service
install -m 644 scripts/systemd/nfs-ganesha-lock.service.el8	%{buildroot}%{_unitdir}/nfs-ganesha-lock.service
install -m 644 scripts/systemd/rpc-statd.conf.el8      %{buildroot}%{_sysconfdir}/systemd/system/nfs-ganesha-lock.service.d/rpc-statd.conf
install -m 644 scripts/systemd/nfs-ganesha-config.service	%{buildroot}%{_unitdir}/nfs-ganesha-config.service
install -m 644 scripts/systemd/sysconfig/nfs-ganesha	%{buildroot}%{_fillupdir}/sysconfig.ganesha
mkdir -p %{buildroot}%{_localstatedir}/log/ganesha

%if %{with lustre}
install -m 644 config_samples/lustre.conf %{buildroot}%{_sysconfdir}/ganesha
%endif

%if %{with xfs}
install -m 644 config_samples/xfs.conf %{buildroot}%{_sysconfdir}/ganesha
%endif

%ifnarch i686 armv7hl ppc64
%if %{with ceph}
install -m 644 config_samples/ceph.conf %{buildroot}%{_sysconfdir}/ganesha
%endif

%if %{with rgw}
install -m 644 config_samples/rgw.conf %{buildroot}%{_sysconfdir}/ganesha
install -m 644 config_samples/rgw_bucket.conf %{buildroot}%{_sysconfdir}/ganesha
%endif
%endif

%if %{with gluster}
install -m 644 config_samples/logrotate_fsal_gluster %{buildroot}%{_sysconfdir}/logrotate.d/ganesha-gfapi
%endif

%if %{with gpfs}
install -m 644 config_samples/gpfs.conf	%{buildroot}%{_sysconfdir}/ganesha
install -m 644 config_samples/gpfs.ganesha.nfsd.conf %{buildroot}%{_sysconfdir}/ganesha
install -m 644 config_samples/gpfs.ganesha.main.conf %{buildroot}%{_sysconfdir}/ganesha
install -m 644 config_samples/gpfs.ganesha.log.conf %{buildroot}%{_sysconfdir}/ganesha
install -m 644 config_samples/gpfs.ganesha.exports.conf	%{buildroot}%{_sysconfdir}/ganesha
%endif

make -C build DESTDIR=%{buildroot} install

rm -f %{buildroot}/%{python3_sitelib}/gpfs*
rm -f %{buildroot}/%{python3_sitelib}/__init__.*

%post
%if ( 0%{?suse_version} )
%service_add_post nfs-ganesha.service nfs-ganesha-lock.service nfs-ganesha-config.service
%else
%if ( 0%{?fedora} || ( 0%{?rhel} && 0%{?rhel} > 6 ) )
semanage fcontext -a -t ganesha_var_log_t %{_localstatedir}/log/ganesha 2>&1 || :
semanage fcontext -a -t ganesha_var_log_t %{_localstatedir}/log/ganesha/ganesha.log 2>&1 || :
%if %{with gluster}
semanage fcontext -a -t ganesha_var_log_t %{_localstatedir}/log/ganesha/ganesha-gfapi.log 2>&1 || :
%endif
restorecon %{_localstatedir}/log/ganesha
%endif
%systemd_post nfs-ganesha.service
%systemd_post nfs-ganesha-lock.service
%systemd_post nfs-ganesha-config.service
%endif
killall -SIGHUP dbus-daemon >/dev/null 2>&1 || :

%pre
%service_add_pre nfs-ganesha-config.service
%service_add_pre nfs-ganesha-lock.service
%service_add_pre nfs-ganesha.service
getent group ganesha > /dev/null || groupadd -r ganesha
getent passwd ganesha > /dev/null || useradd -r -g ganesha -d %{_rundir}/ganesha -s /sbin/nologin -c "NFS-Ganesha Daemon" ganesha
exit 0

%preun
%if ( 0%{?suse_version} )
%service_del_preun nfs-ganesha-config.service
%service_del_preun nfs-ganesha-lock.service
%service_del_preun nfs-ganesha.service
%else
%systemd_preun nfs-ganesha-lock.service
%endif

%postun
%if ( 0%{?suse_version} )
%service_del_postun nfs-ganesha-config.service
%service_del_postun nfs-ganesha-lock.service
%service_del_postun nfs-ganesha.service
%debug_package
%else
%systemd_postun_with_restart nfs-ganesha-lock.service
%{_sysconfdir}/systemd/system/nfs-ganesha-lock.service.d/rpc-statd.conf
%endif

%files
%license src/LICENSE.txt
%{_bindir}/ganesha.nfsd
%{_libdir}/libganesha_nfsd.so*
%config %{_sysconfdir}/dbus-1/system.d/org.ganesha.nfsd.conf
%dir %{_fillupdir}/
%config(noreplace) %{_fillupdir}/sysconfig.ganesha
%dir %attr(755,root,root) %{_sysconfdir}/logrotate.d/
%config(noreplace) %{_sysconfdir}/logrotate.d/ganesha
%dir %{_sysconfdir}/ganesha/
%config(noreplace) %{_sysconfdir}/ganesha/ganesha.conf
# %%dir %%{_defaultdocdir}/ganesha/
# %%{_defaultdocdir}/ganesha/*
%doc src/ChangeLog
%ghost %dir %{_rundir}/ganesha
%dir %{_libexecdir}/ganesha/
%dir %{_libdir}/ganesha
%{_libexecdir}/ganesha/nfs-ganesha-config.sh
%dir %attr(0775,ganesha,ganesha) %{_localstatedir}/log/ganesha

%{_unitdir}/nfs-ganesha.service
%{_unitdir}/nfs-ganesha-lock.service
%{_unitdir}/nfs-ganesha-config.service
%dir %{_sysconfdir}/systemd/system/nfs-ganesha-lock.service.d
%{_sysconfdir}/systemd/system/nfs-ganesha-lock.service.d/rpc-statd.conf

%if %{with man_page}
%{_mandir}/*/ganesha-config.8.gz
%{_mandir}/*/ganesha-core-config.8.gz
%{_mandir}/*/ganesha-export-config.8.gz
%{_mandir}/*/ganesha-cache-config.8.gz
%{_mandir}/*/ganesha-log-config.8.gz
%endif

%if %{with rados_recov}
%files rados-grace
%{_bindir}/ganesha-rados-grace
%{_libdir}/libganesha_rados_recov.so*
%if %{with man_page}
%{_mandir}/*/ganesha-rados-grace.8.gz
%{_mandir}/*/ganesha-rados-cluster-design.8.gz
%endif
%endif

%if %{with rados_urls}
%files rados-urls
%{_libdir}/libganesha_rados_urls.so*
%endif

%if %{with 9P}
%files mount-9P
%{_sbindir}/mount.9P
%if %{with man_page}
%{_mandir}/*/ganesha-9p-config.8.gz
%endif
%endif

%files vfs
%{_libdir}/ganesha/libfsalvfs*
%config(noreplace) %{_sysconfdir}/ganesha/vfs.conf
%if %{with man_page}
%{_mandir}/*/ganesha-vfs-config.8.gz
%endif

%files proxy-v4
%{_libdir}/ganesha/libfsalproxy_v4*
%if %{with man_page}
%{_mandir}/*/ganesha-proxy-v4-config.8.gz
%endif

# Optional packages
%if %{with lustre}
%files lustre
%{_libdir}/ganesha/libfsallustre*
%config(noreplace) %{_sysconfdir}/ganesha/lustre.conf
%if %{with man_page}
%{_mandir}/*/ganesha-lustre-config.8.gz
%endif
%endif

%if %{with nullfs}
%files nullfs
%{_libdir}/ganesha/libfsalnull*
%endif

%if %{with mem}
%files mem
%defattr(-,root,root,-)
%{_libdir}/ganesha/libfsalmem*
%endif

%if %{with gpfs}
%files gpfs
%{_libdir}/ganesha/libfsalgpfs*
%config(noreplace) %{_sysconfdir}/ganesha/gpfs.conf
%config(noreplace) %{_sysconfdir}/ganesha/gpfs.ganesha.nfsd.conf
%config(noreplace) %{_sysconfdir}/ganesha/gpfs.ganesha.main.conf
%config(noreplace) %{_sysconfdir}/ganesha/gpfs.ganesha.log.conf
%config(noreplace) %{_sysconfdir}/ganesha/gpfs.ganesha.exports.conf
%if %{with utils}
/usr/lib/ganesha/gpfs-epoch
%endif
%if %{with man_page}
%{_mandir}/*/ganesha-gpfs-config.8.gz
%endif
%endif

%if %{with xfs}
%files xfs
%{_libdir}/ganesha/libfsalxfs*
%config(noreplace) %{_sysconfdir}/ganesha/xfs.conf
%if %{with man_page}
%{_mandir}/*/ganesha-xfs-config.8.gz
%endif
%endif

%ifnarch i686 armv7hl ppc64
%if %{with ceph}
%files ceph
%{_libdir}/ganesha/libfsalceph*
%config(noreplace) %{_sysconfdir}/ganesha/ceph.conf
%if %{with man_page}
%{_mandir}/*/ganesha-ceph-config.8.gz
%endif
%endif

%if %{with rgw}
%files rgw
%defattr(-,root,root,-)
%{_libdir}/ganesha/libfsalrgw*
%config(noreplace) %{_sysconfdir}/ganesha/rgw.conf
%config(noreplace) %{_sysconfdir}/ganesha/rgw_bucket.conf
%if %{with man_page}
%{_mandir}/*/ganesha-rgw-config.8.gz
%endif
%endif
%endif

%if %{with gluster}
%files gluster
%config(noreplace) %{_sysconfdir}/logrotate.d/ganesha-gfapi
%{_libdir}/ganesha/libfsalgluster*
%if %{with man_page}
%{_mandir}/*/ganesha-gluster-config.8.gz
%endif
%endif

%if ! %{with system_ntirpc}
%files -n libntirpc
%defattr(-,root,root,-)
%{_libdir}/libntirpc.so.@NTIRPC_VERSION_EMBED@
%{_libdir}/libntirpc.so.1.6
%{_libdir}/libntirpc.so
%{!?_licensedir:%global license %%doc}
%license libntirpc/COPYING
%doc libntirpc/NEWS libntirpc/README
%files -n libntirpc-devel
%{_libdir}/pkgconfig/libntirpc.pc
%dir %{_includedir}/ntirpc
%{_includedir}/ntirpc/*
%endif

%if %{with kvsfs}
%files kvsfs
%{_libdir}/ganesha/libfsalkvsfs*
%endif

%if %{with lttng}
%files lttng
%{_libdir}/ganesha/libganesha_trace*
%endif

%if %{with utils}
%files utils
%if ( 0%{?suse_version} )
%dir %{python3_sitelib}/Ganesha
%{python3_sitelib}/Ganesha/*
%{python3_sitelib}/ganeshactl-*-info
%else
%dir %{python_sitelib}/Ganesha
%{python2_sitelib}/Ganesha/*
%{python2_sitelib}/ganeshactl-*-info
%endif
%if %{with gui_utils}
%{_bindir}/ganesha-admin
%{_bindir}/manage_clients
%{_bindir}/manage_exports
%{_bindir}/manage_logger
%{_bindir}/ganeshactl
%if %{with 9P}
%{_bindir}/client_stats_9pOps
%{_bindir}/export_stats_9pOps
%else
%exclude %{_bindir}/client_stats_9pOps
%exclude %{_bindir}/export_stats_9pOps
%endif
%endif
%{_bindir}/fake_recall
%{_bindir}/get_clientids
%{_bindir}/grace_period
%{_bindir}/ganesha_stats
%{_bindir}/sm_notify.ganesha
%{_bindir}/ganesha_mgr
%{_bindir}/ganesha_conf
%{_mandir}/*/ganesha_conf.8.gz
%endif

%changelog
* Fri Dec 31 2021 Kaleb S. KEITHLEY <kkeithle at redhat.com> 4.0-1
- nfs-ganesha 4.0 GA

* Thu Jan 28 2021 Kaleb S. KEITHLEY <kkeithle at redhat.com> 3.5-1
- nfs-ganesha 3.5 GA

* Thu Jun 11 2020 Kaleb S. KEITHLEY <kkeithle at redhat.com> 3.3-1
- nfs-ganesha 3.3 GA

* Fri Nov 15 2019 Kaleb S. KEITHLEY <kkeithle at redhat.com> 3.0-1
- nfs-ganesha 3.0 GA

