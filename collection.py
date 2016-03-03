import lib
import pdb
promise = lib.Promise
error = lib.Error
Utility = lib.Utility
Constants = lib.Constants
class Collection(object):

	def __init__(self, collectionName, collectionSearchFields, collectionAdditionalSearchFields, username, db):
		self.name = collectionName
		self.searchFields = collectionSearchFields
		self.additionalSearchFields = collectionAdditionalSearchFields
		self._username = username
		self.db = db

	def find(self, query, options={}):
		db = self.db
		q = promise()
		options = Utility.handleOptions(options, self.searchFields, self.additionalSearchFields)
		if Utility.isSimpleObject(query) and len(query.keys()) == 0:
			query = [query]
		elif type(query) is dict and len(query) == 0:
			query = [{}]

		if type(options) is int:
			obj = {
				'src': 'find',
				'err': options
			}
			q.reject(error(obj))

		result = db.find(self.name, query, options)

		if type(result) is error:
			q.reject(result)
		else:
			q.fulfill(result)
		return q

	def findAll(self):
		db = self.db
		q = promise()
		result = db.findAll(self.name)

		if type(result) is error:
			q.reject(result)
		else:
			q.fulfill(result)

		return q

	def count(self, query, options={}):
		db = self.db
		q = promise()
		if Utility.isSimpleObject(query) and len(query.keys()) == 0:
			query = [query]
		elif type(query) is dict and len(query) == 0:
			query = [{}]

		if type(options) is int:
			obj = {
				'src': 'count',
				'err': options
			}
			q.reject(error(obj))

		result = db.count(self.name, query, options)

		if type(result) is error:
			q.reject(result)
		else:
			q.fulfill(result)

		return q


	def add(self, data, options={}):
		db = self.db
		q = promise()
		dataArray = Utility.getDataArray(data)
		if Utility.isSimpleObject(self.additionalSearchFields) and options.has_key(Constants.additionalSearchFields):
			if not Utility.isPartOfSearchFields(options[Constants.additionalSearchFields], self.searchFields, self.additionalSearchFields):
				obj = {
					'src': 'add',
					'err': Constants.INVALID_ADD_INDEX_KEY
				}
				q.reject(error(obj))

		if type(data) is dict and len(data) == 0 or type(data) is list and len(data) == 0:
			q.fulfill(0)
		elif len(dataArray) > 0:
			result = db.add(data, self.name, self.searchFields, options)
			q.fulfill(result)
		else:
			obj = {
				'src': 'add',
				'err': Constants.BAD_PARAMETER_EXPECTED_DOCUMENT_OR_ARRAY_OF_DOCUMENTS
			}
			q.reject(error(obj))

		return q

	def replace(self, data, options={}):
		db = self.db
		q = promise()
		dataArray = Utility.getDataArray(data)
		if not options.has_key(Constants.markDirty):
			options[Constants.markDirty] = False

		if type(data) is dict and len(data) == 0 or type(data) is list and len(data) == 0:
			q.fulfill(0)
		elif len(dataArray) > 0:
			result = db.replace(data, self.name, self.searchFields, options)
			if type(result) is error:
				q.reject(result)
			else:
				q.fulfill(result)
		else:
			obj = {
				'src': 'add',
				'err': Constants.BAD_PARAMETER_EXPECTED_DOCUMENT_OR_ARRAY_OF_DOCUMENTS
			}
			q.reject(error(obj))

		return q
	def change(self, data, options={}):
		db = self.db
		q = promise()

		if options.has_key(Constants.replaceCriteria) and Utility.hasJSONSearchFields(options[Constants.replaceCriteria]):
			obj = {
				'src' : 'change',
				'err': Constants.BAD_PARAMETER_WRONG_SEARCH_CRITERIA
			}
			q.reject(error(obj))

		if Utility.isArrayOfObjects(data) or Utility.isEmptyArray(data):
			result = db.change(data, self.name, self.searchFields, options)
			if type(result) is error:
				q.reject(result)
			else :
				q.fulfill(result)
		else:
			obj = {
				'src' : 'change',
				'err': Constants.BAD_PARAMETER_EXPECTED_ARRAY_OF_OBJECTS
			}
			q.reject(error(obj))

		return q

	def clear(self):
		db = self.db
		q = promise()

		result = db.clear(self.name)

		if type(result) is error:
			q.reject(result)
		else:
			q.fulfill(result)
		return q

	def remove(self, query, options={}):
		db = self.db
		q = promise()

		result = db.remove(query, self.name, self.searchFields, options)

		if type(result) is error:
			q.reject(result)
		else:
			q.fulfill(result)

		return q

	def getAllDirtyDocuments(self):
		db = self.db
		q = promise()

		result = db.getAllDirtyDocuments(self.name)

		if type(result) is error:
			q.reject(result)
		else:
			q.fulfill(result)

		return q












		