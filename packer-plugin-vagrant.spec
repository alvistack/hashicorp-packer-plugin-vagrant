# Copyright 2024 Wong Hoi Sing Edison <hswong3i@pantarei-design.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

%global debug_package %{nil}

%global source_date_epoch_from_changelog 0

Name: packer-plugin-vagrant
Epoch: 100
Version: 1.1.2
Release: 1%{?dist}
Summary: Packer Plugin for Vagrant
License: MPL-2.0
URL: https://github.com/hashicorp/packer-plugin-vagrant/tags
Source0: %{name}_%{version}.orig.tar.gz
BuildRequires: golang-1.22
BuildRequires: glibc-static
Requires: packer

%description
The Vagrant multi-component plugin can be used with HashiCorp Packer to
create custom images.

%prep
%autosetup -T -c -n %{name}_%{version}-%{release}
tar -zx -f %{S:0} --strip-components=1 -C .

%build
set -ex && \
    export CGO_ENABLED=0 && \
    go build \
        -mod vendor -buildmode pie -v \
        -ldflags "-s -w -extldflags '-static -lm'" \
        -o ./packer-plugin-vagrant .

%install
install -Dpm755 -d %{buildroot}%{_bindir}
install -Dpm755 -t %{buildroot}%{_bindir}/ packer-plugin-vagrant

%files
%license LICENSE
%{_bindir}/*

%changelog
