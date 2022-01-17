from alvarium.contracts.publish import PublishWrapper
import paho.mqtt.client as mqtt
from .interfaces import StreamProvider
from .contracts import  MQTTConfig
from .exceptions import StreamException

class MQTTStreamProvider( StreamProvider ):
    """implementation of the MQTT StreamProvider"""

    mqttc: mqtt.Client
    mqtt_config: MQTTConfig
    CONNECTION_TIMEOUT = 2

    def __init__(self, mqtt_config: MQTTConfig ):
        self.mqtt_config = mqtt_config
        self.mqttc = mqtt.Client(client_id=self.mqtt_config.client_id,
                                 clean_session=self.mqtt_config.is_clean)
        self.mqttc.username_pw_set(self.mqtt_config.user, self.mqtt_config.password)
    
    def connect(self) -> None:
        if (not self.mqttc.is_connected()):
            self.mqttc.connect(host=self.mqtt_config.provider.host, keepalive=self.CONNECTION_TIMEOUT)
        else:
            self.mqttc.reconnect()
        
    def close(self) -> None:
        self.mqttc.disconnect()

    def publish(self, wrapper: PublishWrapper) -> None:
        if (not self.mqttc.is_connected()):
            self.mqttc.reconnect()
        
        for topic in self.mqtt_config.topics:
            try:
                message_info = self.mqttc.publish(topic=topic,
                                    payload=wrapper.to_json(), 
                                    qos=self.mqtt_config.qos)
                if not message_info.is_published():
                    raise StreamException ('Message was not published')
            except ValueError as e:
                raise StreamException (f"cannot publish to topic {topic}.", e) 
            
            
            

            

    

