import lib
import pdb

promise = lib.Promise
Utility = lib.Utility
constants = lib.Constants
error = lib.Error
Factory = lib.Factory
Collection = lib.Collection

class PicoStore(object):
	offline = True
	collections = {}
	password = None

	def __init__(self, options={}):
		if len(options) != 0:
			self.server = Factory.setServer(options)
		dbType = 'local'
		self.db = Factory.createDB(dbType)
		
		
	# Set the adapter and additional search field options
	# @param key the collection name or key
	# @param cols the collections
	def _setOptions(self,key, cols):
 		options = {}
		if cols[key].has_key(constants.adapter):
			options[constants.adapter] = cols[key][constants.adapter]
		else :
			options[constants.adapter] = {}

		if cols[key].has_key(constants.additionalSearchFields):
			options[constants.additionalSearchFields] = cols[key][constants.additionalSearchFields]
		return options

	def get(self, collectionName):
		try :
			return self.collections[collectionName]
		except KeyError as e:
			return None




	#Adding collection to all collections
	# @param collectionName collection name
	# @param collection the collection content
	def _addToCollections(self,key, value):
		self.collections[key] = value

	# Generate the search fields for the collection
	# @param key the collection name or key
	# @cols cols the collections
	def _generateSearchFields(self,key, cols):
		if cols[key].has_key(constants.searchFields):
			return cols[key][constants.searchFields]
		else:
			return {}

	# Create a new instance of a collection
	# @param name the name of the collection
	# @param searchFields the searchFields for the collection
	# @param options the options for the collection
	def _provisionCollection(self, name, searchFields, options):
		db = self.db
		analytics = False
		localKeyGen = False
		username = constants.default_username
		collectionPassword = ''
		collectionAdapter = ''
		collectionName = ''
		collectionPBKDF2Iterations = ''
		collectionSearchFields = {}
		collectionAdditionalSearchFields = {}
		secureRandom = ''
		collectionPBKDF2Iterations = 10000

		if Utility.isObject(options):
			if options.has_key(constants.analytics) and Utility.isBoolean(options[constants.analytics]):
				analytics = options[constants.analytics]

			if options.has_key(constants.localKeyGen) and Utility.isBoolean(options[constants.localKeyGen]):
				localKeyGen = options[constants.localKeyGen]

			if options.has_key(constants.username) and Utility.isString(options[constants.username]) and len(options[constants.username]) > 0:
				username = options[constants.username]

				if not username.isalnum() or Utility.isReservedWord(username):
					obj = {
						'src': 'provision',
						'err': constants.INVALID_USERNAME
					}
					return error(obj)

			if not self.password == None:
				if Utility.isString(password) and len(password) > 0:
					collectionPassword = password
				else:
					obj = {
						'src': 'provision',
						'err': constants.INVALID_PASSWORD_EXPECTED_ALPHANUMERIC_STRING_WITH_LENGTH_GREATER_THAN_ZERO
					}
					return error(obj)
					#TODO: create an error object[invalid password expected alphanum]

			if options.has_key(constants.password) and Utility.isString(options[constants.password]) and len(options[constants.password]) > 0:
				collectionPassword = options[constants.password]

			if Utility.isValidAdapter(options[constants.adapter]):
				collectionAdapter = options[constants.adapter]


		if name.isalnum() and not Utility.isNumber(name[0]):
			collectionName = name
		else:
			obj = {
				'src': 'provision',
				'err': constants.BAD_PARAMETER_EXPECTED_ALPHANUMERIC_STRING
			}
			return error(obj)

		#check searchFields
		if Utility.isSimpleObject(searchFields) and not Utility.containsDuplicateKeys(searchFields):
			if not Utility.isValidSchemaObject(searchFields):
				obj = {
					'src': 'provision',
					'err': constants.INVALID_SEARCH_FIELD_TYPES
				}
				return error(obj)
			collectionSearchFields = searchFields
		else :
			obj = {
				'src': 'provision',
				'err': constants.BAD_PARAMETER_EXPECTED_SIMPLE_OBJECT
			}
			return error(obj)

		if Utility.isObject(options) and options.has_key(constants.additionalSearchFields):
			if not Utility.isSimpleObject(options[constants.additionalSearchFields]) or Utility.containsDuplicateKeys(options[constants.additionalSearchFields]):
				obj = {
					'src': 'provision',
					'err': constants.BAD_PARAMETER_EXPECTED_SIMPLE_OBJECT
				}
				return error(obj)
				## TODO: create an error object [bad parametere expected simple object]
			else:
				collectionAdditionalSearchFields = options[constants.additionalSearchFields]

		if Utility.isObject(options) and options.has_key(constants.pbkdf2Iterations):
			collectionPBKDF2Iterations = options[constants.pbkdf2Iterations]

		instance = Collection(collectionName, collectionSearchFields, collectionAdditionalSearchFields, username, db)
		collectionOptions = {
			'analytics' : analytics,
			'collectionPassword': collectionPassword,
			'additionalSearchFields': collectionAdditionalSearchFields,
			'username': username,
			'localKeyGen': localKeyGen,
			'secureRandom': secureRandom,
			'pbkdf2Iterations': collectionPBKDF2Iterations
		}


		#if(len(collectionPassword) > 0 and not localKeyGen):
			#TODO: secureRandom method check WLEncrytpion cache for ideas
		db.provision(collectionName, collectionSearchFields, collectionOptions)

		return instance

	def init(self,cols, options={}):
		q = promise()
		db = self.db
		if Utility.countKeys(cols) < 1:
			q.fulfill({})
		else:
			for col in cols:
				options = self._setOptions(col, cols)
				searchFields = self._generateSearchFields(col, cols)
				collectionInstance = self._provisionCollection(col, searchFields, options)
				self._addToCollections(col, collectionInstance)
				username = options[constants.username] if options.has_key(constants.username) and len(options[constants.username]) else constants.default_username
				if type(collectionInstance) is error:
					q.reject(collectionInstance)
					break

			q.fulfill(self.collections)
		
		return q

	def destroy(self,usr=''):
		q = promise()
		db = self.db
		errorObject = {
			'src': 'destroy',
			'err': constants.ERROR_DURING_DESTROY
		}
		if Utility.isString(usr) and len(usr) > 0:
			username = usr
			res = db.destroy(username)
		else :
			self.collections = {}
			res = db.destroy()

		if res == 0:
			q.fulfill(constants.SUCCESS)
		else:
			q.reject(error(errorObject))

		return q

	def closeAll(self):
		q = promise()
		self.collections = {}
		result = self.db.closeAll()

		if type(result) is error:
			q.reject(result)
		else:
			q.fulfill(result)

		return q








