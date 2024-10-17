%define major 6
%define libname %mklibname ffi %{major}
%define devname %mklibname -d ffi
%define staticname %mklibname -d -s ffi

# (tpg) optimize it a bit
%global optflags %optflags -O3

Summary:	A portable foreign function interface library
Name:		libffi6
Version:	3.2.1
Release:	13
Group:		System/Libraries
License:	BSD
Url:		https://sourceware.org/libffi
Source0:	ftp://sourceware.org/pub/%{name}/libffi-%{version}.tar.gz
Patch0:		ffi-3.2.1-sysv.S.patch
Patch1:		libffi-3.2.1-o-tmpfile-eacces.patch
Patch2:		libffi-3.1-fix-include-path.patch
Patch3:		libffi-aarch64-rhbz1174037.patch
Patch4:		libffi-3.1-aarch64-fix-exec-stack.patch
Patch5:		libffi-3.1-riscv.patch
Patch6:		libffi-arm-asmsyntax.patch
BuildRequires:	autoconf

%description
Compilers for high level languages generate code that follow certain
conventions. These conventions are necessary, in part, for separate
compilation to work. One such convention is the "calling convention".
The calling convention is a set of assumptions made by the compiler
about where function arguments will be found on entry to a function. A
calling convention also specifies where the return value for a function
is found.

Some programs may not know at the time of compilation what arguments
are to be passed to a function.  For instance, an interpreter may be
told at run-time about the number and types of arguments used to call a
given function. `Libffi' can be used in such programs to provide a
bridge from the interpreter program to compiled code.

The `libffi' library provides a portable, high level programming
interface to various calling conventions. This allows a programmer to
call any function specified by a call interface description at run time.

FFI stands for Foreign Function Interface. A foreign function
interface is the popular name for the interface that allows code
written in one language to call code written in another language. The
`libffi' library really only provides the lowest, machine dependent
layer of a fully featured foreign function interface. A layer must
exist above `libffi' that handles type conversions for values passed
between the two languages.

%if "%{_lib}" != "lib"
%package -n	%{libname}
Summary:	A portable foreign function interface library
Group:		System/Libraries

%description -n	%{libname}
Compilers for high level languages generate code that follow certain
conventions. These conventions are necessary, in part, for separate
compilation to work. One such convention is the "calling convention".
The calling convention is a set of assumptions made by the compiler
about where function arguments will be found on entry to a function. A
calling convention also specifies where the return value for a function
is found.

Some programs may not know at the time of compilation what arguments
are to be passed to a function.  For instance, an interpreter may be
told at run-time about the number and types of arguments used to call a
given function. `Libffi' can be used in such programs to provide a
bridge from the interpreter program to compiled code.

The `libffi' library provides a portable, high level programming
interface to various calling conventions. This allows a programmer to
call any function specified by a call interface description at run time.

FFI stands for Foreign Function Interface. A foreign function
interface is the popular name for the interface that allows code
written in one language to call code written in another language. The
`libffi' library really only provides the lowest, machine dependent
layer of a fully featured foreign function interface. A layer must
exist above `libffi' that handles type conversions for values passed
between the two languages.
%endif

%package -n	%{devname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Provides:	ffi-devel = %{EVRD}
Obsoletes:	%{mklibname -d ffi 5} < %{EVRD}

%description -n %{devname}
This package contains libraries and header files for developing
applications that use %{name}.

# The static libffi is used to link Host Dalvik while building
# Android from source - please don't remove it.
%package -n	%{staticname}
Summary:	Static libraries for %{name}
Group:		Development/C
Requires:	%{devname} = %{EVRD}
Provides:	ffi-static-devel = %{EVRD}

%description -n %{staticname}
This package contains static libraries for developing
applications that use %{name}.

%prep
%autosetup -p1 -n libffi-%{version}
autoreconf -fiv

%build
%configure --enable-static
%make_build

%install
%make_install
rm -rf %{buildroot}%{_libdir}/pkgconfig \
	%{buildroot}%{_includedir} \
	%{buildroot}%{_mandir} \
	%{buildroot}%{_infodir} \
	%{buildroot}%{_libdir}/*.{a,so}

%if "%{_lib}" == "lib"
%files
%else
%files -n %{libname}
%endif
%{_libdir}/libffi.so.%{major}*

%if 0
%files -n %{devname}
%doc LICENSE README
%{_libdir}/pkgconfig/libffi.pc
%{_includedir}/ffi*.h
%{_libdir}/libffi.so
%{_mandir}/man3/*
%{_infodir}/libffi.info.*

%files -n %{staticname}
%{_libdir}/*.a
%endif
