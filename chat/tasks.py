from __future__ import absolute_import
from celery import shared_task

import time
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@shared_task
def tailf(channel_name):
    channel_layer = get_channel_layer()
    filename = '/Users/clin/File/Project/djangoChannel/djangoChannel/xxx.log'

    try:
        with open(filename) as f:
            f.seek(0, 2)

            while True:
                line = f.readline()

                if line:
                    print(channel_name, line)
                    async_to_sync(channel_layer.send)(
                        channel_name,
                        {
                            "type": "send.message",
                            "message": "tail log =>" + str(line)
                        }
                    )
                else:
                    time.sleep(0.5)
    except Exception as e:
        print(e)
