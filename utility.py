import re
import math
import sys
import hashlib
import pydash
from constants import Constants

class Utility(object):

	@staticmethod
	def countKeys(collection):
		count = 0
		if not type(collection) is dict:
			return -1
		for key in collection:
			count+=1
		return count

	@staticmethod
	def isObject(obj):
		if type(obj) is dict:
			return True
		else :
			return False

	@staticmethod
	def isEmptyArray(obj):
		if type(obj) is list and len(obj) == 0:
			return True
		else:
			return False

	@staticmethod
	def isBoolean(obj):
		if type(obj) is bool:
			return True
		else:
			return False

	@staticmethod
	def isString(obj):
		if type(obj) is str:
			return True
		else:
			return False

	@staticmethod
	def isReservedWord(obj):
		default_username = 'jsonstore'
		default_keychain_username = 'jsonstorekey'
		default_keychain_id = 'dpk'
		if not type(obj) is str:
			return False

		##ignore empty strings
		if type(obj) is str and len(obj) == 0:
			return False

		usr = obj.lower()

		isDefaultUsername = True if usr in default_username else False
		isDefaultKeychainUsername = True if usr in default_keychain_username else False
		isDefaultKeychainID = True if usr in default_keychain_id else False


		return True if isDefaultUsername or isDefaultKeychainUsername or isDefaultKeychainID else False

	@staticmethod
	def hasJSONSearchFields(obj):
		fields = ['_id', '_json', '_deleted', '_operation', '_dirty']

		return (len(pydash.arrays.intersection(obj, fields)) > 0)



	@staticmethod
	def isSimpleObject(obj):
		if not type(obj) is dict:
			return False
		for key in obj:
			if obj.has_key(key) and type(obj[key]) is dict or obj[key] == None or type(obj[key]) is list:
					return False

		return True

	@staticmethod
	def containsDuplicateKeys(obj):
		keys = []
		index = 0
		if not type(obj) is dict:
			return True
		for key in obj:
			if obj.has_key(key):
				keys.append(key.lower())

		if len(keys) == 0:
			return False

		keys.sort()

		for index in range(len(keys)-1):
			if keys[index+1] == keys[index]:
				return True

		return False

	@staticmethod
	def isValidAdapter(obj):
		if type(obj) is dict and obj.has_key('name') and type(obj['name']) is str and len(obj['name']) > 0:
			return True
		else :
			return False

	@staticmethod
	def isNumber(obj):

		if type(obj) is bool or type(obj) is str:
			return False

		return isinstance(obj, (int, long, float))

	@staticmethod
	def isInt(obj):
		return True if type(obj) is int else False

	@staticmethod
	def isPartOfSearchFields(query, searchFields, additionalSearchFields={}):
		if not Utility.isSimpleObject(query) or not Utility.isSimpleObject(searchFields):
			return False
		elif type(query) is dict and len(query) == 0:
			return False

		allSearchFields = {}
		allSearchFields['_id'] = 'number'

		if type(additionalSearchFields) is dict or not additionalSearchFields == None:
			allSearchFields = searchFields.copy()
			allSearchFields.update(additionalSearchFields)


		for key in query:
			if not allSearchFields.has_key(key) and (query.has_key(key) and len(query) > 0):
				return False

		return True

	@staticmethod
	def isArrayOfSearchFields(filterArray, allSearchFields):
		if not type(filterArray) is list:
			return False

		size = len(filterArray)

		while size > 0:
			if not filterArray[size-1] in allSearchFields:
				return False
			size = size - 1

		return True


	@staticmethod
	def isArrayOfObjects(obj):
		if not type(obj) is list or len(obj) < 1:
			return False

		for x in range(len(obj)):
			if not Utility.isObject(obj[x]):
				return False

		return True

	@staticmethod
	def handleQueryObject(query, searchFields, additionalSearchFields={}):
		if Utility.isSimpleObject(query):
			if Utility.isPartOfSearchFields(query, searchFields, additionalSearchFields):
				return [query]
			else :
				raise Exception('INVALID_SEARCH_FIELD')
		elif Utility.isArrayOfObjects(query):
			for x in range(len(query)):
				if not Utility.isPartOfSearchFields(query[x], searchFields, additionalSearchFields):
					raise Exception('INVALID_SEARCH_FIELD')
			return query
		elif type(query) is list and len(query) < 1:
			return []

		else:
			raise Exception('BAD_PARAMETER_EXPECTED_SIMPLE_OBJECT')

	@staticmethod
	def handleOptions(options, searchFields, additionalSearchFields):
		opts = options
		if Utility.isObject(options):
			if not options.has_key(Constants.limit) and (options.has_key(Constants.offset) and Utility.isInt(options[Constants.offset])):
				return Constants.OFFSET_WITHOUT_LIMIT
			if options.has_key(Constants.limit) and Utility.isInt(options[Constants.limit]):
				if options[Constants.limit] < 0:
					if options.has_key(Constants.offset):
						return Constants.INVALID_LIMIT_OR_OFFSET

				opts[Constants.limit] = options[Constants.limit]

			if options.has_key(Constants.offset) and Utility.isInt(options[Constants.offset]):
				if options[Constants.offset] < 0:
					return Constants.INVALID_LIMIT_OR_OFFSET

				opts[Constants.offset] = options[Constants.offset]

			if options.has_key(Constants.sort) and Utility.isArrayOfObjects(options[Constants.sort]) and len(options[Constants.sort]) > 0:
				# check to see if the only one property with the string 'asc' or desc

				for x in range(len(options[Constants.sort])):
					sortObj = options[Constants.sort][i]

					if not Utility.isValidSortObject(sortObj, searchFields, additionalSearchFields):
						return Constants.INVALID_SORT_OBJECT

				opts[Constants.sort] = options[Constants.sort]

			elif options.has_key(Constants.sort) and not (type(options[Constants.sort]) is dict and len(options[Constants.sort]) == 0):
				return Constants.INVALID_SORT_OBJECT

		return opts


	@staticmethod
	def hashPassword(password):
		return hashlib.sha256(password).hexdigest()

	@staticmethod
	def isValidSchemaObject(obj):
		validTypes = ['string', 'integer', 'boolean', 'number']
		invalidKeys = [Constants.field_id, Constants.field_operation, Constants.field_deleted, Constants.field_dirty, Constants.field_json]
		for key in obj:
			if obj.has_key(key) and not obj[key] in validTypes or key in invalidKeys:
				return False

		return True

	@staticmethod
	def isInvalidField(obj):
		invalidKeys = [Constants.field_id, Constants.field_operation, Constants.field_deleted, Constants.field_dirty, Constants.field_json]
		if type(obj) is str and not obj in invalidKeys:
			return False
		else:
			return True

	@staticmethod
	def isValidType(obj):
		validTypes = ['string', 'integer', 'boolean', 'number']
		if type(obj) is str and obj in validTypes:
			return True
		else:
			return False

	@staticmethod
	def getSafeSearchField(obj):
		db_chars = ['@', '$', '^', '&', '|', '>', '<', '?', '-']
		if not type(obj) is str:
			return None

		for char in db_chars:
			obj = obj.replace(char, "")

		obj = obj.replace('.', '_')

		return obj

	@staticmethod
	def getDataArray(obj):
		arrayOfObjects = []

		if Utility.isObject(obj):
			arrayOfObjects.append(obj)
		elif Utility.isArrayOfObjects(obj):
			for x in range(len(obj)):
				if Utility.isObject(obj[x]):
					arrayOfObjects.append(obj[x])
				else:
					return []

		return arrayOfObjects





