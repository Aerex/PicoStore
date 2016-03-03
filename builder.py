import lib
Constants = lib.Constants
Utility = lib.Utility

class QueryBuilder(object):

	@staticmethod
	def createStatementBuilder(operation, expression):
		if operation == Constants.like:
			return LikeQueryBuilder(expression)
		elif operation == Constants.notLike:
			return notLikeQueryBuilder(expression)
		elif operation == Constants.rightLike:
			return rightLikeQueryBuilder(expression)
		elif operation == Constants.notRightLike:
			return notRightLikeQueryBuilder(expression)
		elif operation == Constants.leftLike:
			return leftLikeQueryBuilder(expression)
		elif operation == Constants.notLeftLike:
			return notLeftLikeQueryBuilder(expression)
		elif operation == Constants.equal:
			return equalQueryBuilder(expression)
		elif operation == Constants.notEqual:
			return notEqualQueryBuilder(expression)
		elif operation == Constants.lessThan:
			return lessThanQueryBuilder(expression)
		elif operation == Constants.lessOrEqualThan:
			return lessOrEqualThanQueryBuilder(expression)
		elif operation == Constants.greaterThan:
			return greaterThanQueryBuilder(expression)
		elif operation == Constants.greaterOrEqualThan:
			return greaterOrEqualThanQueryBuilder(expression)
		elif operation == Constants.inside:
			return insideQueryBuilder(expression)
		elif operation == Constants.notInside:
			return notInsideQueryBuilder(expression)
		elif operation == Constants.between:
			return betweenQueryBuilder(expression)
		elif operation == Constants.notBetween:
			return notBetweenQueryBuilder(expression)
		else:
			return Constants.INVALID_QUERY_OPERATION

	def build(self):
		raise NotImplementedError

	def getFormattedStatement(self):
		return self.statement

	def isError(self):
		return self.error

	def getValueList(self):
		return self.queryValues

class LikeQueryBuilder(QueryBuilder):

	def __init__(self, queries):
		self.queries = queries
		self.statement = ''
		self.queryValues = []
		self.error = False

	def build(self):
		lastAndCounter = 1
		queries = self.queries
		if Utility.isObject(queries):
			queries = [queries]	
		size = len(queries)
		for query in queries:
			for key, value in query.iteritems():
				self.statement+= Constants.likeSearch.format(key,'?')
				self.statement+=' AND '
				value = str(value) if not Utility.isString(value) else value
				self.queryValues.append(value)
				self.queryValues.append('%' + value + '%')
				self.queryValues.append(value + '%')
				self.queryValues.append('%' + value)

		lastAND = self.statement.rfind('AND')
		self.statement = self.statement[0:lastAND]


class notLikeQueryBuilder(QueryBuilder):

	def __init__(self, queries):
		self.queries = queries
		self.statement = ''
		self.queryValues = []
		self.error = False

	def build(self):
		lastAndCounter = 1
		queries = self.queries
		if Utility.isObject(queries):
			queries = [queries]
		size = len(queries)
		for query in queries:
			for key, value in query.iteritems():
				self.statement+=Constants.notLikeSearch.format(key, '?')
				self.statement+=' AND '
				value = str(value) if not Utility.isString(value) else value
				self.queryValues.append('%' + value + '%')

		lastAND = self.statement.rfind('AND')
		self.statement = self.statement[0:lastAND]

class rightLikeQueryBuilder(QueryBuilder):
	def __init__(self, queries):
		self.queries = queries
		self.statement = ''
		self.queryValues = []
		self.error = False

	def build(self):
		lastAndCounter = 1
		queries = self.queries
		if Utility.isObject(queries):
			queries = [queries]
		size = len(queries)
		for query in queries:
			for key, value in query.iteritems():
				self.statement+=Constants.leftRightLikeSearch.format(key, '?')
				self.statement+=' AND '
				value = str(value) if not Utility.isString(value) else value
				self.queryValues.append(value + '%')

		lastAND = self.statement.rfind('AND')
		self.statement = self.statement[0:lastAND]

class notRightLikeQueryBuilder(QueryBuilder):
	def __init__(self, queries):
		self.queries = queries
		self.statement = ''
		self.queryValues = []
		self.error = False

	def build(self):
		queries = self.queries
		if Utility.isObject(queries):
			queries = [queries]
		size = len(queries)
		for query in queries:
			for key, value in query.iteritems():
				self.statement+=Constants.notLikeSearch.format(key, '?')
				self.statement+=' AND '
				value = str(value) if not Utility.isString(value) else value
				self.queryValues.append(value + '%')

		lastAND = self.statement.rfind('AND')
		self.statement = self.statement[0:lastAND]



class leftLikeQueryBuilder(QueryBuilder):
	def __init__(self, queries):
		self.queries = queries
		self.statement = ''
		self.queryValues = []
		self.error = False

	def build(self):
		lastAndCounter = 1
		queries = self.queries
		if Utility.isObject(queries):
			queries = [queries]
		size = len(queries)
		for query in queries:
			for key, value in query.iteritems():
				self.statement+=Constants.leftRightLikeSearch.format(key, '?')
				self.statement+=' AND '
				value = str(value) if not Utility.isString(value) else value
				self.queryValues.append('%' + value)

		lastAND = self.statement.rfind('AND')
		self.statement = self.statement[0:lastAND]

class notLeftLikeQueryBuilder(QueryBuilder):
	def __init__(self, queries):
		self.queries = queries
		self.statement = ''
		self.queryValues = []
		self.error = False

	def build(self):
		lastAndCounter = 1
		queries = self.queries
		if Utility.isObject(queries):
			queries = [queries]
		size = len(queries)
		for query in queries:
			for key, value in query.iteritems():
				self.statement+=Constants.notLikeSearch.format(key, '?')
				self.statement+=' AND '
				value = str(value) if not Utility.isString(value) else value
				self.queryValues.append('%' + value)

		lastAND = self.statement.rfind('AND')
		self.statement = self.statement[0:lastAND]

class lessThanQueryBuilder(QueryBuilder):
	def __init__(self, queries):
		self.queries = queries
		self.statement = ''
		self.queryValues = []
		self.error = False

	def build(self):
		lastAndCounter = 1
		queries = self.queries
		if Utility.isObject(queries):
			queries = [queries]
		size = len(queries)
		for query in queries:
			for key, value in query.iteritems():
				self.statement+=Constants.lessThanSearch.format(key, '?')
				self.statement+=' AND '
				value = str(value) if not Utility.isString(value) else value
				self.queryValues.append(value)

		lastAND = self.statement.rfind('AND')
		self.statement = self.statement[0:lastAND]


class lessOrEqualThanQueryBuilder(QueryBuilder):
	def __init__(self, queries):
		self.queries = queries
		self.statement = ''
		self.queryValues = []
		self.error = False

	def build(self):
		lastAndCounter = 1
		queries = self.queries
		if Utility.isObject(queries):
			queries = [queries]
		size = len(queries)
		for query in queries:
			for key, value in query.iteritems():
				self.statement+=Constants.lessThanOrEqualSearch.format(key, '?')
				self.statement+=' AND '
				value = str(value) if not Utility.isString(value) else value
				self.queryValues.append(value)

		lastAND = self.statement.rfind('AND')
		self.statement = self.statement[0:lastAND]


class greaterThanQueryBuilder(QueryBuilder):
	def __init__(self, queries):
		self.queries = queries
		self.statement = ''
		self.queryValues = []
		self.error = False

	def build(self):
		lastAndCounter = 1
		queries = self.queries
		if Utility.isObject(queries):
			queries = [queries]
		size = len(queries)
		for query in queries:
			for key, value in query.iteritems():
				self.statement+=Constants.greaterThanSearch.format(key, '?')
				self.statement+=' AND '
				value = str(value) if not Utility.isString(value) else value
				self.queryValues.append(value)

		lastAND = self.statement.rfind('AND')
		self.statement = self.statement[0:lastAND]

class greaterOrEqualThanQueryBuilder(QueryBuilder):
	def __init__(self, queries):
		self.queries = queries
		self.statement = ''
		self.queryValues = []
		self.error = False

	def build(self):
		lastAndCounter = 1
		queries = self.queries
		if Utility.isObject(queries):
			queries = [queries]
		size = len(queries)
		for query in queries:
			for key, value in query.iteritems():
				self.statement+=Constants.greaterThanOrEqualSearch.format(key, '?')
				self.statement+=' AND '
				value = str(value) if not Utility.isString(value) else value
				self.queryValues.append(value)

		lastAND = self.statement.rfind('AND')
		self.statement = self.statement[0:lastAND]

class equalQueryBuilder(QueryBuilder):
	def __init__(self, queries):
		self.queries = queries
		self.statement = ''
		self.queryValues = []
		self.error = False

	def build(self):
		lastAndCounter = 1
		queries = self.queries
		if Utility.isObject(queries):
			queries = [queries]
		size = len(queries)
		for query in queries:
			for key, value in query.iteritems():
				self.statement+=Constants.equalSearch.format(key, '?')
				self.statement+=' AND '
				value = str(value) if not Utility.isString(value) else value
				self.queryValues.append(value)

		lastAND = self.statement.rfind('AND')
		self.statement = self.statement[0:lastAND]

class notEqualQueryBuilder(QueryBuilder):
	def __init__(self, queries):
		self.queries = queries
		self.statement = ''
		self.queryValues = []
		self.error = False

	def build(self):
		lastAndCounter = 1
		queries = self.queries
		if Utility.isObject(queries):
			queries = [queries]
		size = len(queries)
		for query in queries:
			for key, value in query.iteritems():
				self.statement+=Constants.notEqualSearch.format(key, '?')
				self.statement+=' AND '
				value = str(value) if not Utility.isString(value) else value
				self.queryValues.append(value)

		lastAND = self.statement.rfind('AND')
		self.statement = self.statement[0:lastAND]


class insideQueryBuilder(QueryBuilder):
	def __init__(self, queries):
		self.queries = queries
		self.statement = ''
		self.queryValues = []
		self.error = False

	def build(self):
		lastAndCounter = 1
		queries = self.queries
		if Utility.isObject(queries):
			queries = [queries]
		size = len(queries)
		for query in queries:
			for key, value in query.iteritems():
				if not type(value) is list:
					self.error = True
				else:
					value = str(value)
					value = value.replace('[', '(')
					value = value.replace(']', ')')
					self.statement+=Constants.insideSearch.format(key, value)
					self.statement+=' AND '

		lastAND = self.statement.rfind('AND')
		self.statement = self.statement[0:lastAND]

class notInsideQueryBuilder(QueryBuilder):
	def __init__(self, queries):
		self.queries = queries
		self.statement = ''
		self.queryValues = []
		self.error = False

	def build(self):
		lastAndCounter = 1
		queries = self.queries
		if Utility.isObject(queries):
			queries = [queries]
		size = len(queries)
		for query in queries:
			for key, value in query.iteritems():
				if not type(value) is list:
					self.error = True
				else:
					value = str(value)
					value = value.replace('[', '(')
					value = value.replace(']', ')')
					self.statement+=Constants.notInsideSearch.format(key, value)
					self.statement+=' AND '

		lastAND = self.statement.rfind('AND')
		self.statement = self.statement[0:lastAND]


class betweenQueryBuilder(QueryBuilder):
	def __init__(self, queries):
		self.queries = queries
		self.statement = ''
		self.queryValues = []
		self.error = False

	def build(self):
		lastAndCounter = 1
		queries = self.queries
		if Utility.isObject(queries):
			queries = [queries]
		size = len(queries)
		for query in queries:
			for key, value in query.iteritems():
				if not type(value) is list and not len(value) == 2:
					self.error = True
				else:
					self.statement+=Constants.betweenSearch.format(key, value[0], value[1])
					self.statement+=' AND '

		lastAND = self.statement.rfind('AND')
		self.statement = self.statement[0:lastAND]





































