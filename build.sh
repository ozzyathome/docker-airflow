docker build  --rm -t osb/docker-airflow \
  --build-arg DOCKER_ID=116 \
  --build-arg USER_ID=$(id -u) \
  --build-arg GROUP_ID=$(id -g) .

