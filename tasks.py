
from celery import Celery
from celery import bootsteps
from kombu import Consumer, Exchange, Queue


BROKER_URL = 'amqp://guest@localhost:5672//'
app = Celery('tasks', broker=BROKER_URL)

app.conf.task_create_missing_queues = True

# Add more queues like this, if you need. and add it in the "queues" argument under
# get_consumers function in AMQPConsumer
test_queue = Queue('test', Exchange('test'), routing_key='test', queue_arguments={'x-max-priority': 10})


class AMQPConsumer(bootsteps.ConsumerStep):

    def get_consumers(self, channel):
        return [Consumer(channel,
                         queues=[test_queue],
                         callbacks=[self.handle_message],
                         accept=['json'])]

    @staticmethod
    def handle_message(body, message):
        """
        :param body: message content
        :param message: message dict
        :return:

        message.delivery_info["routing_key"] will give you the routing key, based on which you can redirect to
        different functions
        """
        print('Received New Published Message: {0!r}'.format(body))
        if message.delivery_info["routing_key"] == "test":
            # Use delay or call directly. Calling directly will be sync and delay will make it async.
            test_queue_function.delay(body)
        else:
            another_queue_function.delay(body)
        message.ack()


@app.task
def test_queue_function(body):
    print("test function", body)
    print("111111111")


@app.task
def another_queue_function(body):
    print("default function", body)
    print("22222222")


app.steps['consumer'].add(AMQPConsumer)
