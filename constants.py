class Constants(object):
	'''
	GENERAL CONSTANTS
	'''
	markDirty = 'markDirty'
	adapter = 'adapters'
	additionalSearchFields = 'additionalSearchFields'
	searchFields = 'searchFields'
	analytics = 'analytics'
	markDirty = 'markDirty'
	adapter = 'adapter'
	localKeyGen = 'localKeyGen'
	password = 'password'
	replaceCriteria = 'replaceCriteria'
	pbkdf2Iterations = 'pbkdf2Iterations'
	username = 'username'
	addNew = 'addNew'
	collectionPassword = 'collectionPassword'
	name = 'name'
	default_username = 'jsonstore'
	metadata = 'metadata'
	pwHash = 'pwHash'
	transactionState = 'transactionState'
	default_db_ext = '.db'
	limit = 'limit'
	filter = 'filter'
	offset = 'offset'
	sort = 'sort'
	
	#set_key = 'pragma key='
	set_key = 'pragma key=?;'
	set_kdf_iter = 'pragma kdf_iter=64000;'
	field_json = '_json'
	field_dirty = '_dirty'
	field_deleted = '_deleted'
	field_operation = '_operation'
	field_id = '_id'
	create_table = 'CREATE TABLE {0} (_id INTEGER PRIMARY KEY AUTOINCREMENT, {1} {2} TEXT, {3} REAL DEFAULT 0, {4} INTEGER DEFAULT 0, {5} TEXT);'
	check_table = 'pragma table_info({0})'

	operation_add = 'add'
	operation_store = 'store'

	'''
	operations
	'''
	lessThan = 'lessThan'
	lessOrEqualThan = 'lessOrEqualThan'
	greaterThan = 'greaterThan'
	greaterOrEqualThan = 'greaterOrEqualThan'
	equal = 'equal'
	notEqual = 'notEqual'
	inside = 'inside'
	notInside = 'notInside'
	between = 'between'
	notBetween = 'notBetween'
	rightLike = 'rightLike'
	notRightLike = 'notRightLike'
	leftLike = 'leftLike'
	notLeftLike = 'notLeftLike'
	like = 'like'
	notLike = 'notLike'


	'''SQL Search Statements'''
	likeSearch = '[{0}] = {1} OR [{0}] LIKE {1} OR [{0}] LIKE {1} OR [{0}] LIKE {1}'
	notLikeSearch = '[{0}] NOT LIKE {1}'
	leftRightLikeSearch = '[{0}] LIKE {1}'
	lessThanSearch = '[{0}] < {1}'
	lessThanOrEqualSearch = '[{0}] <= {1}'
	greaterThanSearch = '[{0}] > {1}'
	greaterThanOrEqualSearch = '[{0}] >= {1}'
	equalSearch = '[{0}] = {1}'
	notEqualSearch = '[{0}] != {1}'
	insideSearch = '[{0}] IN {1}'
	notInsideSearch = '[{0}] NOT IN {1}'
	betweenSearch = '[{0}] BETWEEN {1} AND {2}'

	CLOUDANT = 'cloudant'




	'''
	ERROR CONSTANTS
	'''
	SUCCESS = 0
	INVALID_KEY_ON_PROVISION = -3
	TRANSACTION_FAILURE_DURING_INIT = -44
	TRANSACTION_FAILURE_DURING_CLOSE_ALL = -45
	INVALID_ADD_INDEX_KEY = 21,
	BAD_PARAMETER_EXPECTED_DOCUMENT_OR_ARRAY_OF_DOCUMENTS = 10
	TRANSACTION_IN_PROGRESS = -41
	OFFSET_WITHOUT_LIMIT = -9
	INVALID_LIMIT_OR_OFFSET = -8
	USERNAME_MISMATCH_DETECTED = -6
	INVALID_SEARCH_FIELD = 22
	ERROR_DURING_DESTROY = 25
	ERROR_CLEARING_COLLECTION = 26
	INVALID_SORT_OBJECT = 28
	INVALID_USERNAME = -7
	INVALID_PASSWORD_EXPECTED_ALPHANUMERIC_STRING_WITH_LENGTH_GREATER_THAN_ZERO = 11
	BAD_PARAMETER_EXPECTED_ALPHANUMERIC_STRING = 4
	INVALID_SEARCH_FIELD_TYPES = -12
	BAD_PARAMETER_EXPECTED_SIMPLE_OBJECT = 6
	BAD_PARAMETER_EXPECTED_ARRAY_OF_OBJECTS = 30
	BAD_PARAMETER_WRONG_SEARCH_CRITERIA = 32
	DATABASE_ERROR_WHILE_INSERTING = 33
	DATABASE_ERROR_WHILE_SEARCHING = 34
	DATABASE_ERROR_WHILE_UPDATING = 35
	INVALID_QUERY_OPERATION = 36
	BAD_PARAMETER_EXPECTED_LIST = 37
	INVALID_FILTER_ARRAY = 29
	ERROR_DURING_COUNT = 38



