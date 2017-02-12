#!/usr/bin/env python
import sys
import boto3
import uuid
import time
from os.path import expanduser
import md5


db = boto3.resource("dynamodb")

table = db.Table("CNoteHistory")

''' Send history to server '''


def sendHistory(n):

    home = expanduser("~")
    f = open(home + "/.bash_history")

    print "Sending last", n, "entries ...!"

    with table.batch_writer() as batch:

        lines = tail(f, int(n)).split("\n")
        groupId = str(uuid.uuid4())

        for l in range(0, len(lines)):

            s_uuid = str(uuid.uuid4())
            timestamp = int(time.time())

            if (lines[l] != ''):
                batch.put_item(
                    Item={
                        'Uuid': s_uuid,
                        'Timestamp': int(timestamp),
                        'Command': str(lines[l]),
                        'Sequence': int(l),
                        'GroupId': groupId,
                        'Enviroment': 'danilo@server-01',
                        'Comment': 'Empty'
                    }
                )

    print "History sent!"


def help():
    print "Help"


def tail(f, n):
    return "\n".join(f.read().split("\n")[-n:])


def init(argv):
    try:
        n = argv[1]
    except:
        n = 100

    sendHistory(n)


if __name__ == "__main__":
    init(sys.argv)
