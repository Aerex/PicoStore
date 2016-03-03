from errors import Error
from local import Local
import lib
import pdb

constants = lib.Constants
#from cloudant import Cloudant


class Factory(object):

	@staticmethod
	def createDB(type, options={}):
		if type == 'local':
			return Local()
		#elif type == 'cloudant':
			#return Cloudant(options)
		#elif type == 'webhook':
			#return Webhook(options)
		else :
			raise Exception('Invalid database')

	@staticmethod
	def setServer(type, options={}):
		pdb.set_trace()
		#if type.lower() in constants.CLOUDANT
			#return Cloudant(options)
		return 0





