#
# Conditional build:
%bcond_with	tests	# pytest tests [use ptys, so not on builders]
%bcond_without	python2 # CPython 2.x module
%bcond_with	python3 # CPython 3.x module (built from python3-pytest-timeout.spec)

%define 	module	pytest-timeout
Summary:	pytest plugin to abort hanging tests
Summary(pl.UTF-8):	Wtyczka pytesta do przerywania zawieszonych testów
Name:		python-%{module}
# keep 1.x here for python2/pytest<5 support
Version:	1.4.2
Release:	8
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/pytest-timeout/
Source0:	https://files.pythonhosted.org/packages/source/p/pytest-timeout/pytest-timeout-%{version}.tar.gz
# Source0-md5:	552cc293447b00f7a294ce7a1fb3839f
URL:		https://github.com/pytest-dev/pytest-timeout
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-pexpect
BuildRequires:	python-pytest >= 3.6.0
BuildRequires:	python-pytest-cov
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.5
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-pexpect
BuildRequires:	python3-pytest >= 3.6.0
BuildRequires:	python3-pytest-cov
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a plugin which will terminate tests after a certain timeout.
When doing so it will show a stack dump of all threads running at the
time. This is useful when running tests under a continuous integration
server or simply if you don't know why the test suite hangs.

%description -l pl.UTF-8
Ta wtyczka przerywa testy po upłynięciu określonego limitu czasu. Przy
tym pokazuje zrzut stosu wszystkich wątków działających w tej chwili.
Jest to przydatne przy uruchamianiu testów na serwerze ciągłej
integracji lub jeśli nie wiemy, dlaczego testy się zawieszają.

%package -n python3-%{module}
Summary:	py.test plugin to abort hanging tests
Summary(pl.UTF-8):	Wtyczka py.test do przerywania zawieszonych testów
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.5

%description -n python3-%{module}
This is a plugin which will terminate tests after a certain timeout.
When doing so it will show a stack dump of all threads running at the
time. This is useful when running tests under a continuous integration
server or simply if you don't know why the test suite hangs.

%description -n python3-%{module} -l pl.UTF-8
Ta wtyczka przerywa testy po upłynięciu określonego limitu czasu. Przy
tym pokazuje zrzut stosu wszystkich wątków działających w tej chwili.
Jest to przydatne przy uruchamianiu testów na serwerze ciągłej
integracji lub jeśli nie wiemy, dlaczego testy się zawieszają.

%prep
%setup -q -n %{module}-%{version}

%build
%if %{with python2}
%py_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=pytest_cov.plugin,pytest_timeout \
PYTHONPATH=$(pwd) \
%{__python} -m pytest
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=pytest_cov.plugin,pytest_timeout \
PYTHONPATH=$(pwd) \
%{__python3} -m pytest
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc LICENSE README.rst
%{py_sitescriptdir}/pytest_timeout.py[co]
%{py_sitescriptdir}/pytest_timeout-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc LICENSE README.rst
%{py3_sitescriptdir}/pytest_timeout.py
%{py3_sitescriptdir}/__pycache__/pytest_timeout.cpython-*.py[co]
%{py3_sitescriptdir}/pytest_timeout-%{version}-py*.egg-info
%endif
