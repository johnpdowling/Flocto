import time
import usb1

class FlashForgeError(Exception):
	def __init__(self, message, error):
		super(FlashForgeError, self).__init__(message)
		self.error = error

class FlashForge(object):
	ENDPOINT_CMD_IN   = 0x81
	ENDPOINT_CMD_OUT  = 0x01
	ENDPOINT_DATA_IN  = 0x83
	ENDPOINT_DATA_OUT = 0x03
	BUFFER_SIZE = 128
	
	def __init__(self, vendorid=0x2b71, deviceid=0x0001, autoconnect=True):
		self.vendorid = vendorid
		self.deviceid = deviceid
		
		self._context = usb1.USBContext()
		self._handle = self._context.openByVendorIDAndProductID(self.vendorid, self.deviceid)
		self._handle.claimInterface(0)

	def gcodecmd(self, cmd, timeout=10, retry_counter=5, retry_timeout=1):
		try:
			self._handle.bulkWrite(self.ENDPOINT_CMD_IN, '~{0}\r\n'.format(cmd).encode())
			
			#read data until ok signals end
			data = ''
			cmd_done = False
			while not cmd_done:
				newdata = self._handle.bulkRead(self.ENDPOINT_CMD_OUT, self.BUFFER_SIZE, int(timeout*1000.0)).decode()

				if newdata.strip() == 'ok':
					cmd_done = True
				elif newdata.strip().endswith('ok'):
					cmd_done = True
				
				data = data + newdata
			
			#decode data
			return data.replace('\r', '')
		except usb1.USBError as usberror:
			raise FlashForgeError('USB Error', usberror)
	
	def __del__(self):
		try:
			self._handle.releaseInterface(0)
		except:
			pass

if __name__ == '__main__':
	pass
