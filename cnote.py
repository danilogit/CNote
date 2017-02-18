#!/usr/bin/env python
import sys
import boto3
import uuid
import time
from os.path import expanduser
from boto3.dynamodb.conditions import Attr
import md5


class CNote:

    db = boto3.resource("dynamodb")
    table = db.Table("CNoteHistory")

    def sendHistory(self, n):

        home = expanduser("~")
        f = open(home + "/.bash_history")

        print "Sending last", n, "entries ...!"

        with self.table.batch_writer() as batch:

            lines = self.tail(f, int(n)).split("\n")
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

        print "History Sent!"

    def help(elf):
        print "Help"


    def tail(self, f, n):
        return "\n".join(f.read().split("\n")[-n:])


    def search(self, text):
        response = self.table.scan(
        Limit=100,
        Select='SPECIFIC_ATTRIBUTES',
        ReturnConsumedCapacity='TOTAL',
        ProjectionExpression='Command, #TS, #S, Enviroment',
        FilterExpression=Attr('Command').contains(text),
        ExpressionAttributeNames={
        '#TS': 'Timestamp', "#S": "Sequence"
        },
        ConsistentRead=False )

        for i in response['Items']:
            print ">", i['Command']


    def __init__(self, argv):

        try:
            n = argv[1]
        except:
            n = 100

        #self.sendHistory(n)
        self.search(n)


if __name__ == "__main__":
    app = CNote(sys.argv);
