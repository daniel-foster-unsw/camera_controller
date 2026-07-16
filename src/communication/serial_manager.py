import serial

from communication.communication_interface import CommunicationInterface


class SerialManager(CommunicationInterface):

    def __init__(self):

        self.configuration = None
        self.logger = None
        self.serial_port = None
        self.connected = False
        self.enabled = False
        self.port = None
        self.baud_rate = None
        self.timeout = None


    def initialise(self, configuration, logger):

        self.configuration = configuration
        self.logger = logger

        self.enabled = configuration.get(
            "serial",
            "enabled"
        )

        self.port = configuration.get(
            "serial",
            "port"
        )

        self.baud_rate = configuration.get(
            "serial",
            "baud_rate"
        )

        self.timeout = configuration.get(
            "serial",
            "timeout"
        )

        if not self.enabled:
            self.logger.info(
                f"Serial interface disabled (configured port: {self.port})."
            )
            return

        self.serial_port = serial.Serial(
            port=self.port,
            baudrate=self.baud_rate,
            timeout=self.timeout
        )



        self.connected = True

        self.logger.info(
            f"Serial interface enabled on {self.port} @ {self.baud_rate} baud."
        )

    def recieve(self):
        if not self.connected:
            return None

        line = self.serial_port.readline()

        if not line:
            return None
            
        json_string = line.decode("utf-8").strip()

#        return line.decode("utf-8").strip()
        try:
            return json_string

        except Exception as e:
            self.logger.error(f"Invalid command received: {e}")
        return None
        

    def send(self, message):
#    def send(self, response):

        if not self.connected:
            return
        
#        message = response.to_json()

        self.serial_port.write(
            (message + "\n").encode("utf-8")
        )


    def stop(self):

        if self.serial_port:
            self.serial_port.close()
        self.connected = False
        self.logger.info(
            "Serial connection closed."
        )