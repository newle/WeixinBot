#!/usr/bin/env python
# coding: utf-8
import time
import json
import redis


redis_connect = redis.StrictRedis(host="127.0.0.1", port=6379, db=0)

def redis_get_all_process(user_name):
    """
        获取该用户的所有的待操作的数据
    """
    current_ts = int(time.time())
    response = []
    reserved_item = []
    item = redis_connect.lpop(user_name)
    while item != None:
        process = json.loads(item.decode("utf8"))
        if process['ts'] <= current_ts:
            response.append(process['message'])
        else:
            reserved_item.append(item)
        item = redis_connect.lpop(user_name)


    for item in reserved_item:
        redis_connect.lpush(user_name, item)

    return response

def main():
    print(redis_get_all_process("@7819007286afc228ac83de33dec32198"))


if __name__ == "__main__":
    main()
