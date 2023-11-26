https://ops-coffee.cn/s/hqaprps7w3d-9seegqab2q

django channels celery

channels 3.05  4.0 版本使用的方式不一样

https://channels.readthedocs.io/en/stable/topics/channel_layers.html#using-outside-of-consumers

```python

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
channel_layer = get_channel_layer()

async_to_sync(channel_layer.send)(
                        "chat_lobby",
                        {
                            "type": "chat_message",
                            "message": "tail log => xxxxxxxxxxx"
                        }
                    )
```


这个 channel_layer 发送消息的 type 是 WebsocketConsumer 的一个方法，那直接调用怎么知道我用的是哪个 Consumer 类？

我现在想用channel 做个 tail 日志的功能，想法是用 channel 加 celery 异步调用发送
https://ops-coffee.cn/s/r5spytjrl0jjeauye4q_-q
我借鉴了这个代码，但没实现起来，想手动调用测试下，了解咋实现的