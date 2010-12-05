Summary:	DVB mpegtools libdvb - base tools
Name:		libdvb
Version:	0.5.5.1
Release:	%mkrel 9
License:	GPLv2+
Group:		Video
URL:		http://www.metzlerbros.org/dvb/
Source0:	http://www.metzlerbros.org/dvb/%{name}-%{version}.tar.gz
Patch0:		libdvb-0.5.5.1-long.patch
Patch3:		libdvb-0.5.5.1-pkgconfig.patch
Patch4:		libdvb-maindvb.patch
Patch5:		libdvb-0.5.5.1-gcc43.patch
Provides:	dvb-mpegtools
BuildRequires:	gcc-c++
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Manipulation of various MPEG file formats and their DVB variants

%package	devel
Summary:	DVB mpegtools libdvb - developer tools
Group:		Development/Other
Provides:	dvb-mpegtools-devel

%description	devel
manipulation of various MPEG file formats and their DVB variants

%prep

%setup -q
%patch0 -p1
%patch3 -p1 -b .pkgconfig
%patch4
%patch5 -p1

# no `configure` here..

%build
# (anssi) no shared libraries provided; build static libs with -fPIC:
make  PREFIX=%_prefix CFLAGS="%optflags -fPIC" CXX="g++ %{ldflags}" CC="gcc %{ldflags}"
make pkgconfig \
  PREFIX=%_prefix LIBDIR=%_libdir

%install
rm -rf %{buildroot}

# make install DESTDIR=%buildroot
%__mkdir_p %buildroot%_bindir
make install DESTDIR=%buildroot PREFIX=%_prefix LIBDIR=%_libdir
make pkgconfig-install DESTDIR=%buildroot PREFIX=%_prefix LIBDIR=%_libdir

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

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README
%_bindir/*

%files devel
%defattr(-,root,root)
%_libdir/libdvb.a
%_libdir/libdvbci.a
%_libdir/libdvbmpegtools.a
%_libdir/pkgconfig/libdvb*.pc
%_includedir/*
