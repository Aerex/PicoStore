from nose.tools import *    
import pdb
import sys
sys.path.insert(0, "../")
from picostore import PicoStore


#Find

# Here's our "unit tests".

class Counter:
    """
    A helper class with some side effects
    we can test. Need to compensate for silent assertion 
    """

    def __init__(self):
        self.count = 0

    def tick(self):
        self.count += 1

    def messages(self,obj):
        self.message.append(obj)

    def value(self):
        return self.count

    def getMessage(self,index):
        return self.message[0]



def testLikeSimpleFind():
    PicoStoreInstance = PicoStore()
    successCounter = Counter()
    failCounter = Counter()
    collection =  {
        'customers' : {
                'searchFields' : {'name' : 'string', 'age': 'integer'}
        }
    }

    data = [{'name': 'shin', 'age': 1}, {'name': 'shu', 'age': 2}, {'name': 'masao', 'age': 3}]
    query = [
        {'like': [{'name': 'sh'}]}

    ]

    def fail(err):
        failCounter.tick()
        print 'Failed with ' + err

    def successFind(res):
        assert_equals(len(res), 2)
        successCounter.tick()
        assert_equals(res[0]['_json']['name'], 'shin')
        successCounter.tick()
        assert_equals(res[1]['_json']['name'], 'shu')
        successCounter.tick()

    def successAdd(res):
        assert_equals(res, 3)
        successCounter.tick()
        '''
            select *
                from 'customers'
                where 
                    [name] = 'sh' OR [name] LIKE '%-@-na-@-%' OR [name] LIKE '%-@-na' OR [name] LIKE 'na-@-%'
        '''
        PicoStoreInstance.get('customers').find(query).then(lambda res: successFind(res), lambda err: fail(err))

    def successInit(res):
        assert_equals(res['customers'].name, 'customers')
        successCounter.tick()
        PicoStoreInstance.get('customers').add(data).then(lambda res: successAdd(res), lambda err: fail(err))


    def successDestroy(res):
        assert_equals(res, 0)
        successCounter.tick()
        PicoStoreInstance.init(collection).then(lambda res: successInit(res), lambda err: fail(err))


    PicoStoreInstance.destroy().then(lambda res: successDestroy(res), lambda err: fail(err))
    assert_equals(6, successCounter.value())
    assert_equals(0, failCounter.value())

def testLikeSimpleFindUsingMultTypesForSearchFields():
    PicoStoreInstance = PicoStore()
    successCounter = Counter()
    failCounter = Counter()
    collection =  {
        'customers' : {
                'searchFields' : {'name' : 'string', 'gpa': 'number', 'ssn': 'integer', 'active': 'boolean'}
        }
    }

    data = [
        {'name': 'shin', 'gpa': 1.0, 'ssn': 123, 'active': True},
        {'name': 'shu', 'gpa': 2.2, 'ssn': 345, 'active': False},
        {'name': 'masao', 'gpa': 2.4, 'ssn': 567, 'active': True},
        {'name': 'saito', 'gpa': 3.6, 'ssn': 789, 'active': False},
        {'name': 'aiko', 'gpa': 4.8, 'ssn': 890, 'active': True}
        ]
    query = [
        {'like': [{'gpa': '.2'}]}

    ]

    def fail(err):
        failCounter.tick()
        print 'Failed with ' + err


    def successFind(res):
        assert_equals(len(res), 1)
        successCounter.tick()
        assert_equals(res[1]['json']['name'], 'shu')

    def successAdd(res):
        assert_equals(res, 5)
        successCounter.tick()
        '''
            select *
                from 'customers'
                where
                    [gpa] = '.2' OR [gpa] LIKE '%-@-.2-@-%' OR [gpa] LIKE '%-@-.2' OR [gpa] LIKE '.2-@-%'
        '''
        PicoStoreInstance.get('customers').find(query).then(lambda res: successFind(res), lambda err: fail(err))

    def successInit(res):
        assert_equals(res['customers'].name, 'customers')
        successCounter.tick()
        PicoStoreInstance.get('customers').add(data).then(lambda res: successAdd(res), lambda err: fail(err))


    def successDestroy(res):
        assert_equals(res, 0)
        successCounter.tick()
        PicoStoreInstance.init(collection).then(lambda res: successInit(res), lambda err: fail(err))


    PicoStoreInstance.destroy().then(lambda res: successDestroy(res), lambda err: fail(err))
    assert_equals(4, successCounter.value())
    assert_equals(0, failCounter.value())

def testLikeSimpleTestWithAddtionalSearchFieldsFind():
    PicoStoreInstance = PicoStore()
    successCounter = Counter()
    failCounter = Counter()
    collection =  {
        'customers' : {
                'searchFields' : {'name' : 'string', 'age': 'integer'},
                'additionalSearchFields': {'lol': 'string'}
        }
    }

    addOptions = {
        'additionalSearchFields': {
            'lol': '1337'
        }
    }

    data = [{'name': 'masao', 'age': 1}, {'name': 'junko', 'age': 2}, {'name': 'haruka', 'age': 3}, {'name': 'saito', 'age': 4}]

    query = [
        {'like': [{'lol': '1337'}]}
    ]

    def fail(err):
        failCounter.tick()
        print 'Failed with ' + err

    def successFind(res):
        assert_equals(len(res), 4)
        successCounter.tick()
        assert_equals(res[0]['_json']['name'], 'masao')
        successCounter.tick()
        assert_equals(res[1]['_json']['name'], 'junko')
        successCounter.tick()
        assert_equals(res[2]['_json']['name'], 'haruka')
        successCounter.tick()
        assert_equals(res[3]['_json']['name'], 'saito')

    def successAdd(res):
        assert_equals(res, 4)
        successCounter.tick()
        '''
           select *
            from 'customers'
            where
              [name] = 'x' OR [name] LIKE '%-@-x-@-%' OR [name] LIKE '%-@-x' OR [name] LIKE 'x-@-%'
        '''
        PicoStoreInstance.get('customers').find(query).then(lambda res: successFind(res), lambda err: fail(err))

    def successInit(res):
        assert_equals(res['customers'].name, 'customers')
        successCounter.tick()
        PicoStoreInstance.get('customers').add(data, addOptions).then(lambda res: successAdd(res), lambda err: fail(err))


    def successDestroy(res):
        assert_equals(res, 0)
        successCounter.tick()
        PicoStoreInstance.init(collection).then(lambda res: successInit(res), lambda err: fail(err))

    PicoStoreInstance.destroy().then(lambda res: successDestroy(res), lambda err: fail(err))
    assert_equals(7, successCounter.value())
    assert_equals(0, failCounter.value())


def testLikeNoResultsFind():
    PicoStoreInstance = PicoStore()
    successCounter = Counter()
    failCounter = Counter()
    collection =  {
        'customers' : {
                'searchFields' : {'name' : 'string', 'age': 'integer'}
        }
    }

    data = [{'name': 'masao', 'age': 1}, {'name': 'junko', 'age': 2}, {'name': 'haruka', 'age': 3}, {'name': 'saito', 'age': 4}]

    query = [
        {'like': [{'name': 'x'}]}

    ]

    def fail(err):
        failCounter.tick()
        print 'Failed with ' + err

    def successFind(res):
        assert_equals(len(res), 0)
        successCounter.tick()

    def successAdd(res):
        assert_equals(res, 4)
        successCounter.tick()
        '''
            select *
            from 'customers'
            where
              [name] = 'x' OR [name] LIKE '%-@-x-@-%' OR [name] LIKE '%-@-x' OR [name] LIKE 'x-@-%'
        '''
        PicoStoreInstance.get('customers').find(query).then(lambda res: successFind(res), lambda err: fail(err))

    def successInit(res):
        assert_equals(res['customers'].name, 'customers')
        successCounter.tick()
        PicoStoreInstance.get('customers').add(data).then(lambda res: successAdd(res), lambda err: fail(err))


    def successDestroy(res):
        assert_equals(res, 0)
        successCounter.tick()
        PicoStoreInstance.init(collection).then(lambda res: successInit(res), lambda err: fail(err))


    PicoStoreInstance.destroy().then(lambda res: successDestroy(res), lambda err: fail(err))
    assert_equals(4, successCounter.value())
    assert_equals(0, failCounter.value())

def testLikeAllResults():
    PicoStoreInstance = PicoStore()
    successCounter = Counter()
    failCounter = Counter()
    collection =  {
        'customers' : {
                'searchFields' : {'name' : 'string', 'age': 'integer'}
        }
    }

    data = [{'name': 'Hayata', 'age': 1}, {'name': 'HAyata', 'age': 2}, {'name': 'HAYata', 'age': 3}, {'name': 'HAYAta', 'age': 4}]

    query = [
        {'like': [  {'name': 'hayata'}]}

    ]

    def fail(err):
        failCounter.tick()
        print 'Failed with ' + err

    def successFind(res):
        assert_equals(len(res), 4)
        successCounter.tick()
        assert_equals(res[0]['_json']['name'], 'Hayata')
        successCounter.tick()
        assert_equals(res[1]['_json']['name'], 'HAyata')
        successCounter.tick()
        assert_equals(res[2]['_json']['name'], 'HAYata')
        successCounter.tick()
        assert_equals(res[3]['_json']['name'], 'HAYAta')

    def successAdd(res):
        assert_equals(res, 4)
        successCounter.tick()
        '''
            select *
            from 'customers'
            where
              [lol] = 'hey' OR [name] LIKE '%-@-hey-@-%' OR [name] LIKE '%-@-hey' OR [name] LIKE 'hey-@-%'
        '''
        PicoStoreInstance.get('customers').find(query).then(lambda res: successFind(res), lambda err: fail(err))

    def successInit(res):
        assert_equals(res['customers'].name, 'customers')
        successCounter.tick()
        PicoStoreInstance.get('customers').add(data).then(lambda res: successAdd(res), lambda err: fail(err))


    def successDestroy(res):
        assert_equals(res, 0)
        successCounter.tick()
        PicoStoreInstance.init(collection).then(lambda res: successInit(res), lambda err: fail(err))


    PicoStoreInstance.destroy().then(lambda res: successDestroy(res), lambda err: fail(err))
    assert_equals(7, successCounter.value())
    assert_equals(0, failCounter.value())

def testNotLikeSimpleFind():
    PicoStoreInstance = PicoStore()
    successCounter = Counter()
    failCounter = Counter()
    collection =  {
        'customers' : {
                'searchFields' : {'name' : 'string', 'age': 'integer'}
        }
    }

    data = [{'name': 'masao', 'age': 1}, {'name': 'junko', 'age': 2}, {'name': 'haruka', 'age': 3}, {'name': 'saito', 'age': 4}]
    query = [
        {'notLike': [{'name': 'ha'}]}

    ]

    def fail(err):
        failCounter.tick()
        print 'Failed with ' + err

    def successFind(res):
        assert_equals(len(res), 3)
        successCounter.tick()
        assert_equals(res[0]['_json']['name'], 'masao')
        successCounter.tick()
        assert_equals(res[1]['_json']['name'], 'junko')
        successCounter.tick()
        assert_equals(res[2]['_json']['name'], 'saito')

    def successAdd(res):
        assert_equals(res, 4)
        successCounter.tick()
        '''
            select *
                from 'customers'
                where 
                    [name] NOT LIKE '%-@-na-@-%'
        '''
        PicoStoreInstance.get('customers').find(query).then(lambda res: successFind(res), lambda err: fail(err))

    def successInit(res):
        assert_equals(res['customers'].name, 'customers')
        successCounter.tick()
        PicoStoreInstance.get('customers').add(data).then(lambda res: successAdd(res), lambda err: fail(err))


    def successDestroy(res):
        assert_equals(res, 0)
        successCounter.tick()
        PicoStoreInstance.init(collection).then(lambda res: successInit(res), lambda err: fail(err))


    PicoStoreInstance.destroy().then(lambda res: successDestroy(res), lambda err: fail(err))
    assert_equals(6, successCounter.value())
    assert_equals(0, failCounter.value())


def testLikeMultipleFind():
    PicoStoreInstance = PicoStore()
    successCounter = Counter()
    failCounter = Counter()
    collection =  {
        'customers' : {
                'searchFields' : {'name' : 'string', 'age': 'integer', 'ssn': 'integer'}
        }
    }

    data = [{'name': 'hayata', 'age': 1, 'ssn': 123}, {'name': 'takaki', 'age': 2, 'ssn': 345}, {'name': 'junko', 'age': 3, 'ssn': 567}, {'name': 'santaru', 'age': 4, 'ssn': 789}]

    query = [
        {'like': [  {'name': 'yat'}, {'ssn': '23'}]}

    ]

    def fail(err):
        failCounter.tick()
        print 'Failed with ' + err

    def successFind(res):
        assert_equals(len(res), 1)
        successCounter.tick()
        assert_equals(res[0]['_json']['name'], 'hayata')
        successCounter.tick()
        assert_equals(res[0]['_json']['age'], 1)
        successCounter.tick()
        assert_equals(res[0]['_json']['ssn'], 123)

    def successAdd(res):
        assert_equals(res, 4)
        successCounter.tick()
        '''
            select *
            from 'customers'
            where
                [name] = 'yat' OR [name] LIKE '%-@-yat-@-%' OR [name] LIKE '%-@-yat' OR [name] LIKE 'yat-@-%'
            AND
                [ssn] = '23' OR [ssn] LIKE '%-@-23-@-%' OR [ssn] LIKE '%-@-23' OR [ssn] LIKE '23-@-%'

        '''
        PicoStoreInstance.get('customers').find(query).then(lambda res: successFind(res), lambda err: fail(err))

    def successInit(res):
        assert_equals(res['customers'].name, 'customers')
        successCounter.tick()
        PicoStoreInstance.get('customers').add(data).then(lambda res: successAdd(res), lambda err: fail(err))


    def successDestroy(res):
        assert_equals(res, 0)
        successCounter.tick()
        PicoStoreInstance.init(collection).then(lambda res: successInit(res), lambda err: fail(err))


    PicoStoreInstance.destroy().then(lambda res: successDestroy(res), lambda err: fail(err))
    assert_equals(6, successCounter.value())
    assert_equals(0, failCounter.value())

def testLikeMultipleSingleObjectFind():
    PicoStoreInstance = PicoStore()
    successCounter = Counter()
    failCounter = Counter()
    collection =  {
        'customers' : {
                'searchFields' : {'name' : 'string', 'age': 'integer', 'ssn': 'integer'}
        }
    }

    data = [{'name': 'hayata', 'age': 1, 'ssn': 123}, {'name': 'takaki', 'age': 2, 'ssn': 345}, {'name': 'junko', 'age': 3, 'ssn': 567}, {'name': 'santaru', 'age': 4, 'ssn': 789}]

    query = [
        {'like': [  {'name': 'yat', 'ssn': '23'}]}

    ]

    def fail(err):
        failCounter.tick()
        print 'Failed with ' + err

    def successFind(res):
        assert_equals(len(res), 1)
        successCounter.tick()
        assert_equals(res[0]['_json']['name'], 'hayata')
        successCounter.tick()
        assert_equals(res[0]['_json']['age'], 1)
        successCounter.tick()
        assert_equals(res[0]['_json']['ssn'], 123)

    def successAdd(res):
        assert_equals(res, 4)
        successCounter.tick()
        '''
            select *
            from 'customers'
            where
                [name] = 'yat' OR [name] LIKE '%-@-yat-@-%' OR [name] LIKE '%-@-yat' OR [name] LIKE 'yat-@-%'
            AND
                [ssn] = '23' OR [ssn] LIKE '%-@-23-@-%' OR [ssn] LIKE '%-@-23' OR [ssn] LIKE '23-@-%'

        '''
        PicoStoreInstance.get('customers').find(query).then(lambda res: successFind(res), lambda err: fail(err))

    def successInit(res):
        assert_equals(res['customers'].name, 'customers')
        successCounter.tick()
        PicoStoreInstance.get('customers').add(data).then(lambda res: successAdd(res), lambda err: fail(err))


    def successDestroy(res):
        assert_equals(res, 0)
        successCounter.tick()
        PicoStoreInstance.init(collection).then(lambda res: successInit(res), lambda err: fail(err))


    PicoStoreInstance.destroy().then(lambda res: successDestroy(res), lambda err: fail(err))
    assert_equals(6, successCounter.value())
    assert_equals(0, failCounter.value())

def testRightLikeTest():
    PicoStoreInstance = PicoStore()
    successCounter = Counter()
    failCounter = Counter()
    collection =  {
        'customers' : {
                'searchFields' : {'name' : 'string', 'age': 'integer'}
        }
    }

    data = [{'name': 'hayatashin', 'age': 1}, {'name': 'hayata', 'age': 2}, {'name': 'Hayata', 'age': 3}, {'name': 'hayataShin', 'age': 4}, {'name': 'shin', 'age': 5}]

    query = [
        {'rightLike': [  {'name': 'hayata'}]}

    ]

    def fail(err):
        failCounter.tick()
        print 'Failed with ' + err

    def successFind(res):
        assert_equals(len(res), 4)
        successCounter.tick()
        assert_equals(res[0]['_json']['name'], 'hayatashin')
        successCounter.tick()
        assert_equals(res[1]['_json']['name'], 'hayata')
        successCounter.tick()
        assert_equals(res[2]['_json']['name'], 'Hayata')
        successCounter.tick()
        assert_equals(res[3]['_json']['name'], 'hayataShin')

    def successAdd(res):
        assert_equals(res, 5)
        successCounter.tick()
        '''
            select *
            from 'customers'
            where
                [name] LIKE 'hayata-@-%'
        '''
        PicoStoreInstance.get('customers').find(query).then(lambda res: successFind(res), lambda err: fail(err))

    def successInit(res):
        assert_equals(res['customers'].name, 'customers')
        successCounter.tick()
        PicoStoreInstance.get('customers').add(data).then(lambda res: successAdd(res), lambda err: fail(err))


    def successDestroy(res):
        assert_equals(res, 0)
        successCounter.tick()
        PicoStoreInstance.init(collection).then(lambda res: successInit(res), lambda err: fail(err))


    PicoStoreInstance.destroy().then(lambda res: successDestroy(res), lambda err: fail(err))
    assert_equals(7, successCounter.value())
    assert_equals(0, failCounter.value())

def testRightLikeMultipleTypesSearchFields():
    PicoStoreInstance = PicoStore()
    successCounter = Counter()
    failCounter = Counter()
    collection =  {
        'customers' : {
                'searchFields' : {'name' : 'string', 'gpa': 'integer', 'ssn': 'integer', 'active': 'boolean'}
        }
    }

    data = [
        {'name': 'hayatashin', 'age': 1, 'gpa': 1.0, 'ssn': 123, 'active': True},
        {'name': 'hayata', 'age': 2, 'gpa': 2.2, 'ssn': 345, 'active': False }, {
        'name': 'Hayata', 'age': 3,  'gpa': 2.4, 'ssn': 567, 'active': False},
        {'name': 'hayataShin', 'gpa': 3.6, 'active': False, 'age': 4, 'ssn': 789}]

    query = [
        {'rightLike': [  {'gpa': '3.'}]}

    ]

    def fail(err):
        failCounter.tick()
        print 'Failed with ' + err

    def successFind(res):
        assert_equals(len(res), 1)
        successCounter.tick()
        assert_equals(res[0]['_json']['name'], 'hayataShin')
        successCounter.tick()

    def successAdd(res):
        assert_equals(res, 4)
        successCounter.tick()
        '''
            select *
            from 'customers'
            where
                [name] LIKE '3.-@-%'
        '''
        PicoStoreInstance.get('customers').find(query).then(lambda res: successFind(res), lambda err: fail(err))

    def successInit(res):
        assert_equals(res['customers'].name, 'customers')
        successCounter.tick()
        PicoStoreInstance.get('customers').add(data).then(lambda res: successAdd(res), lambda err: fail(err))


    def successDestroy(res):
        assert_equals(res, 0)
        successCounter.tick()
        PicoStoreInstance.init(collection).then(lambda res: successInit(res), lambda err: fail(err))


    PicoStoreInstance.destroy().then(lambda res: successDestroy(res), lambda err: fail(err))
    assert_equals(5, successCounter.value())
    assert_equals(0, failCounter.value())

def testRightLikeWithAdditionalSearchFields():
    PicoStoreInstance = PicoStore()
    successCounter = Counter()
    failCounter = Counter()
    collection =  {
        'customers' : {
                'searchFields' : {'name' : 'string', 'age': 'integer'},
                'additionalSearchFields': {'lol': 'string'}
        }
    }

    addOptions = {
        'additionalSearchFields': {
            'lol': '1337'
        }
    }

    data = [{'name': 'masao', 'age': 1}, {'name': 'junko', 'age': 2}, {'name': 'haruka', 'age': 3}, {'name': 'saito', 'age': 4}]

    query = [
        {'like': [{'lol': '13'}]}
    ]

    def fail(err):
        failCounter.tick()
        print 'Failed with ' + err

    def successFind(res):
        assert_equals(len(res), 2)
        successCounter.tick()
        assert_equals(res[0]['_json']['name'], 'haruka')
        successCounter.tick()
        assert_equals(res[1]['_json']['name'], 'saito')

    def successAddTwo(res):
        assert_equals(res, 2)
        successCounter.tick()
        '''
           select *
            from 'customers'
            where
              [lol] LIKE '13-@-%'
        '''
        PicoStoreInstance.get('customers').find(query).then(lambda res: successFind(res), lambda err: fail(err))

    def successAddOne(res):
        assert_equals(res, 2)
        successCounter.tick()
        PicoStoreInstance.get('customers').add([data[0],data[1]]).then(lambda res: successAddTwo(res), lambda err: fail(err))

    def successInit(res):
        assert_equals(res['customers'].name, 'customers')
        successCounter.tick()
        PicoStoreInstance.get('customers').add([data[2],data[3]], addOptions).then(lambda res: successAddOne(res), lambda err: fail(err))


    def successDestroy(res):
        assert_equals(res, 0)
        successCounter.tick()
        PicoStoreInstance.init(collection).then(lambda res: successInit(res), lambda err: fail(err))

    PicoStoreInstance.destroy().then(lambda res: successDestroy(res), lambda err: fail(err))
    assert_equals(6, successCounter.value())
    assert_equals(0, failCounter.value())

def testNotRightLike():
    PicoStoreInstance = PicoStore()
    successCounter = Counter()
    failCounter = Counter()
    collection =  {
        'customers' : {
                'searchFields' : {'name' : 'string', 'age': 'integer'}
        }
    }

    data = [{'name': 'masao', 'age': 1}, {'name': 'junko', 'age': 2}, {'name': 'haruka', 'age': 3}, {'name': 'saito', 'age': 4}]
    query = [
        {'notRightLike': [{'name': 'ha'}]}

    ]

    def fail(err):
        failCounter.tick()
        print 'Failed with ' + err

    def successFind(res):
        assert_equals(len(res), 3)
        successCounter.tick()
        assert_equals(res[0]['_json']['name'], 'masao')
        successCounter.tick()
        assert_equals(res[1]['_json']['name'], 'junko')
        successCounter.tick()
        assert_equals(res[2]['_json']['name'], 'saito')

    def successAdd(res):
        assert_equals(res, 4)
        successCounter.tick()
        '''
            select *
                from 'customers'
                where 
                    [name] NOT LIKE 'ha-@-%'
        '''
        PicoStoreInstance.get('customers').find(query).then(lambda res: successFind(res), lambda err: fail(err))

    def successInit(res):
        assert_equals(res['customers'].name, 'customers')
        successCounter.tick()
        PicoStoreInstance.get('customers').add(data).then(lambda res: successAdd(res), lambda err: fail(err))


    def successDestroy(res):
        assert_equals(res, 0)
        successCounter.tick()
        PicoStoreInstance.init(collection).then(lambda res: successInit(res), lambda err: fail(err))


    PicoStoreInstance.destroy().then(lambda res: successDestroy(res), lambda err: fail(err))
    assert_equals(6, successCounter.value())
    assert_equals(0, failCounter.value())

def testRightLikeNoResults():
    PicoStoreInstance = PicoStore()
    successCounter = Counter()
    failCounter = Counter()
    collection =  {
        'customers' : {
                'searchFields' : {'name' : 'string', 'age': 'integer'}
        }
    }

    data = [{'name': 'eTakakimasao', 'age': 1}, {'name': 'dmasao', 'age': 2}, {'name': 'choshikata', 'age': 3}, {'name': 'dmasao', 'age': 4}]
    query = [
        {'rightLike': [{'name': 'masao'}]}

    ]

    def fail(err):
        failCounter.tick()
        print 'Failed with ' + err

    def successFind(res):
        assert_equals(len(res), 0)
        successCounter.tick()
     
    def successAdd(res):
        assert_equals(res, 4)
        successCounter.tick()
        '''
            select *
                from 'customers'
                where 
                    [name] LIKE 'masao-@-%'
        '''
        PicoStoreInstance.get('customers').find(query).then(lambda res: successFind(res), lambda err: fail(err))

    def successInit(res):
        assert_equals(res['customers'].name, 'customers')
        successCounter.tick()
        PicoStoreInstance.get('customers').add(data).then(lambda res: successAdd(res), lambda err: fail(err))


    def successDestroy(res):
        assert_equals(res, 0)
        successCounter.tick()
        PicoStoreInstance.init(collection).then(lambda res: successInit(res), lambda err: fail(err))


    PicoStoreInstance.destroy().then(lambda res: successDestroy(res), lambda err: fail(err))
    assert_equals(4, successCounter.value())
    assert_equals(0, failCounter.value())


def testRightLikeAllResults():
    PicoStoreInstance = PicoStore()
    successCounter = Counter()
    failCounter = Counter()
    collection =  {
        'customers' : {
                'searchFields' : {'name' : 'string', 'age': 'integer'}
        }
    }

    data = [{'name': 'hayata', 'age': 1}, {'name': 'hayatashin', 'age': 2}, {'name': 'hayataS', 'age': 3}, {'name': 'hayata is raikage', 'age': 4}]
    query = [
        {'rightLike': [{'name': 'hayata'}]}

    ]

    def fail(err):
        failCounter.tick()
        print 'Failed with ' + err

    def successFind(res):
        assert_equals(len(res), 4)
        successCounter.tick()
        assert_equals(res[0]['_json']['name'], 'hayata')
        successCounter.tick()
        assert_equals(res[1]['_json']['name'], 'hayatashin')
        successCounter.tick()
        assert_equals(res[2]['_json']['name'], 'hayataS')
        successCounter.tick()
        assert_equals(res[3]['_json']['name'], 'hayata is raikage')
        successCounter.tick()

     
    def successAdd(res):
        assert_equals(res, 4)
        successCounter.tick()
        '''
            select *
                from 'customers'
                where 
                    [name] LIKE 'hayata-@-%'
        '''
        PicoStoreInstance.get('customers').find(query).then(lambda res: successFind(res), lambda err: fail(err))

    def successInit(res):
        assert_equals(res['customers'].name, 'customers')
        successCounter.tick()
        PicoStoreInstance.get('customers').add(data).then(lambda res: successAdd(res), lambda err: fail(err))


    def successDestroy(res):
        assert_equals(res, 0)
        successCounter.tick()
        PicoStoreInstance.init(collection).then(lambda res: successInit(res), lambda err: fail(err))


    PicoStoreInstance.destroy().then(lambda res: successDestroy(res), lambda err: fail(err))
    assert_equals(8, successCounter.value())
    assert_equals(0, failCounter.value())

def testLeftLikeTest():
    PicoStoreInstance = PicoStore()
    successCounter = Counter()
    failCounter = Counter()
    collection =  {
        'customers' : {
                'searchFields' : {'name' : 'string', 'age': 'integer'}
        }
    }

    data = [{'name': 'hayatashin', 'age': 1}, {'name': 'shin', 'age': 2}, {'name': 'ShinHayata', 'age': 3}, {'name': 'HAYATAShiN', 'age': 4}, {'name': 'Hayata is the surname for shin', 'age': 5}]

    query = [
        {'leftLike': [  {'name': 'shin'}]}

    ]

    def fail(err):
        failCounter.tick()
        print 'Failed with ' + err

    def successFind(res):
        assert_equals(len(res), 4)
        successCounter.tick()
        assert_equals(res[0]['_json']['name'], 'hayatashin')
        successCounter.tick()
        assert_equals(res[1]['_json']['name'], 'shin')
        successCounter.tick()
        assert_equals(res[2]['_json']['name'], 'HAYATAShiN')
        successCounter.tick()
        assert_equals(res[3]['_json']['name'], 'Hayata is the surname for shin')

    def successAdd(res):
        assert_equals(res, 5)
        successCounter.tick()
        '''
            select *
            from 'customers'
            where
                [name] LIKE '%-@-shin'
        '''
        PicoStoreInstance.get('customers').find(query).then(lambda res: successFind(res), lambda err: fail(err))

    def successInit(res):
        assert_equals(res['customers'].name, 'customers')
        successCounter.tick()
        PicoStoreInstance.get('customers').add(data).then(lambda res: successAdd(res), lambda err: fail(err))


    def successDestroy(res):
        assert_equals(res, 0)
        successCounter.tick()
        PicoStoreInstance.init(collection).then(lambda res: successInit(res), lambda err: fail(err))


    PicoStoreInstance.destroy().then(lambda res: successDestroy(res), lambda err: fail(err))
    assert_equals(7, successCounter.value())
    assert_equals(0, failCounter.value())

def testNotLeftLike():
    PicoStoreInstance = PicoStore()
    successCounter = Counter()
    failCounter = Counter()
    collection =  {
        'customers' : {
                'searchFields' : {'name' : 'string', 'age': 'integer'}
        }
    }

    data = [{'name': 'hayatashin', 'age': 1}, {'name': 'shin', 'age': 2}, {'name': 'ShinHayata', 'age': 3}, {'name': 'HAYATAShiN', 'age': 4}, {'name': 'Hayata is the surname for shin', 'age': 5}]

    query = [
        {'notLeftLike': [  {'name': 'shin'}]}

    ]

    def fail(err):
        failCounter.tick()
        print 'Failed with ' + err

    def successFind(res):
        assert_equals(len(res), 1)
        successCounter.tick()
        assert_equals(res[0]['_json']['name'], 'ShinHayata')
        successCounter.tick()
      
    def successAdd(res):
        assert_equals(res, 5)
        successCounter.tick()
        '''
            select *
            from 'customers'
            where
                [name] NOT LIKE '%-@-shin'
        '''
        PicoStoreInstance.get('customers').find(query).then(lambda res: successFind(res), lambda err: fail(err))

    def successInit(res):
        assert_equals(res['customers'].name, 'customers')
        successCounter.tick()
        PicoStoreInstance.get('customers').add(data).then(lambda res: successAdd(res), lambda err: fail(err))


    def successDestroy(res):
        assert_equals(res, 0)
        successCounter.tick()
        PicoStoreInstance.init(collection).then(lambda res: successInit(res), lambda err: fail(err))


    PicoStoreInstance.destroy().then(lambda res: successDestroy(res), lambda err: fail(err))
    assert_equals(5, successCounter.value())
    assert_equals(0, failCounter.value())

def testLessThanFind():
    PicoStoreInstance = PicoStore()
    successCounter = Counter()
    failCounter = Counter()
    collection =  {
        'customers' : {
                'searchFields' : {'name' : 'string', 'age': 'integer'}
        }
    }

    data = [{'name': 'shin', 'age': 1}, {'name': 'deta', 'age': 2}, {'name': 'shu', 'age': 2}, {'name': 'ango', 'age': 4}, {'name': 'kenshin', 'age': 5}]

    query = [
        {'lessThan': [  {'age': 3}]}

    ]

    def fail(err):
        failCounter.tick()
        print 'Failed with ' + err

    def successFind(res):
        assert_equals(len(res), 3)
        successCounter.tick()
        assert_equals(res[0]['_json']['name'], 'shin')
        successCounter.tick()
        assert_equals(res[1]['_json']['name'], 'deta')
        successCounter.tick()
        assert_equals(res[2]['_json']['name'], 'shu')
      
    def successAdd(res):
        assert_equals(res, 5)
        successCounter.tick()
        '''
            select *
            from 'customers'
            where
                [age] < 3
        '''
        PicoStoreInstance.get('customers').find(query).then(lambda res: successFind(res), lambda err: fail(err))

    def successInit(res):
        assert_equals(res['customers'].name, 'customers')
        successCounter.tick()
        PicoStoreInstance.get('customers').add(data).then(lambda res: successAdd(res), lambda err: fail(err))


    def successDestroy(res):
        assert_equals(res, 0)
        successCounter.tick()
        PicoStoreInstance.init(collection).then(lambda res: successInit(res), lambda err: fail(err))


    PicoStoreInstance.destroy().then(lambda res: successDestroy(res), lambda err: fail(err))
    assert_equals(6, successCounter.value())
    assert_equals(0, failCounter.value())

def testLessThanEqualsFind():
    PicoStoreInstance = PicoStore()
    successCounter = Counter()
    failCounter = Counter()
    collection =  {
        'customers' : {
                'searchFields' : {'name' : 'string', 'age': 'integer'}
        }
    }

    data = [{'name': 'shin', 'age': 1}, {'name': 'deta', 'age': 2}, {'name': 'shu', 'age': 2}, {'name': 'ango', 'age': 4}, {'name': 'kenshin', 'age': 5}]

    query = [
        {'lessOrEqualThan': [  {'age': 4}]}

    ]

    def fail(err):
        failCounter.tick()
        print 'Failed with ' + err

    def successFind(res):
        assert_equals(len(res), 4)
        successCounter.tick()
        assert_equals(res[0]['_json']['name'], 'shin')
        successCounter.tick()
        assert_equals(res[1]['_json']['name'], 'deta')
        successCounter.tick()
        assert_equals(res[2]['_json']['name'], 'shu')
        successCounter.tick()
        assert_equals(res[3]['_json']['name'], 'ango')
      
    def successAdd(res):
        assert_equals(res, 5)
        successCounter.tick()
        '''
            select *
            from 'customers'
            where
                [age] <= 4
        '''
        PicoStoreInstance.get('customers').find(query).then(lambda res: successFind(res), lambda err: fail(err))

    def successInit(res):
        assert_equals(res['customers'].name, 'customers')
        successCounter.tick()
        PicoStoreInstance.get('customers').add(data).then(lambda res: successAdd(res), lambda err: fail(err))


    def successDestroy(res):
        assert_equals(res, 0)
        successCounter.tick()
        PicoStoreInstance.init(collection).then(lambda res: successInit(res), lambda err: fail(err))


    PicoStoreInstance.destroy().then(lambda res: successDestroy(res), lambda err: fail(err))
    assert_equals(7, successCounter.value())
    assert_equals(0, failCounter.value())


def testGreaterThanFind():
    PicoStoreInstance = PicoStore()
    successCounter = Counter()
    failCounter = Counter()
    collection =  {
        'customers' : {
                'searchFields' : {'name' : 'string', 'age': 'integer'}
        }
    }

    data = [{'name': 'shin', 'age': 1}, {'name': 'deta', 'age': 2}, {'name': 'shu', 'age': 2}, {'name': 'ango', 'age': 4}, {'name': 'kenshin', 'age': 5}]

    query = [
        {'greaterThan': [  {'age': 2}]}

    ]

    def fail(err):
        failCounter.tick()
        print 'Failed with ' + err

    def successFind(res):
        assert_equals(len(res), 2)
        successCounter.tick()
        assert_equals(res[0]['_json']['name'], 'ango')
        successCounter.tick()
        assert_equals(res[1]['_json']['name'], 'kenshin')
        successCounter.tick()
      
    def successAdd(res):
        assert_equals(res, 5)
        successCounter.tick()
        '''
            select *
            from 'customers'
            where
                [age] > 2
        '''
        PicoStoreInstance.get('customers').find(query).then(lambda res: successFind(res), lambda err: fail(err))

    def successInit(res):
        assert_equals(res['customers'].name, 'customers')
        successCounter.tick()
        PicoStoreInstance.get('customers').add(data).then(lambda res: successAdd(res), lambda err: fail(err))


    def successDestroy(res):
        assert_equals(res, 0)
        successCounter.tick()
        PicoStoreInstance.init(collection).then(lambda res: successInit(res), lambda err: fail(err))


    PicoStoreInstance.destroy().then(lambda res: successDestroy(res), lambda err: fail(err))
    assert_equals(6, successCounter.value())
    assert_equals(0, failCounter.value())    


def testGreaterThanEqualsFind():
    PicoStoreInstance = PicoStore()
    successCounter = Counter()
    failCounter = Counter()
    collection =  {
        'customers' : {
                'searchFields' : {'name' : 'string', 'age': 'integer'}
        }
    }

    data = [{'name': 'shin', 'age': 1}, {'name': 'deta', 'age': 2}, {'name': 'shu', 'age': 2}, {'name': 'ango', 'age': 4}, {'name': 'kenshin', 'age': 5}]

    query = [
        {'greaterOrEqualThan': [  {'age': 2}]}

    ]

    def fail(err):
        failCounter.tick()
        print 'Failed with ' + err

    def successFind(res):
        assert_equals(len(res), 4)
        successCounter.tick()
        assert_equals(res[0]['_json']['name'], 'deta')
        successCounter.tick()
        assert_equals(res[1]['_json']['name'], 'shu')
        successCounter.tick()
        assert_equals(res[2]['_json']['name'], 'ango')
        successCounter.tick()
        assert_equals(res[3]['_json']['name'], 'kenshin')
        successCounter.tick()
      
    def successAdd(res):
        assert_equals(res, 5)
        successCounter.tick()
        '''
            select *
            from 'customers'
            where
                [age] >= 2
        '''
        PicoStoreInstance.get('customers').find(query).then(lambda res: successFind(res), lambda err: fail(err))

    def successInit(res):
        assert_equals(res['customers'].name, 'customers')
        successCounter.tick()
        PicoStoreInstance.get('customers').add(data).then(lambda res: successAdd(res), lambda err: fail(err))


    def successDestroy(res):
        assert_equals(res, 0)
        successCounter.tick()
        PicoStoreInstance.init(collection).then(lambda res: successInit(res), lambda err: fail(err))


    PicoStoreInstance.destroy().then(lambda res: successDestroy(res), lambda err: fail(err))
    assert_equals(8, successCounter.value())
    assert_equals(0, failCounter.value())       


def testIntegerEqualFind():
    PicoStoreInstance = PicoStore()
    successCounter = Counter()
    failCounter = Counter()
    collection =  {
        'customers' : {
                'searchFields' : {'name' : 'string', 'age': 'integer'}
        }
    }

    data = [{'name': 'shin', 'age': 1}, {'name': 'deta', 'age': 2}, {'name': 'shu', 'age': 2}, {'name': 'ango', 'age': 4}, {'name': 'kenshin', 'age': 5}]

    query = [
        {'equal': [  {'age': 2}]}

    ]

    def fail(err):
        failCounter.tick()
        print 'Failed with ' + err

    def successFind(res):
        assert_equals(len(res), 2)
        successCounter.tick()
        assert_equals(res[0]['_json']['name'], 'deta')
        successCounter.tick()
        assert_equals(res[1]['_json']['name'], 'shu')
        successCounter.tick()
      
    def successAdd(res):
        assert_equals(res, 5)
        successCounter.tick()
        '''
            select *
            from 'customers'
            where
                [age] = 2
        '''
        PicoStoreInstance.get('customers').find(query).then(lambda res: successFind(res), lambda err: fail(err))

    def successInit(res):
        assert_equals(res['customers'].name, 'customers')
        successCounter.tick()
        PicoStoreInstance.get('customers').add(data).then(lambda res: successAdd(res), lambda err: fail(err))


    def successDestroy(res):
        assert_equals(res, 0)
        successCounter.tick()
        PicoStoreInstance.init(collection).then(lambda res: successInit(res), lambda err: fail(err))


    PicoStoreInstance.destroy().then(lambda res: successDestroy(res), lambda err: fail(err))
    assert_equals(6, successCounter.value())
    assert_equals(0, failCounter.value())

def testStringEqualFind():
    PicoStoreInstance = PicoStore()
    successCounter = Counter()
    failCounter = Counter()
    collection =  {
        'customers' : {
                'searchFields' : {'name' : 'string', 'age': 'integer'}
        }
    }

    data = [{'name': 'shin', 'age': 1}, {'name': 'deta', 'age': 2}, {'name': 'shu', 'age': 2}, {'name': 'ango', 'age': 4}, {'name': 'kenshin', 'age': 5}]

    query = [
        {'equal': [  {'name': 'shin'}]}

    ]

    def fail(err):
        failCounter.tick()
        print 'Failed with ' + err

    def successFind(res):
        assert_equals(len(res), 1)
        successCounter.tick()
        assert_equals(res[0]['_json']['name'], 'shin')
        successCounter.tick()
      
    def successAdd(res):
        assert_equals(res, 5)
        successCounter.tick()
        '''
            select *
            from 'customers'
            where
                [age] = 2
        '''
        PicoStoreInstance.get('customers').find(query).then(lambda res: successFind(res), lambda err: fail(err))

    def successInit(res):
        assert_equals(res['customers'].name, 'customers')
        successCounter.tick()
        PicoStoreInstance.get('customers').add(data).then(lambda res: successAdd(res), lambda err: fail(err))


    def successDestroy(res):
        assert_equals(res, 0)
        successCounter.tick()
        PicoStoreInstance.init(collection).then(lambda res: successInit(res), lambda err: fail(err))


    PicoStoreInstance.destroy().then(lambda res: successDestroy(res), lambda err: fail(err))
    assert_equals(5, successCounter.value())
    assert_equals(0, failCounter.value())          


def testIntegerNotEqualFind():
    PicoStoreInstance = PicoStore()
    successCounter = Counter()
    failCounter = Counter()
    collection =  {
        'customers' : {
                'searchFields' : {'name' : 'string', 'age': 'integer'}
        }
    }

    data = [{'name': 'shin', 'age': 1}, {'name': 'deta', 'age': 2}, {'name': 'shu', 'age': 2}, {'name': 'ango', 'age': 4}, {'name': 'kenshin', 'age': 5}]

    query = [
        {'notEqual': [  {'age': 2}]}

    ]

    def fail(err):
        failCounter.tick()
        print 'Failed with ' + err

    def successFind(res):
        assert_equals(len(res), 3)
        successCounter.tick()
        assert_equals(res[0]['_json']['name'], 'shin')
        successCounter.tick()
        assert_equals(res[1]['_json']['name'], 'ango')
        successCounter.tick()
        assert_equals(res[2]['_json']['name'], 'kenshin')
      
    def successAdd(res):
        assert_equals(res, 5)
        successCounter.tick()
        '''
            select *
            from 'customers'
            where
                [age] != 2
        '''
        PicoStoreInstance.get('customers').find(query).then(lambda res: successFind(res), lambda err: fail(err))

    def successInit(res):
        assert_equals(res['customers'].name, 'customers')
        successCounter.tick()
        PicoStoreInstance.get('customers').add(data).then(lambda res: successAdd(res), lambda err: fail(err))


    def successDestroy(res):
        assert_equals(res, 0)
        successCounter.tick()
        PicoStoreInstance.init(collection).then(lambda res: successInit(res), lambda err: fail(err))


    PicoStoreInstance.destroy().then(lambda res: successDestroy(res), lambda err: fail(err))
    assert_equals(6, successCounter.value())
    assert_equals(0, failCounter.value())

def testIntegerInFind():
    PicoStoreInstance = PicoStore()
    successCounter = Counter()
    failCounter = Counter()
    collection =  {
        'customers' : {
                'searchFields' : {'name' : 'string', 'age': 'integer'}
        }
    }

    data = [{'name': 'shin', 'age': 1}, {'name': 'deta', 'age': 2}, {'name': 'shu', 'age': 2}, {'name': 'ango', 'age': 3}, {'name': 'kenshin', 'age': 5}]

    query = [
        {'inside': [  {'age': [2,3]}]}

    ]

    def fail(err):
        failCounter.tick()
        print 'Failed with ' + err

    def successFind(res):
        assert_equals(len(res), 3)
        successCounter.tick()
        assert_equals(res[0]['_json']['name'], 'deta')
        successCounter.tick()
        assert_equals(res[1]['_json']['name'], 'shu')
        successCounter.tick()
        assert_equals(res[2]['_json']['name'], 'ango')
        successCounter.tick()
      
    def successAdd(res):
        assert_equals(res, 5)
        successCounter.tick()
        '''
            select *
            from 'customers'
            where
                [age] IN (2, 3)
        '''
        PicoStoreInstance.get('customers').find(query).then(lambda res: successFind(res), lambda err: fail(err))

    def successInit(res):
        assert_equals(res['customers'].name, 'customers')
        successCounter.tick()
        PicoStoreInstance.get('customers').add(data).then(lambda res: successAdd(res), lambda err: fail(err))


    def successDestroy(res):
        assert_equals(res, 0)
        successCounter.tick()
        PicoStoreInstance.init(collection).then(lambda res: successInit(res), lambda err: fail(err))


    PicoStoreInstance.destroy().then(lambda res: successDestroy(res), lambda err: fail(err))
    assert_equals(7, successCounter.value())
    assert_equals(0, failCounter.value())    

def testNotInsideTest():
    PicoStoreInstance = PicoStore()
    successCounter = Counter()
    failCounter = Counter()
    collection =  {
        'customers' : {
                'searchFields' : {'name' : 'string', 'age': 'integer'}
        }
    }

    data = [{'name': 'shin', 'age': 1}, {'name': 'deta', 'age': 2}, {'name': 'shu', 'age': 2}, {'name': 'ango', 'age': 3}, {'name': 'kenshin', 'age': 5}]

    query = [
        {'notInside': [  {'age': [2,3]}]}

    ]

    def fail(err):
        failCounter.tick()
        print 'Failed with ' + err

    def successFind(res):
        assert_equals(len(res), 2)
        successCounter.tick()
        assert_equals(res[0]['_json']['name'], 'shin')
        successCounter.tick()
        assert_equals(res[1]['_json']['name'], 'kenshin')
        successCounter.tick()
        
      
    def successAdd(res):
        assert_equals(res, 5)
        successCounter.tick()
        '''
            select *
            from 'customers'
            where
                [age] NOT IN (2, 3)
        '''
        PicoStoreInstance.get('customers').find(query).then(lambda res: successFind(res), lambda err: fail(err))

    def successInit(res):
        assert_equals(res['customers'].name, 'customers')
        successCounter.tick()
        PicoStoreInstance.get('customers').add(data).then(lambda res: successAdd(res), lambda err: fail(err))


    def successDestroy(res):
        assert_equals(res, 0)
        successCounter.tick()
        PicoStoreInstance.init(collection).then(lambda res: successInit(res), lambda err: fail(err))


    PicoStoreInstance.destroy().then(lambda res: successDestroy(res), lambda err: fail(err))
    assert_equals(6, successCounter.value())
    assert_equals(0, failCounter.value())

def testBetweenFind():
    PicoStoreInstance = PicoStore()
    successCounter = Counter()
    failCounter = Counter()
    collection =  {
        'customers' : {
                'searchFields' : {'name' : 'string', 'age': 'integer'}
        }
    }

    data = [{'name': 'shin', 'age': 1}, {'name': 'deta', 'age': 2}, {'name': 'shu', 'age': 2}, {'name': 'ango', 'age': 3}, {'name': 'kenshin', 'age': 5}]

    query = [
        {'between': [  {'age': [1,4]}]}

    ]

    def fail(err):
        failCounter.tick()
        print 'Failed with ' + err

    def successFind(res):
        assert_equals(len(res), 4)
        successCounter.tick()
        assert_equals(res[0]['_json']['name'], 'shin')
        successCounter.tick()
        assert_equals(res[1]['_json']['name'], 'deta')
        successCounter.tick()
        assert_equals(res[2]['_json']['name'], 'shu')
        successCounter.tick()
        assert_equals(res[3]['_json']['name'], 'ango')
        
      
    def successAdd(res):
        assert_equals(res, 5)
        successCounter.tick()
        '''
            select *
            from 'customers'
            where
                [age] BETWEEN  1 AND 4
        '''
        PicoStoreInstance.get('customers').find(query).then(lambda res: successFind(res), lambda err: fail(err))

    def successInit(res):
        assert_equals(res['customers'].name, 'customers')
        successCounter.tick()
        PicoStoreInstance.get('customers').add(data).then(lambda res: successAdd(res), lambda err: fail(err))


    def successDestroy(res):
        assert_equals(res, 0)
        successCounter.tick()
        PicoStoreInstance.init(collection).then(lambda res: successInit(res), lambda err: fail(err))


    PicoStoreInstance.destroy().then(lambda res: successDestroy(res), lambda err: fail(err))
    assert_equals(7, successCounter.value())
    assert_equals(0, failCounter.value())    
