import sys

from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment


class PayPalClient:
    def __init__(self):
        self.client_id = "AQAfFYjRpMU8-YYvcRz3sc7d13iaboZFiAnvuLz67pjVVIiIXYpirEXlbpS6TPKmhzNH0flAflS2u_mZ"
        self.client_secret = "EA5QjhYzVmjH-xQIFILOGzCEFPbO7Ja0UH0Vyc63ivpYOuq3-Xb1cVAteCkDFXoFdssiruAIqg2FutgP"
        self.environment = SandboxEnvironment(client_id=self.client_id, client_secret=self.client_secret)
        self.client = PayPalHttpClient(self.environment)
