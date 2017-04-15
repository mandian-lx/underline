%{?_javapackages_macros:%_javapackages_macros}

Summary:	A Git-like command-line parser for Java with no strings attached 
Name:		underline
Version:	1.0.0
Release:	1
License:	ASL 2.0
Group:		Development/Java
URL:		https://github.com/michel-kraemer/%{name}/
Source0:	https://github.com/michel-kraemer/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:	https://repo1.maven.org/maven2/de/undercouch/%{name}/%{version}/%{name}-%{version}.pom
Patch0:		%{name}-1.0.0-gradle-use-local-repo.patch 
Patch1:		%{name}-1.0.0-gradle-remove-custom-repo.patch 
BuildArch:	noarch

BuildRequires:	gradle-local
BuildRequires:	maven-local
BuildRequires:	mvn(junit:junit)

%description
underline is a command-line parser for Java. It allows for creating
command-line programs with a Git-like interface. It is lightweight
and has no dependencies to external libraries ("no strings attached").

The library is really low-level but extremely flexible. There are a
number of alternatives (such as JCommander or Apache Commons CLI) but
underline enables you to fully control how your command-line arguments
are parsed and handled. If you're stuck with one of the existing libraries
and need more flexibility then underline may be the right tool for you.

%files -f .mfiles
%doc README.md
%doc LICENSE.txt

#----------------------------------------------------------------------------

%package javadoc
Summary:	Javadoc for %{name}

%description javadoc
API documentation for %{name}.

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt

#----------------------------------------------------------------------------

%prep
%setup -q

# Delete prebuild JARs
find . -name "*.jar" -delete
find . -name "*.class" -delete

# Apply all patches
%patch0 -p1 -b .local
%patch1 -p1 -b .repo

# Add pom.xml
cp -a %{SOURCE1} ./pom.xml

# fix deps in pom.xml
%pom_add_dep junit:junit::test

%build
# FIXME: test fails
gradle build install -x test --offline -s
%mvn_artifact pom.xml build/libs/%{name}-%{version}-%{version}.jar

%install
%mvn_install -J build/docs/javadoc

