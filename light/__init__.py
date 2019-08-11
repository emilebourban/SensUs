from gpiozero import  PWMLED

class Light:

	def __init__(self, gpio, min_intensity, max_intensity):
		self.gpio = gpio
		self.min_intensity = min_intensity
		self.max_intensity = max_intensity
		self.led = PWMLED(self.gpio)

	def on(self):
		self.led.value = self.max_intensity

	def off(self):
		self.led.value = self.min_intensity



