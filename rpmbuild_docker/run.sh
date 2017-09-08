#!/bin/bash
sudo docker run --cap-add=sys_admin --net=host --rm=true \
	-w "${PWD}" -v "${PWD}":"${PWD}":Z \
	-t rpmbuild "./rpmsource/run.sh"

