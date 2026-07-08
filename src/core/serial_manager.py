import serial

class SerialManager:

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

        self.serial_port = serial.Serial(
            port=self.port,
            baudrate=self.baud_rate,
            timeout=self.timeout

        )


        if not self.enabled:
            self.logger.info(
                "Serial interface disabled."
            )
            return
        self.serial_port = serial.Serial(
            port=self.port,
            baudrate=self.baud_rate,
            timeout=self.timeout

        )

        self.connected = True

        self.logger.info(
            f"Opened serial port {self.port}"
        )

        def read(self):
            if not self.connected:
                return None

            line = self.serial_port.readline()

            if not line:
                return None

            return line.decode("utf-8").strip()
        
        def write(self, message):

            if not self.connected:
                return

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