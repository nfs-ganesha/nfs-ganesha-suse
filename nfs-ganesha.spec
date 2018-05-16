
%global _hardened_build 1

%if 0%{?fedora} >= 15 || 0%{?rhel} >= 7
%global with_nfsidmap 1
%else
%global with_nfsidmap 0
%endif

%if ( 0%{?fedora} >= 18 || 0%{?rhel} >= 7 )
%global with_systemd 1
%else
%global with_systemd 0
%endif

%if ( 0%{?suse_version} )
BuildRequires: distribution-release
%if ( ! 0%{?is_opensuse} )
BuildRequires: sles-release >= 12
Requires: sles-release >= 12
%else
BuildRequires: openSUSE-release
Requires: openSUSE-release
%endif

%global with_systemd 1
%global with_nfsidmap 1
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

%bcond_without xfs
%global use_fsal_xfs %{on_off_switch xfs}

%bcond_with ceph
%global use_fsal_ceph %{on_off_switch ceph}

%bcond_with rgw
%global use_fsal_rgw %{on_off_switch rgw}

%bcond_without gluster
%global use_fsal_gluster %{on_off_switch gluster}

%bcond_with panfs
%global use_fsal_panfs %{on_off_switch panfs}

%bcond_with rdma
%global use_rdma %{on_off_switch rdma}

%bcond_with jemalloc

%bcond_with lttng
%global use_lttng %{on_off_switch lttng}

%bcond_without utils
%global use_utils %{on_off_switch utils}

%bcond_with gui_utils
%global use_gui_utils %{on_off_switch gui_utils}

%bcond_without system_ntirpc
%global use_system_ntirpc %{on_off_switch system_ntirpc}

%bcond_without man_page
%global use_man_page %{on_off_switch man_page}

%bcond_with rados_recov
%global use_rados_recov %{on_off_switch rados_recov}
 
%bcond_with rados_urls
%global use_rados_urls %{on_off_switch rados_urls}

%if ( 0%{?rhel} && 0%{?rhel} < 7 )
%global _rundir %{_localstatedir}/run
%endif

%global dev_version %{lua: s = string.gsub('@GANESHA_EXTRA_VERSION@', '^%-', ''); s2 = string.gsub(s, '%-', '.'); print(s2) }
# %%global	dev final
# %%global	dash_dev_version 2.5-final

Name:		nfs-ganesha
Version:	2.6.2
Release:	1%{?dev:%{dev}}%{?dist}
Summary:	NFS-Ganesha is a NFS Server running in user space
Group:		Applications/System
License:	LGPL-3.0+
Url:		https://github.com/nfs-ganesha/nfs-ganesha/wiki

Source0:	https://github.com/%{name}/%{name}/archive/V%{version}/%{name}-%{version}.tar.gz

BuildRequires:	cmake
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	pkgconfig
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
%if %{with system_ntirpc}
BuildRequires:	libntirpc-devel >= 1.6.2
%endif
%if ( 0%{?fedora} )
# this should effectively be a no-op, as all Fedora installs should have it
# with selinux.
Requires:	policycoreutils-python
%endif
Requires:	nfs-utils
%if ( 0%{?fedora} ) || ( 0%{?rhel} && 0%{?rhel} >= 6 ) || ( 0%{?suse_version} )
Requires:	rpcbind
%else
Requires:	portmap
%endif
%if %{with_nfsidmap}
%if ( 0%{?suse_version} )
BuildRequires:	nfsidmap-devel
%else
BuildRequires:	libnfsidmap-devel
%endif
%else
BuildRequires:	nfs-utils-lib-devel
%endif
%if %{with rdma}
BuildRequires:	libmooshika-devel >= 0.6-0
%endif
%if %{with jemalloc}
BuildRequires:	jemalloc-devel
%endif
%if %{with_systemd}
BuildRequires: systemd
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
%else
BuildRequires:	initscripts
%endif
%if %{with man_page}
BuildRequires: python-Sphinx
%endif
Requires(post): psmisc
%if ( 0%{?suse_version} )
Requires(pre): shadow
%else
Requires(pre): shadow-utils
%endif

# Use CMake variables

%description
nfs-ganesha : NFS-GANESHA is a NFS Server running in user space.
It comes with various back-end modules (called FSALs) provided as
shared objects to support different file systems and name-spaces.

%package mount-9P
Summary: A 9p mount helper
Group: Applications/System

%description mount-9P
This package contains the mount.9P script that clients can use
to simplify mounting to NFS-GANESHA. This is a 9p mount helper.

%package vfs
Summary: The NFS-GANESHA's VFS FSAL
Group: Applications/System
BuildRequires: libattr-devel
Requires: nfs-ganesha = %{version}-%{release}

%description vfs
This package contains a FSAL shared object to
be used with NFS-Ganesha to support VFS based filesystems

%package proxy
Summary: The NFS-GANESHA's PROXY FSAL
Group: Applications/System
BuildRequires: libattr-devel
Requires: nfs-ganesha = %{version}-%{release}

%description proxy
This package contains a FSAL shared object to
be used with NFS-Ganesha to support PROXY based filesystems

%if %{with utils}
%package utils
Summary: The NFS-GANESHA's util scripts
Group: Applications/System
%if ( 0%{?suse_version} )
Requires:	dbus-1-python, python-gobject2 python-pyparsing
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
%if ( 0%{?suse_version} )
BuildRequires:	python-devel
Requires: nfs-ganesha = %{version}-%{release}, python
%else
BuildRequires:	python2-devel
Requires: nfs-ganesha = %{version}-%{release}, python2
%endif

%description utils
This package contains utility scripts for managing the NFS-GANESHA server
%endif

%if %{with lttng}
%package lttng
Summary: The NFS-GANESHA's library for use with LTTng
Group: Applications/System
BuildRequires: lttng-ust-devel >= 2.3
Requires: nfs-ganesha = %{version}-%{release}, lttng-tools >= 2.3, lttng-ust >= 2.3

%description lttng
This package contains the libganesha_trace.so library. When preloaded
to the ganesha.nfsd server, it makes it possible to trace using LTTng.
%endif

%if %{with rados_recov}
%package rados
Summary: The NFS-GANESHA's library for recovery backend
Group: Applications/System
BuildRequires: librados-devel >= 0.61
Requires: nfs-ganesha = %{version}-%{release}

%description rados
This package contains the librados.so library. Ganesha uses it to
store client tracking data in ceph cluster.
%endif

# Option packages start here. use "rpmbuild --with gpfs" (or equivalent)
# for activating this part of the spec file

# NULL
%if %{with nullfs}
%package nullfs
Summary: The NFS-GANESHA's NULLFS Stackable FSAL
Group: Applications/System
Requires: nfs-ganesha = %{version}-%{release}

%description nullfs
This package contains a Stackable FSAL shared object to
be used with NFS-Ganesha. This is mostly a template for future (more sophisticated) stackable FSALs
%endif

# MEM
%if %{with mem}
%package mem
Summary: The NFS-GANESHA's Memory backed testing FSAL
Group: Applications/System
Requires: nfs-ganesha = %{version}-%{release}

%description mem
This package contains a FSAL shared object to be used with NFS-Ganesha. This
is used for speed and latency testing.
%endif

# GPFS
%if %{with gpfs}
%package gpfs
Summary: The NFS-GANESHA's GPFS FSAL
Group: Applications/System
Requires: nfs-ganesha = %{version}-%{release}

%description gpfs
This package contains a FSAL shared object to
be used with NFS-Ganesha to support GPFS backend
%endif

# CEPH
%ifnarch i686 armv7hl ppc64
%if %{with ceph}
%package ceph
Summary: The NFS-GANESHA's CephFS FSAL
Group: Applications/System
Requires:	nfs-ganesha = %{version}-%{release}
BuildRequires:	libcephfs1-devel >= 10.2.7

%description ceph
This package contains a FSAL shared object to
be used with NFS-Ganesha to support CephFS
%endif

# RGW
%if %{with rgw}
%package rgw
Summary: The NFS-GANESHA's Ceph RGW FSAL
Group: Applications/System
Requires:	nfs-ganesha = %{version}-%{release}
BuildRequires:	librgw2-devel >= 10.2.7

%description rgw
This package contains a FSAL shared object to
be used with NFS-Ganesha to support Ceph RGW
%endif
%endif

# XFS
%if %{with xfs}
%package xfs
Summary: The NFS-GANESHA's XFS FSAL
Group: Applications/System
Requires:	nfs-ganesha = %{version}-%{release}
BuildRequires:	libattr-devel xfsprogs-devel

%description xfs
This package contains a shared object to be used with FSAL_VFS
to support XFS correctly
%endif

# PANFS
%if %{with panfs}
%package panfs
Summary: The NFS-GANESHA's PANFS FSAL
Group: Applications/System
Requires:	nfs-ganesha = %{version}-%{release}

%description panfs
This package contains a FSAL shared object to
be used with NFS-Ganesha to support PANFS
%endif

# GLUSTER
%if %{with gluster}
%package gluster
Summary: The NFS-GANESHA's GLUSTER FSAL
Group: Applications/System
Requires:	nfs-ganesha = %{version}-%{release}
BuildRequires:	glusterfs-devel >= 3.12.3
BuildRequires:	libattr-devel, libacl-devel

%description gluster
This package contains a FSAL shared object to
be used with NFS-Ganesha to support Gluster
%endif

# NTIRPC (if built-in)
%if ! %{with system_ntirpc}
%package -n libntirpc
Summary:       New Transport Independent RPC Library
Group:         System Environment/Libraries
License:       BSD
Version:       @NTIRPC_VERSION_EMBED@
Url:           https://github.com/nfs-ganesha/ntirpc

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
Summary:       Development headers for libntirpc
Requires:      libntirpc = @NTIRPC_VERSION_EMBED@
Group:         System Environment/Libraries
License:       BSD
Version:       @NTIRPC_VERSION_EMBED@
Url:           https://github.com/nfs-ganesha/ntirpc

%description -n libntirpc-devel
Development headers and auxiliary files for developing with %{name}.
%endif

%prep
%setup -q -n %{name}-%{version}
rm -rf contrib/libzfswrapper

%build
cd src && %cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo	\
	-DBUILD_CONFIG=rpmbuild				\
	-DDSANITIZE_ADDRESS=OFF				\
	-DUSE_FSAL_NULL=%{use_fsal_null}		\
	-DUSE_FSAL_MEM=%{use_fsal_mem}			\
	-DUSE_FSAL_XFS=%{use_fsal_xfs}			\
	-DUSE_FSAL_CEPH=%{use_fsal_ceph}		\
	-DUSE_FSAL_RGW=%{use_fsal_rgw}			\
	-DUSE_FSAL_GPFS=%{use_fsal_gpfs}		\
	-DUSE_FSAL_PANFS=%{use_fsal_panfs}		\
	-DUSE_FSAL_GLUSTER=%{use_fsal_gluster}		\
	-DUSE_SYSTEM_NTIRPC=%{use_system_ntirpc}	\
	-DUSE_9P_RDMA=%{use_rdma}			\
	-DUSE_LTTNG=%{use_lttng}			\
	-DUSE_ADMIN_TOOLS=%{use_utils}			\
	-DUSE_GUI_ADMIN_TOOLS=%{use_gui_utils}		\
	-DUSE_RADOS_RECOV=%{use_rados_recov}		\
	-DRADOS_URLS=%{use_rados_urls}			\
	-DUSE_FSAL_VFS=ON				\
	-DUSE_FSAL_PROXY=ON				\
	-DUSE_DBUS=ON					\
	-DUSE_9P=ON					\
	-DDISTNAME_HAS_GIT_DATA=OFF			\
	-DCMAKE_C_FLAGS="-fmessage-length=0 -grecord-gcc-switches -fstack-protector -O2 -Wall -D_FORTIFY_SOURCE=2 -funwind-tables -fasynchronous-unwind-tables -DNDEBUG -fPIC" \
	-DCMAKE_EXE_LINKER_FLAGS="-Wl,-z,relro"		\
	-DCMAKE_MODULE_LINKER_FLAGS=			\
	-DCMAKE_SHARED_LINKER_FLAGS="-fPIC -Wl,-z,relro"\
	-DUSE_MAN_PAGE=%{use_man_page}			\
%if %{with jemalloc}
	-DALLOCATOR=jemalloc
%endif

make %{?_smp_mflags} || make %{?_smp_mflags} || make

%install
mkdir -p %{buildroot}%{_sysconfdir}/ganesha/
mkdir -p %{buildroot}%{_sysconfdir}/dbus-1/system.d
mkdir -p %{buildroot}%{_localstatedir}/adm/fillup-templates
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
install -m 755 tools/mount.9P	%{buildroot}%{_sbindir}/mount.9P
install -m 644 config_samples/vfs.conf %{buildroot}%{_sysconfdir}/ganesha
%if %{with rgw}
install -m 644 config_samples/rgw.conf %{buildroot}%{_sysconfdir}/ganesha
%endif

%if %{with_systemd}
mkdir -p %{buildroot}%{_unitdir}
install -m 644 scripts/systemd/nfs-ganesha.service.el7	%{buildroot}%{_unitdir}/nfs-ganesha.service
install -m 644 scripts/systemd/nfs-ganesha-lock.service.el7	%{buildroot}%{_unitdir}/nfs-ganesha-lock.service
install -m 644 scripts/systemd/nfs-ganesha-config.service	%{buildroot}%{_unitdir}/nfs-ganesha-config.service
install -m 644 scripts/systemd/sysconfig/nfs-ganesha	%{buildroot}%{_localstatedir}/adm/fillup-templates/ganesha
%if 0%{?_tmpfilesdir:1}
mkdir -p %{buildroot}%{_tmpfilesdir}
install -m 644 scripts/systemd/tmpfiles.d/ganesha.conf	%{buildroot}%{_tmpfilesdir}
%endif
mkdir -p %{buildroot}%{_localstatedir}/log/ganesha
%else
mkdir -p %{buildroot}%{_sysconfdir}/init.d
install -m 755 scripts/init.d/nfs-ganesha.el6		%{buildroot}%{_sysconfdir}/init.d/nfs-ganesha
install -m 644 scripts/init.d/sysconfig/ganesha		%{buildroot}%{_sysconfdir}/sysconfig/ganesha
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
install -m 755 scripts/gpfs-epoch %{buildroot}%{_libexecdir}/ganesha
install -m 644 config_samples/gpfs.conf	%{buildroot}%{_sysconfdir}/ganesha
install -m 644 config_samples/gpfs.ganesha.nfsd.conf %{buildroot}%{_sysconfdir}/ganesha
install -m 644 config_samples/gpfs.ganesha.main.conf %{buildroot}%{_sysconfdir}/ganesha
install -m 644 config_samples/gpfs.ganesha.log.conf %{buildroot}%{_sysconfdir}/ganesha
install -m 644 config_samples/gpfs.ganesha.exports.conf	%{buildroot}%{_sysconfdir}/ganesha
%if ! %{with_systemd}
mkdir -p %{buildroot}%{_sysconfdir}/init.d
install -m 755 scripts/init.d/nfs-ganesha.gpfs		%{buildroot}%{_sysconfdir}/init.d/nfs-ganesha-gpfs
%endif
%endif

make -C build DESTDIR=%{buildroot} install

find "%{buildroot}%{python_sitelib}/" -name '*.pyc' \
-exec %__rm {} \;
%__python -c 'import compileall;
compileall.compile_dir("%{buildroot}%{python_sitelib}/",
ddir="%{python_sitelib}/",
force=1)'

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
%if %{with_systemd}
%systemd_post nfs-ganesha.service
%systemd_post nfs-ganesha-lock.service
%systemd_post nfs-ganesha-config.service
%endif
%endif
killall -SIGHUP dbus-daemon >/dev/null 2>&1 || :

%pre
getent group ganesha > /dev/null || groupadd -r ganesha
getent passwd ganesha > /dev/null || useradd -r -g ganesha -d %{_rundir}/ganesha -s /sbin/nologin -c "NFS-Ganesha Daemon" ganesha
exit 0

%preun
%if ( 0%{?suse_version} )
%service_del_preun nfs-ganesha-lock.service
%else
%if %{with_systemd}
%systemd_preun nfs-ganesha-lock.service
%endif
%endif

%postun
%if ( 0%{?suse_version} )
%service_del_postun nfs-ganesha-lock.service
%debug_package
%else
%if %{with_systemd}
%systemd_postun_with_restart nfs-ganesha-lock.service
%endif
%endif

%files
%license src/LICENSE.txt
%{_bindir}/ganesha.nfsd
%config %{_sysconfdir}/dbus-1/system.d/org.ganesha.nfsd.conf
%config(noreplace) %{_localstatedir}/adm/fillup-templates/ganesha
%config(noreplace) %{_sysconfdir}/logrotate.d/ganesha
%dir %{_sysconfdir}/ganesha/
%config(noreplace) %{_sysconfdir}/ganesha/ganesha.conf
%dir %{_defaultdocdir}/ganesha/
%{_defaultdocdir}/ganesha/*
%doc src/ChangeLog
%dir %{_rundir}/ganesha
%dir %{_libexecdir}/ganesha/
%dir %{_libdir}/ganesha
%{_libexecdir}/ganesha/nfs-ganesha-config.sh
%dir %attr(0775,ganesha,ganesha) %{_localstatedir}/log/ganesha

%if %{with_systemd}
%{_unitdir}/nfs-ganesha.service
%{_unitdir}/nfs-ganesha-lock.service
%{_unitdir}/nfs-ganesha-config.service
%if 0%{?_tmpfilesdir:1}
%{_tmpfilesdir}/ganesha.conf
%endif
%else
%{_sysconfdir}/init.d/nfs-ganesha
%endif

%if %{with man_page}
%{_mandir}/*/ganesha-config.8.gz
%{_mandir}/*/ganesha-core-config.8.gz
%{_mandir}/*/ganesha-export-config.8.gz
%{_mandir}/*/ganesha-cache-config.8.gz
%{_mandir}/*/ganesha-log-config.8.gz
%endif


%files mount-9P
%{_sbindir}/mount.9P
%if %{with man_page}
%{_mandir}/*/ganesha-9p-config.8.gz
%endif

%files vfs
%{_libdir}/ganesha/libfsalvfs*
%config(noreplace) %{_sysconfdir}/ganesha/vfs.conf
%if %{with man_page}
%{_mandir}/*/ganesha-vfs-config.8.gz
%endif

%files proxy
%{_libdir}/ganesha/libfsalproxy*
%if %{with man_page}
%{_mandir}/*/ganesha-proxy-config.8.gz
%endif

# Optional packages
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
%{_libexecdir}/ganesha/gpfs-epoch
%if ! %{with_systemd}
%{_sysconfdir}/init.d/nfs-ganesha-gpfs
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

%if %{with panfs}
%files panfs
%{_libdir}/ganesha/libfsalpanfs*
%endif

%if %{with lttng}
%files lttng
%{_libdir}/ganesha/libganesha_trace*
%endif

%if %{with utils}
%files utils
%if ( 0%{?suse_version} )
%dir %{python_sitelib}/Ganesha
%{python_sitelib}/Ganesha/*
%{python_sitelib}/ganeshactl-*-info
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
%{_bindir}/client_stats_9pOps
%{_bindir}/export_stats_9pOps
%endif
%{_bindir}/fake_recall
%{_bindir}/get_clientids
%{_bindir}/grace_period
%{_bindir}/purge_gids
%{_bindir}/ganesha_stats
%{_bindir}/sm_notify.ganesha
%{_bindir}/ganesha_mgr
%{_bindir}/ganesha_conf
%{_mandir}/*/ganesha_conf.8.gz
%endif

%changelog
* Mon May 14 2018 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.6.2-1
- nfs-ganesha 2.6.2 GA

* Wed Mar 21 2018 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.6.1-1
- nfs-ganesha 2.6.1 GA

* Thu Feb 22 2018 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.6.0-1
- nfs-ganesha 2.6.0 GA

* Mon Dec 4 2017 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.5.4-1
- nfs-ganesha 2.5.4 GA

* Tue Oct 10 2017 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.5.3-1
- nfs-ganesha 2.5.3 GA

* Mon Aug 28 2017 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.5.2-1
- nfs-ganesha 2.5.2 GA

* Mon Jul 24 2017 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.5.1-1
- nfs-ganesha 2.5.1 GA

* Thu Jul 20 2017 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.5.0-2
- nfs-ganesha 2.5.0 w/ libntirpc-1.5.3

* Mon Jun 12 2017 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.5.0-1
- nfs-ganesha 2.5.0 GA

* Tue May 16 2017 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.4.5-3
- rebuild with libntirpc-1.4.4

* Wed Apr 19 2017 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.4.5-2
- nfs-ganesha 2.4.5 GA, w/ RGW again (cephfs-10.2.7)

* Wed Apr 5 2017 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.4.5-1
- nfs-ganesha 2.4.5 GA

* Tue Mar 21 2017 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.4.4-1
- nfs-ganesha 2.4.4 GA

* Thu Feb 9 2017 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.4.3-2
- nfs-ganesha 2.4.3 GA, reenable FSAL_CEPH and FSAL_RGW

* Tue Feb 7 2017 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.4.3-1
- nfs-ganesha 2.4.3 GA

* Mon Jan 23 2017 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.4.2-1
- nfs-ganesha 2.4.2 GA

* Wed Jan 18 2017 Kaleb S. KEITHLEY <kkeithle at redhat.com>
- python2 (vs. python3) cleanup

* Fri Dec 23 2016 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.4.1-2
- nfs-ganesha 2.4.1 w/ FSAL_RGW

* Mon Oct 31 2016 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.4.1-1
- nfs-ganesha 2.4.1 GA

* Fri Oct 28 2016 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.4.0-2
- rebuild with libntirpc-1.4.3

* Thu Sep 22 2016 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.4.0-1
- nfs-ganesha 2.4.0 GA

* Wed Sep 21 2016 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.4.0-0.22rc6
- 2.4-rc6

* Fri Sep 16 2016 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.4.0-0.21rc5
- 2.4-rc5

* Sun Sep 11 2016 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.4.0-0.20rc4
- 2.4-rc4

* Wed Sep 7 2016 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.4.0-0.19rc3
- 2.4-rc3

* Tue Sep 6 2016 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.4.0-0.18rc2
- 2.4-rc2

* Mon Aug 29 2016 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.4.0-0.17rc1
- 2.4-rc1

* Tue Aug 16 2016 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.4.0-0.16dev29
- 2.4-dev-29, jemalloc off by default (conflicts with glusterfs-api)

* Mon Aug 15 2016 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.4.0-0.15dev29
- 2.4-dev-29

* Mon Aug 1 2016 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.4.0-0.14dev27
- 2.4-dev-27

* Mon Jul 25 2016 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.4.0-0.13dev26
- 2.4-dev-26

* Wed Jul 20 2016 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.4.0-0.12dev25
- 2.4-dev-25 (revised 32-bit)

* Tue Jul 19 2016 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.4.0-0.11dev25
- 2.4-dev-25

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.0-0.10dev23
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Tue Jul 5 2016 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.4.0-0.9dev23
- 2.4-dev-23

* Fri Jun 24 2016 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.4.0-0.8dev21
- 2.4-dev-21 w/ FSAL_RGW

* Mon Jun 20 2016 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.4.0-0.7dev21
- 2.4-dev-21

* Mon May 30 2016 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.4.0-0.6dev19
- 2.4-dev-19

* Tue May 10 2016 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.4.0-0.5dev17
- 2.4-dev-17

* Fri Apr 8 2016 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.4.0-0.4dev14
- 2.4-dev-14

* Thu Mar 31 2016 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.4.0-0.3dev12
- 2.4-dev-12

* Mon Feb 29 2016 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.4.0-0.2dev10
- 2.4-dev-10

* Fri Feb 5 2016 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.4.0-0.1dev7
- 2.4-dev-7

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 17 2015 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.3.0-2
- Requires: rpcbind or portmap

* Wed Oct 28 2015 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.3.0-1
- 2.3.0 GA

* Tue Oct 27 2015 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.3.0-0.15rc8
- 2.3.0 RC8, rebuild with libntirpc-1.3.1, again

* Mon Oct 26 2015 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.3.0-0.14rc8
- 2.3.0 RC8, rebuild with libntirpc-1.3.1

* Sun Oct 25 2015 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.3.0-0.13rc8
- 2.3.0 RC8

* Thu Oct 22 2015 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.3.0-0.12rc7
- 2.3.0 RC7 (N.B. 2.3.0-0.11rc6 was really rc7)

* Mon Oct 19 2015 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.3.0-0.11rc7
- 2.3.0 RC7

* Mon Oct 12 2015 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.3.0-0.10rc6
- 2.3.0 RC6

* Thu Oct 8 2015 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.3.0-0.9rc5
- 2.3.0 RC5 w/ CMakeLists.txt.patch and config-h.in.cmake.patch

* Wed Oct 7 2015 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.3.0-0.8rc5
- 2.3.0 RC5 mount-9p w/o Requires: nfs-ganesha

* Tue Oct 6 2015 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.3.0-0.7rc5
- 2.3.0 RC5 revised scripts/ganeshactl/CMakeLists.txt.patch

* Mon Oct 5 2015 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.3.0-0.6rc5
- 2.3.0 RC5

* Mon Sep 28 2015 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.3.0-0.5rc4
- 2.3.0 RC4

* Fri Sep 18 2015 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.3.0-0.4rc3
- 2.3.0 RC3

* Fri Sep 11 2015 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.3.0-0.3rc2
- 2.3.0 RC2

* Fri Sep 11 2015 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.3.0-0.2rc1
- 2.3.0 RC1, revised .../SAL/nfs4_state_id.c.patch

* Wed Sep 9 2015 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.3.0-0.1rc1
- 2.3.0 RC1

* Sat Aug 29 2015 Niels de Vos <ndevos@redhat.com> 2.2.0-6
- Rebuilt for jemalloc SONAME bump

* Fri Jul 17 2015 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.2.0-5
- BuildRequires: libntirprc on base

* Fri Jul 17 2015 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.2.0-4
- link with unbundled, shared libntirpc

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed May 27 2015 Niels de Vos <ndevos@redhat.com>
- improve readability and allow "rpmbuild --with .." options again

* Fri May 15 2015 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.2.0-2
- %%license, build with glusterfs-3.7.0 GA

* Tue Apr 21 2015 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.2.0-1
- 2.2.0 GA

* Mon Apr 20 2015 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.2.0-0.13rc-final
- 2.2.0-0.13rc-final

* Mon Apr 13 2015 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.2.0-0.12rc8
- 2.2.0-0.12rc8

* Mon Apr 6 2015 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.2.0-0.11rc7
- 2.2.0-0.11rc7

* Thu Apr 2 2015 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.2.0-0.10rc6
- 2.2.0-0.10rc6, with unbundled libntirpc

* Mon Mar 30 2015 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.2.0-0.9rc6
- 2.2.0-0.9rc6

* Sun Mar 22 2015 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.2.0-0.8rc5
- 2.2.0-0.8rc5

* Tue Mar 17 2015 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.2.0-0.7rc4
- ntirpc-1.2.1.tar.gz

* Tue Mar 17 2015 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.2.0-0.6rc4
- updated ntirpc-1.2.0.tar.gz

* Sun Mar 15 2015 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.2.0-0.5rc4
- 2.2.0-0.5rc4

* Mon Feb 23 2015 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.2.0-0.4rc3
- 2.2.0-0.4rc3

* Mon Feb 16 2015 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.2.0-0.3rc2
- subpackage Requires: nfs-ganesha = %%{version}-%%{release}

* Mon Feb 16 2015 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.2.0-0.2rc2
- 2.2.0-0.2rc2

* Fri Feb 13 2015 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.2.0-0.1rc1
- 2.2.0-0.1rc1
- nfs-ganesha.spec based on upstream

* Thu Feb 12 2015 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.1.0-14
- Fedora 23/rawhide build fixes
- Ceph restored in EPEL

* Mon Jan 19 2015 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.1.0-13
- Ceph retired from EPEL 7

* Thu Nov 6 2014 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.1.0-12
- rebuild after libnfsidmap symbol version revert

* Wed Oct 29 2014 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.1.0-11
- PyQt -> PyQt4 typo

* Mon Oct 27 2014 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.1.0-10
- use upstream init.d script

* Thu Oct 2 2014 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.1.0-9
- restore exclusion of gluster gfapi on rhel

* Thu Oct 2 2014 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.1.0-8
- install /etc/dbus-1/system.d/org.ganesha.nfsd.conf
- build and install admin tools

* Mon Sep 29 2014 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.1.0-7
- install /etc/sysconfig/nfs-ganesha file

* Fri Aug 29 2014 Kaleb S. KEITHLEY <kkeithle at redhat.com>
- Ceph FSAL typo, #1135437

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jul 24 2014 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.1.0-5
- use upstream nfs-ganesha.service

* Fri Jul 11 2014 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.1.0-4
- keep fsal .so files, implementation now uses them

* Tue Jul 1 2014 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.1.0-3
- static libuid2grp

* Tue Jul 1 2014 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.1.0-2
- add libuid2grp.so

* Mon Jun 30 2014 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.1.0-1
- nfs-ganesha-2.1.0 GA

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Jun 2 2014 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.0.0-9
- Ceph FSAL enabled with ceph-0.80

* Wed May 21 2014 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.0.0-8
- getdents()->getdents64(), struct dirent -> struct dirent64

* Sat May 10 2014 Kaleb S. KEITHLEY <kkeithle at redhat.com>
- and exclude libfsalceph

* Sat May 10 2014 Kaleb S. KEITHLEY <kkeithle at redhat.com>
- exclude libfsalgluster correctly

* Fri May 9 2014 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.0.0-7
- Ceph FSAL, in a subpackage, (but requires ceph >= 0.78)

* Mon Mar 31 2014 Kaleb S. KEITHLEY <kkeithle at redhat.com>
- GlusterFS FSAL in a subpackage
- EPEL7 has jemalloc as of 2014-02-25

* Tue Jan 21 2014 Kaleb S. KEITHLEY <kkeithle at redhat.com>
- sussed out github archive so as to allow correct Source0

* Fri Jan 17 2014 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.0.0-6
- EPEL7 and xfsprogs

* Fri Jan 17 2014 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.0.0-5
- EPEL7

* Mon Jan 6 2014 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.0.0-4
- with glusterfs-api(-devel) >= 3.4.2

* Sat Jan 4 2014 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.0.0-3
- with glusterfs-api

* Thu Jan 2 2014 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.0.0-2
- Build on RHEL6. Add sample init.d script

* Wed Dec 11 2013 Jim Lieb <lieb@sea-troll.net> - 2.0.0-1
- Update to V2.0.0 release

* Mon Nov 25 2013 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.0.0-0.2.rcfinal
- update to RC-final

* Fri Nov 22 2013 Kaleb S. KEITHLEY <kkeithle at redhat.com> 2.0.0-0.1.rc5
- Initial commit
