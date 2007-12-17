%define name libdvb
%define version 0.5.5.1
%define release %mkrel 4

Summary: DVB mpegtools libdvb - base tools
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://www.metzlerbros.org/dvb/%{name}-%{version}.tar.gz
Patch: libdvb-0.5.5.1-long.patch
Patch3: libdvb-0.5.5.1-pkgconfig.patch
Patch4: libdvb-maindvb.patch
License: GPL
Group: Video
URL: http://www.metzlerbros.org/dvb/
Provides: dvb-mpegtools
BuildRequires: gcc-c++

%description
Manipulation of various MPEG file formats and their DVB variants

%package devel
Summary: DVB mpegtools libdvb - developer tools
Group: Development/Other
Provides: dvb-mpegtools-devel

%description devel
manipulation of various MPEG file formats and their DVB variants

%prep
%setup -q
%patch -p1
%patch3 -p1 -b .pkgconfig
%patch4
# no `configure` here..

%build
# -I../../include is wrong... point to the headers of the current kernel
# (anssi) no shared libraries provided; build static libs with -fPIC:
make "INCS=-I/lib/modules/`uname -r`/build/include -I../include" \
 "INCLUDES=-I/lib/modules/`uname -r`/build/include -I../include" \
  PREFIX=%_prefix CFLAGS="%optflags -fPIC"
make pkgconfig \
  PREFIX=%_prefix LIBDIR=%_libdir

%install
rm -rf $RPM_BUILD_ROOT
# make install DESTDIR=%buildroot
%__mkdir_p %buildroot%_bindir
make install DESTDIR=%buildroot PREFIX=%_prefix LIBDIR=%_libdir
make pkgconfig-install DESTDIR=%buildroot PREFIX=%_prefix LIBDIR=%_libdir
(cd sample_progs && make install DESTDIR=%buildroot PREFIX=%_prefix LIBDIR=%_libdir)

# prefix binaries with dvb_
for i in %buildroot%_bindir/* ; do 
  dir=`dirname $i` ; file=`basename $i` 
  case "$file" in
  dvb*) ;; 
  *)  mv $dir/$file $dir/dvb_$file ;;
  esac
done
# but keep aliases for ts* and pes*
for i in %buildroot%_bindir/dvb_ts* %buildroot%_bindir/dvb_pes* ; do
  dir=`dirname $i` ; file=`basename $i` 
  (cd $dir && ln -s $file `echo $file | sed -e 's/^dvb_//'`)
done

#gw lib64
#%if %_lib == lib64
#mv %buildroot%_prefix/lib %buildroot%_libdir
#%endif


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README
%_bindir/*

%files devel
%defattr(-,root,root)
%_libdir/*
%_includedir/*


