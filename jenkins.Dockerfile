FROM jenkins/jenkins:lts-jdk21

USER root

RUN apt-get update \
    && apt-get install -y \
        docker.io \
        curl \
        python3 \
        python3-pip \
        python3-venv \
    && curl -fL --http1.1 -o /tmp/kubectl https://dl.k8s.io/release/v1.36.1/bin/linux/amd64/kubectl \
    && install -o root -g root -m 0755 /tmp/kubectl /usr/local/bin/kubectl \
    && rm /tmp/kubectl \
    && rm -rf /var/lib/apt/lists/*

USER jenkins
