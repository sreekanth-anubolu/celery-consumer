# celery-consumer
Celery Consumer, custom consumer, bootsteps, consumer step

Here is a code to subscribe/consume the messages that are produced from non celery producer.


Ensure you have installed
 
     - RBMQ (brew install rabbitmq)
     - Celery (pip install celery)


**Assumption**

You already has a queue that has messages coming in and you only need consumer. Basically a non celery producer.


Steps to run:
   - Start the rabbitmq server
   - Ensure your producer starts sending messages to the queue.
   - Open the tasks.py and ensure that you change the queue name to what ever is your queue name.
   - All set.. Then run
        - celery worker -A tasks -l INFO

That is all... 
