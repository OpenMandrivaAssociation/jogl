%define debug_package %{nil}

Summary:	Java bindings for the OpenGL API
Name:		jogl
Version:	1.1.1
Release:	0.6.12
Group:		Development/Java
License:	BSD
URL:		https://jogl.dev.java.net/
# svn co https://svn.java.net/svn/jogl~svn/branches/1.x-maint jogl-1.1.1
Source0:	%{name}-%{version}.tar.bz2
# match gluegen package
# svn co https://svn.java.net/svn/gluegen~svn/branches/1.0b06-maint gluegen-1.0b06
Source1:	gluegen-1.0b06.tar.bz2
Source2:	jogl.properties
Patch0:		%{name}-1.1.1-src-no-link-against-sun-java.patch
# http://pkgs.fedoraproject.org/gitweb/?p=gluegen.git;a=blob;f=fix-antlr-classpath.patch
Patch1:		fix-antlr-classpath.patch
BuildRequires:	ant
BuildRequires:	ant-antlr
BuildRequires:	antlr
BuildRequires:	jpackage-utils
BuildRequires:	mesa-common-devel
BuildRequires:	java-rpmbuild
BuildRequires:	unzip
BuildRequires:	update-alternatives
BuildRequires:	xml-commons-apis
BuildRequires:	cpptasks
BuildRequires:	pkgconfig(xt)
Requires:	java >= 1.5

%description 
The JOGL Project hosts a reference implementation of the Java bindings for
OpenGL API, and is designed to provide hardware-supported 3D graphics to
applications written in the Java programming language.

It is part of a suite of open-source technologies initiated bu the Game
Technology Group at Sun Microsystems.

JOGL provides full access to the APIs in the OpenGL 1.5 specification as
well as nearly all vendor extensions, and integrated with the AWT and Swing
widget sets.

%package javadoc
Summary:	Javadoc for jogl
Group:		Development/Java

%description javadoc
Javadoc for jogl.

%package manual
Summary:	User documetation for jogl
Group:		Development/Java

%description manual
Usermanual for jogl.


%prep
%setup -q -b 1
ln -sf gluegen-1.0b06 ../gluegen
pushd make
%patch0 -p0
popd
pushd ../gluegen-1.0b06
%patch1 -p1
popd

%__cp %{SOURCE2} make

%build
export OPT_JAR_LIST="antlr ant/antlr"
export CLASSPATH=$(build-classpath antlr ant/ant-antlr)

rm -rf doc/jogl-manual/*/.svn

pushd make
perl -pi -e 's@/usr/X11R6/%{_lib}@%{_libdir}@g' build.xml

%ant \
    -Duser.home=%{_topdir}/SOURCES \
    -Dantlr.jar=$(build-classpath antlr) \
    all \
    javadoc.dev.x11

popd

%install

# jars
%__install -dm 755 %{buildroot}%{_javadir}
%__install -m 644 build/%{name}.jar \
	%{buildroot}%{_javadir}/%{name}-%{version}.jar
pushd %{buildroot}%{_javadir}
	for jar in *-%{version}*; do
		ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`
	done
popd

# native lib
%__install -dm 755 %{buildroot}%{_libdir}
%__install -m 644 build/obj/lib*.so \
	%{buildroot}%{_libdir}

# javadoc
%__install -dm 755 %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -pr javadoc_jogl_dev/* \
	%{buildroot}%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name} # ghost symlink

%post javadoc
%__rm -f %{_javadocdir}/%{name}
ln -s %{name}-%{version} %{_javadocdir}/%{name}

%files
%{_javadir}/*.jar
%attr(755,root,root) %{_libdir}/libjogl.so
%attr(755,root,root) %{_libdir}/libjogl_awt.so

%files javadoc
%doc %{_javadocdir}/%{name}-%{version}
%ghost %doc %{_javadocdir}/%{name}

%files manual
%doc doc/*


