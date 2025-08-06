from fastapi import APIRouter
from app.types.models import TransferModel, ConvertModel
from kafka import KafkaProducer, KafkaConsumer
from dotenv import load_dotenv
import os
import asyncio
import json 
from app.routers.convert import read_converter
load_dotenv()


router = APIRouter(
    prefix="/transaction",
    tags=["transaction"],
)

KAFKA_BROKER_URL = os.getenv('KAFKA_BROKER_URL')
KAFKA_TOPIC = 'transaction'

stop_polling_event = asyncio.Event()

@router.post('/payment')
async def submit_payment(params: TransferModel):
    producer = KafkaProducer(bootstrap_servers=os.getenv('KAFKA_BROKER_URL'))
    producer.send(KAFKA_TOPIC, json.dumps(params.dict()).encode())

    return {'message': 'Payment submitted for processing'}

def create_kafka_consumer():
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=[KAFKA_BROKER_URL],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='your-consumer-group-id'
    )

    return consumer

async def poll_consumer(consumer: KafkaConsumer):
    try:
        while not stop_polling_event.is_set():
            print('Trying to poll again...')
            records = consumer.poll(5000, 250)

            if records:
                for record in records.values():
                    for message in record:
                        recieved = json.loads(message.value)
                        params = ConvertModel(idr = recieved['send_amount'])
                        result = await read_converter(params)

                        output = {
                            'sender': recieved['sender'],
                            'reciever': recieved['receiver'],
                            'status': 'recieved',
                            'amount': {
                                'currency': 'IDR',
                                'amount': result['amount'],
                                'amount_in_text': result['writting']
                            }
                        }

                        print(output)
                        consumer.commit()

            await asyncio.sleep(5)

    except Exception as error:
        print(error)
        raise Exception
    finally:
        consumer.close()

tasklist = []

@router.get('/trigger')
async def trigger_polling():
    if not tasklist:
        stop_polling_event.clear()
        consumer = create_kafka_consumer()
        task = asyncio.create_task(poll_consumer(consumer=consumer))
        tasklist.append(task)

        return "Has been started"

@router.get('/stop-trigger')
async def stop_trigger_polling():
    stop_polling_event.set()

    if tasklist:
        tasklist.pop()

    return "Has been stopped"


