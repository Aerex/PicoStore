import lib
import os
import pdb
from datetime import date
import ast
import pydash

sqlcipher = lib.sqlcipher
promise = lib.Promise
Utility = lib.Utility
Constants = lib.Constants
error = lib.Error
Builder = lib.QueryBuilder


class Local(object):

	_storeOpen = False
	_transitionState = False
	_username = ''
	_store = {}
	pwHash = ''	
	db = None

	class SqliteDB(object):

		def __init__(self,dbname, password):
			self.db = sqlcipher.connect(dbname + Constants.default_db_ext)
			if len(password) > 0:
				self.db.executescript(Constants.set_key + password + ';' + Constants.set_kdf_iter)



		def checkIfTableExists(self, tablename):
			row = self.db.execute(Constants.check_table.format(tablename)).fetchall()
			return True if len(row) > 0 else False
		def createTable(self, collection, searchFields):
			try :
				self.db.execute(Constants.create_table.format(collection, self._getFormatedColumns(searchFields), Constants.field_json, Constants.field_dirty, Constants.field_deleted, Constants.field_operation))
				row = self.db.execute(Constants.check_table.format(collection)).fetchall()
				return len(row)
			except TypeError as e:
				return -1

		def close(self):
			self.db.close()


		def _getFormatedColumns(self, fields):
			columns = '';
			if len(fields) < 1 :
				obj = {
					src : 'createTable',
					err : constants.INVALID_SEARCH_FIELD
				}
				raise error(obj)

			for field, fieldType in fields.items():
				if not Utility.isInvalidField(field) and Utility.isValidType(fieldType):
					columns+="'" + Utility.getSafeSearchField(field) +  "'" + ' ' + fieldType + ", "
			return columns

		def insert(self, tablename, columns, values):
			insert_stm = 'INSERT INTO ' + tablename + '('
			for x in range(len(columns)):
				insert_stm+=(columns[x] + ',')
			insert_stm =insert_stm[0:len(insert_stm)-1]
			insert_stm+=') VALUES ('
			for x in range(len(values)):
				insert_stm+='?,'
			insert_stm =insert_stm[0:len(insert_stm)-1]
			insert_stm+=')'
			try:
				self.db.execute(insert_stm, tuple(values))
				self.db.commit()
				return 1
			except sqlcipher.Error as e:
				return -1

		def find(self, tablename, stmt, values):
			find_stmt = 'SELECT * FROM ' + tablename + ' WHERE ' + stmt
			columns = []

			try:
				if len(values) == 0:
					row = self.db.execute(find_stmt)
				else:
					row =  self.db.execute(find_stmt, tuple(values))
				for x in range(len(row.description)):
					columns.append(row.description[x][0])
				return [columns, row.fetchall()]
			except sqlcipher.Error as e:
				return -1

		def dirty(self, tablename):
			dirty_find_stmt = 'SELECT * FROM ' + tablename + ' WHERE _dirty != ?'
			columns = []
			try:
				row = self.db.execute(dirty_find_stmt, tuple([0]))
				for x in range(len(row.description)):
					columns.append(row.description[x][0])
				return [columns, row.fetchall()]
			except sqlcipher.Error as e:
				return -1

		def count(self, tablename, stmt, values):
			count_stmt = 'SELECT COUNT(*) FROM ' + tablename + ' WHERE ' + stmt

			try:
				count = self.db.execute(count_stmt, tuple(values))
				return count.fetchall()[0][0]
			except sqlcipher.Error as e:
				return -1


		def delete(self, tablename, stmt, values):
			delete_stmt = 'DELETE FROM ' + tablename + ' WHERE ' + stmt
			columns = []

			try:
				self.db.execute(delete_stmt, tuple(values))
				self.db.commit()
				return 1
			except sqlcipher.Error as e:
				return -1

		def findAll(self, tablename):
			find_stmt = 'SELECT * FROM ' + tablename
			columns = []
			try:
				row = self.db.execute(find_stmt)
				for x in range(len(row.description)):
					columns.append(row.description[x][0])
				return [columns, row.fetchall()]
			except sqlcipher.Error as e:
				return -1

		def update(self, tablename, columns, values, id):
			update_stmt = 'UPDATE ' + tablename + ' SET '

			for x in range(len(columns)):
				update_stmt+=columns[x] + '=?,'
			update_stmt = update_stmt[0: len(update_stmt)-1]

			update_stmt+=' WHERE _id=' + str(id)
			try:
				self.db.execute(update_stmt, tuple(values))
				self.db.commit()
				return 1
			except sqlcipher.Error as e:
				return -1

		def clear(self, tablename):
			SQL_DELETE_ALL = 'DELETE from ' + tablename
			try :
				self.db.execute(SQL_DELETE_ALL)
				self.db.commit()
				return 1
			except sqlcipher.Error as e:
				return -1


	@property
	def storeOpen(self):
	    return self._storeOpen

	@property
	def store(self):
	    return self._store

	@property
	def transitionState(self):
	    return self._transitionState

	@store.setter
	def _addToStore(self, key, value):
		_store[key] = value

	@storeOpen.setter
	def setStore(self,flag):
		self._storeOpen = flag

	@transitionState.setter
	def setTransitionState(self, flag):
		self.transitionState = flag

	def _handlePassword(self, pw):
		q = promise()
		store = self._store
		self._storeOpen = True
		if not pw == None:
			if not self.pwHash == None:
				if pw == self.pwHash:
					q.fulfill(1)
				else:
					#user password does not match with stored password
					q.reject(Constants.INVALID_KEY_ON_PROVISION)
			else :
				#init without password and then init with password
				q.reject(Constants.INVALID_KEY_ON_PROVISION)
		else:
				if not self.pwHash == None:
					#user does not specify password but we have one saved
					q.reject(Constants.INVALID_KEY_ON_PROVISION)
				q.fulfill(1)
		return q


	def _checkOpenStore(self, password, username):
		q = promise()
		if not self._storeOpen:
			if self._username == '':
				self._username = username
				self._storeOpen = True
				q.fulfill(password)
			else:
				self._handlePassword(password)
		elif self._transitionState:
			q.reject(Constants.TRANSACTION_FAILURE_DURING_INIT)
		else:
			if username == self._username:
				q.fulfill(password)
			else:
				q.reject(Constants.USERNAME_MISMATCH_DETECTED)

		return q


	def _processProvisioning(self,options):
		q = promise()
		if Utility.isString(options[Constants.collectionPassword]) and len(options[Constants.collectionPassword]) > 0:
			self.pwHash = Utility.hashPassword(options[Constants.collectionPassword])

		self.db = self.SqliteDB(options[Constants.username], self.pwHash)
		self._checkOpenStore(self.pwHash, options[Constants.username]).then(lambda res: self._checkOpenStoreSuccess(res,q), lambda err: self._checkOpenStoreFailure(err))
		return q

	def _storeCollection(self,res, db, username, collection, searchFields, options, q):
		db = self.db
		self._storeOpen = True
		result = 0
		if not db.checkIfTableExists(collection):
			result = db.createTable(collection, searchFields)

		if Utility.isInt(result) and result > 0:
			q.fulfill(result)
		else:
			q.reject(result)

		return q


	def _getAllSearchFields(self, searchFields, additionalSearchFields):
		allSearchFields = {}
		if Utility.isObject(searchFields) and len(searchFields) > 0:
			for key in searchFields:
				allSearchFields[key] = searchFields[key]

		if Utility.isObject(additionalSearchFields) and len(additionalSearchFields) > 0:
			for key in additionalSearchFields:
				allSearchFields[key] = additionalSearchFields[key]

		return allSearchFields

	def _formatQuery(self, docs):
		formattedResult = []
		columns = docs[0]
		row = docs[1]
		for x in range(len(row)):
			formattedResult.append({})
			for y in range(len(columns)):
				if columns[y] == Constants.field_json:
					formattedResult[x][columns[y]] = ast.literal_eval(row[x][y])
				elif type(row[x][y]) is unicode:
					formattedResult[x][columns[y]] = str(row[x][y])
				else:
					formattedResult[x][columns[y]] = row[x][y]
		return {'docs' : formattedResult, 'columns': columns}




	def provision(self, collection, searchFields, options):
		pwHash = ''
		name = 'name'
		store = self._store
		q = promise()
		db = self.db
		username = options[Constants.username]
		allSearchFields = self._getAllSearchFields(searchFields, options[Constants.additionalSearchFields])
		(self._processProvisioning(options)
			.then(lambda res: self._storeCollection(res,db, username, collection, allSearchFields, options, q), lambda err: self._generalFailure(err, q)))

	def closeAll(self):
		if self._transitionState:
			obj = {
				'src' : 'closeAll',
				'err': Constants.TRANSACTION_FAILURE_DURING_CLOSE_ALL
			}
			return error(obj)
		else:
			self.db.close()
			return 0

	def destroy(self,username=''):
		if not self.db == None:
			self.db.close()
		try:
			if len(username) > 0:
				os.remove(username + Constants.default_db_ext)
			else :
				os.remove(Constants.default_username + Constants.default_db_ext)
			return 0
		except OSError as e:
			return 0

	def findAll(self, collectionName):
		db = self.db
		result = db.findAll(collectionName)
		formattedResult = []
		if type(result) is int:
			obj = {
				'src': 'find',
				'err': Constants.DATABASE_ERROR_WHILE_SEARCHING
			}
			return error(obj)
		else:
			result = self._formatQuery(result)
			formattedResult = result['docs']

		for x in range (len(formattedResult)):
			formattedResult[x] = pydash.objects.pick(formattedResult[x], [Constants.field_json, Constants.field_id])
 		return formattedResult

 	def count(self, collectionName, queries, options={}):
 		db  = self.db
 		find_stmt = ''
 		values = []
 		lastOrCounter = 1
 		if Utility.isObject(queries):
			queries = [queries]
		size = len (queries)
		for query in queries:
			for op in query:
				statementBuilder = Builder.createStatementBuilder(op, query[op])
				statementBuilder.build()
				if statementBuilder.isError():
					obj = {
						'src': 'find',
						'err': Constants.BAD_PARAMETER_EXPECTED_LIST
					}
					return error(obj)
				find_stmt+=statementBuilder.getFormattedStatement()
				values+=statementBuilder.getValueList()
			if lastOrCounter < size:
				find_stmt = find_stmt + 'OR'
				lastOrCounter+=1

		result = db.count(collectionName, find_stmt, values)

		if result == -1:
			obj = {
				'src': 'count',
				'err': Constants.ERROR_DURING_COUNT
			}

			return error(obj)
		else:
			return result

	def find(self, collectionName, queries, options={}):
		db = self.db
		find_stmt = ''
		values = []
		lastOrCounter = 1
		if Utility.isObject(queries):
			queries = [queries]
		size = len (queries)
		for query in queries:
			for op in query:
				statementBuilder = Builder.createStatementBuilder(op, query[op])
				statementBuilder.build()
				if statementBuilder.isError():
					obj = {
						'src': 'find',
						'err': Constants.BAD_PARAMETER_EXPECTED_LIST
					}
					return error(obj)
				find_stmt+=statementBuilder.getFormattedStatement()
				values+=statementBuilder.getValueList()
			if lastOrCounter < size:
				find_stmt = find_stmt + 'OR'
				lastOrCounter+=1
		result = db.find(collectionName, find_stmt, values)
		formattedResult = []

		if type(result) is int:
			obj = {
					'src': 'find',
					'err': Constants.DATABASE_ERROR_WHILE_SEARCHING
				}
			return error(obj)
		else:
			columns = result[0]
			row = result[1]
			for x in range(len(row)):
				formattedResult.append({})
				for y in range(len(columns)):
					if columns[y] == Constants.field_json:
						formattedResult[x][columns[y]] = ast.literal_eval(row[x][y])
					elif type(row[x][y]) is unicode:
						formattedResult[x][columns[y]] = str(row[x][y])
					else:
						formattedResult[x][columns[y]] = row[x][y]


			if options.has_key(Constants.filter) and not Utility.isArrayOfSearchFields(options[Constants.filter], columns):
				obj = {
					'src': 'find',
					'err': Constants.INVALID_FILTER_ARRAY
				}
				return error(obj)

			for x in range (len(formattedResult)):
					if options.has_key(Constants.filter) and len(options[Constants.filter]) > 0:
						formattedResult[x] = pydash.objects.pick(formattedResult[x], options[Constants.filter])
					else:
						formattedResult[x] = pydash.objects.pick(formattedResult[x], [Constants.field_json, Constants.field_id])
 
			
			return formattedResult





	def add(self, data, collectionName, collectionSearchFields,  options={}):
		numberOfAddedDocs = 0
		db = self.db
		columns = []
		values = []
		if self._transitionState:
			obj = {
				'src' : 'add',
				'err': Constants.TRANSACTION_IN_PROGRESS
			}

			return error(obj)
		if Utility.isObject(data):
			data = [data]

		index = 0
		if options.has_key(Constants.markDirty) and options[Constants.markDirty] == True:
			_dirty = date.today().isoformat()
		else:
			_dirty = 0

		searchFields = collectionSearchFields.keys()

		for x in range(len(data)):
			startingIndex = index;
			columns = []
			values = []

			if(options.has_key(Constants.additionalSearchFields)):
				additionalSearchFields =  options[Constants.additionalSearchFields].keys()
				for y in range(len(additionalSearchFields)):
					index+=y
					columns.insert(index, additionalSearchFields[y])
					values.insert(index, options[Constants.additionalSearchFields][additionalSearchFields[y]])


			for k in range(len(searchFields)):
				index+=k
				columns.insert(index, searchFields[k])
				values.insert(index, data[x][searchFields[k]])



			#set _json col/val
			startingIndex+=1
			columns.insert(startingIndex, Constants.field_json)
			values.insert(startingIndex, str(data[x]))

			#set _dirty col/value

			startingIndex+=1
			columns.insert(startingIndex, Constants.field_dirty)
			values.insert(startingIndex, _dirty)

			#set _operation col/value
			startingIndex+=1
			columns.insert(startingIndex, Constants.field_operation)
			op = Constants.operation_store if _dirty == 0 else Constants.operation_add
			values.insert(startingIndex, op)
			result = db.insert(collectionName, columns, values)

			if(result == -1):
				obj = {
					'src': 'add',
					'err': Constants.DATABASE_ERROR_WHILE_INSERTING
				}
				return error(obj)

			else:
				numberOfAddedDocs+=1

		return numberOfAddedDocs

	def replace(self, data, collectionName, collectionSearchFields, options={}):
		db = self.db
		update_stmt = ''
		numOfReplacedDocuments = 0
		values = []
		keys = []
		dirty = date.today().isoformat() if options.has_key(Constants.markDirty) and options[Constants.markDirty] else 0

		if self._transitionState:
			obj = {
				'src' : 'add',
				'err': Constants.TRANSACTION_IN_PROGRESS
			}

			return error(obj)

		if Utility.isObject(data):
			data = [data]

		for x in range(len(data)):
			if Utility.isObject(data[x]):
				keys = data[x][Constants.field_json].keys()
				values = data[x][Constants.field_json].values()				

				keys.append(Constants.field_json)
				values.append(str(data[x][Constants.field_json]))	

				keys.append(Constants.field_dirty)
				values.append(dirty)
				
				keys.append(Constants.field_operation)
				values.append('replace')

				result = db.update(collectionName, keys, values, data[x][Constants.field_id])
				
				if result == -1:
					obj = {
						'src': 'replace',
						'err': Constants.DATABASE_ERROR_WHILE_UPDATING
					}
				 	return error(obj)
				else :
				 	numOfReplacedDocuments+=1

		return numOfReplacedDocuments

	def change(self, dataArray, collectionName, collectionSearchFields, options={}):
		db = self.db
		allReplaceDocs = []
		allAddDocs = []
		retData = []
		changedDocs = 0

		if len(dataArray) == 0:
			return 0;
		else:
			for data in dataArray:
				if options.has_key(Constants.replaceCriteria) and len(options[Constants.replaceCriteria]) > 0:
					newData = pydash.objects.pick(data, options[Constants.replaceCriteria])
					retData.append(newData)
					query = [{'equal': [newData]}]
					foundData = self.find(collectionName, query)
					if len(foundData) == 1:
						allReplaceDocs.append({'_id': foundData[0][Constants.field_id], '_json': data})
					elif len(foundData) > 1:
						for x in range(len(foundData)):
							allReplaceDocs.append({'_id': foundData[x][Constants.field_id], '_json': data})
					else:
						allAddDocs.append(data)
				else :
					allAddDocs.append(data)
					
			for doc in allReplaceDocs:
				update = self.replace(doc,collectionName, collectionSearchFields, options)
				if Utility.isInt(update):
					changedDocs+=update
				else:
					return update

			if options.has_key(Constants.addNew) and options[Constants.addNew]:
				for doc in allAddDocs:
					update = self.add(doc, collectionName, collectionSearchFields, options)
					if Utility.isInt(update):
						changedDocs+=update
					else:
						return update

			return changedDocs

	def clear(self, collectionName):
		db = self.db

		result = db.clear(collectionName)

		if result == -1:
			obj = {
				'src': 'clear',
				'err': Constants.ERROR_CLEARING_COLLECTION 
			}
			return error(obj)
		else:
			return 0

	def getAllDirtyDocuments(self, collectionName):
		db = self.db

		result = db.dirty(collectionName)

		if result == -1:
			obj = {
				'src': 'getAllDirtyDocuments',
				'err': Constants.DATABASE_ERROR_WHILE_SEARCHING
			}

			return error(obj)
		else:
			return self._formatDocuments(result)


	def remove(self, queries, collectionName, collectionSearchFields, options={}):
		db = self.db
		remove_stmt = ''
		values = []
		lastOrCounter = 1
		if Utility.isObject(queries):
			queries = [queries]
		size = len (queries)
		for query in queries:
			for op in query:
				statementBuilder = Builder.createStatementBuilder(op, query[op])
				statementBuilder.build()
				if statementBuilder.isError():
					obj = {
						'src': 'remove',
						'err': Constants.BAD_PARAMETER_EXPECTED_LIST
					}
					return error(obj)
				remove_stmt+=statementBuilder.getFormattedStatement()
				values+=statementBuilder.getValueList()
			if lastOrCounter < size:
				remove_stmt = remove_stmt + 'OR'
				lastOrCounter+=1
		result = db.delete(collectionName, remove_stmt, values)
		return result




	def _formatDocuments(self, docs, options={}):
		formattedResult = []
		columns = docs[0]
		row = docs[1]
		for x in range(len(row)):
			formattedResult.append({})
			for y in range(len(columns)):
				if columns[y] == Constants.field_json:
					formattedResult[x][columns[y]] = ast.literal_eval(row[x][y])
				elif type(row[x][y]) is unicode:
					formattedResult[x][columns[y]] = str(row[x][y])
				else:
					formattedResult[x][columns[y]] = row[x][y]

		if options.has_key(Constants.filter) and not Utility.isArrayOfSearchFields(options[Constants.filter], columns):
			obj = {
				'src': 'find',
				'err': Constants.INVALID_FILTER_ARRAY
			}
			return error(obj)

		for x in range (len(formattedResult)):
			if options.has_key(Constants.filter) and len(options[Constants.filter]) > 0:
				formattedResult[x] = pydash.objects.pick(formattedResult[x], options[Constants.filter])
			else:
				formattedResult[x] = pydash.objects.pick(formattedResult[x], [Constants.field_json, Constants.field_id])
				
		return formattedResult

	def _checkOpenStoreSuccess(self, password, q):
		if  Utility.isString(password) and len(password) == 0:
			q.fulfill(Constants.SUCCESS)
		else:
			if not pwHash == password:
				q.reject(Constants.INVALID_KEY_ON_PROVISION)
			else:
				q.fulfill(Constants.SUCCESS)
		return q

	def _checkOpenStoreFailure(self, err):
		q = promise()
		q.reject(err)
		return q

	def _generalFailure(self, err, q):
		q.reject(err)
		return q


