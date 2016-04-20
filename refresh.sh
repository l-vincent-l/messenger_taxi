git fetch && git pull
redis-cli KEYS "*:864202940369007" | xargs redis-cli DEL
supervisorctl restart taxi
tail -f /var/log/supervisor/taxi-std*
