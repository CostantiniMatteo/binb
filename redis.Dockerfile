FROM redis

COPY db/dump.rdb /data/dump.rdb

CMD ["redis-server", "/etc/redis/redis.conf"]
