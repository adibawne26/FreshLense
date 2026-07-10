FROM jenkins/jenkins:lts-jdk21

USER root

# Install dependencies
RUN apt-get update && apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    git \
    lsb-release

# Add Docker's official GPG key
RUN install -m 0755 -d /etc/apt/keyrings

RUN curl -fsSL https://download.docker.com/linux/debian/gpg | \
    gpg --dearmor -o /etc/apt/keyrings/docker.gpg

RUN chmod a+r /etc/apt/keyrings/docker.gpg

# Add Docker repository
RUN echo \
"deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
https://download.docker.com/linux/debian \
bookworm stable" \
> /etc/apt/sources.list.d/docker.list

# Install Docker CLI + Compose Plugin
RUN apt-get update && apt-get install -y \
    docker-ce-cli \
    docker-compose-plugin

# Match host Docker group
ARG DOCKER_GID=115

RUN groupdel docker || true
RUN groupadd -g ${DOCKER_GID} docker
RUN usermod -aG docker jenkins

USER jenkins