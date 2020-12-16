ExecStartPre=/sbin/setcap 'cap_ipc_lock=+ep' $(readlink -f $(which vault))
export MYUID=1001
export MYGID=1001
docker-compose -f docker-compose-LocalExecutor.yml up
