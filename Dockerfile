FROM centos:7

#RUN yum -y update && Install Ansible
RUN yum -y install epel-release && yum -y install ansible rpm-build redhat-rpm-config libselinux-python gcc

# Get and INstall go
WORKDIR /usr/local
RUN curl -O https://storage.googleapis.com/golang/go1.8.linux-amd64.tar.gz
RUN tar -xf go1.8.linux-amd64.tar.gz

RUN useradd vagrant -u 1000
COPY ./ansible/playbooks /etc/ansible/playbooks/

WORKDIR /
# Execute RPMBUILD Command
CMD ansible-playbook /etc/ansible/playbooks/syncthing-build.yml