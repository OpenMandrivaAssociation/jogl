Summary:	Java bindings for the OpenGL API
Name:		jogl
Version:	1.1.1
Release:	%mkrel 0.6.4
Group:		Development/Java
License:	BSD
URL:		http://jogl.dev.java.net/
Source0:	https://jogl.dev.java.net/files/documents/27/17108/%{name}-%{version}-src.zip
Source1:	%{name}.properties
Patch0:		%{name}-1.1.1-src-no-link-against-sun-java.patch
BuildRequires:	ant
BuildRequires:	ant-antlr
BuildRequires:	antlr
BuildRequires:	jpackage-utils
BuildRequires:	mesa-common-devel
BuildRequires:	java-rpmbuild
BuildRequires:	unzip
BuildRequires:	update-alternatives
BuildRequires:	xml-commons-apis
Requires:	java >= 1.5
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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
%setup -q -n %{name}
pushd make
%patch0 -0
popd

%__cp %{SOURCE1} make

%build
export OPT_JAR_LIST="antlr ant/antlr"
export CLASSPATH=$(build-classpath antlr ant/ant-antlr)

pushd make

perl -p -i -e 's@/usr/X11R6/%{_lib}@%{_libdir}@g' build.xml

%ant \
    -Djogl.cg="0" \
    -Duser.home=%{_topdir}/SOURCES \
    -Dantlr.jar=$(build-classpath antlr)

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
%__cp -pr javadoc_public/* \
	%{buildroot}%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name} # ghost symlink

%clean
[ -d %{buildroot} -a "%{buildroot}" != "" ] && %__rm -rf %{buildroot}
 
%post javadoc
%__rm -f %{_javadocdir}/%{name}
ln -s %{name}-%{version} %{_javadocdir}/%{name}

%files
%defattr(644,root,root,755)
%{_javadir}/*.jar
%{_libdir}/libjogl.so
#%{_libdir}/libjogl_awt.so
#%{_libdir}/libjogl_drihack.so

%files javadoc
%defattr(-,root,root)
%doc %{_javadocdir}/%{name}-%{version}
%ghost %doc %{_javadocdir}/%{name}

%files manual
%defattr(-,root,root)
%doc doc/*
