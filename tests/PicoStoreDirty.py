from nose.tools import *
import pdb
import sys
sys.path.insert(0, "../")
from picostore import PicoStore


#Dirty

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

def testAddWhenDirtyTrue():
    PicoStoreInstance = PicoStore()
    successCounter = Counter()
    failCounter = Counter()
    collection =  {
        'customers' : {
                'searchFields' : {'name': 'string', 'age' : 'integer'}
        }
    }

    data = [
        {'name': 'shin', 'age': 1},
        {'name': 'shuu', 'age': 2},
        {'name': 'kenshin', 'age': 3}
    ]

    addOptions = {'markDirty': True}



    def fail(err):
        failCounter.tick()
        print 'Failed with ' + err

    def successDirty(res):
        assert_equals(len(res), 3)
        successCounter.tick()
        assert_equals(res[0]['_json']['name'], 'shin')
        successCounter.tick()
        assert_equals(res[0]['_json']['age'], 1)
        successCounter.tick()
        assert_equals(res[1]['_json']['name'], 'shuu')
        successCounter.tick()
        assert_equals(res[1]['_json']['age'], 2)
        successCounter.tick()
        assert_equals(res[2]['_json']['name'], 'kenshin')
        successCounter.tick()
        assert_equals(res[2]['_json']['age'], 3)

    def successAdd(res):
        assert_equals(res, 3)
        successCounter.tick()
        PicoStoreInstance.get('customers').getAllDirtyDocuments().then(lambda res: successDirty(res), lambda err: fail(err)) 

    def successInit(res):
        assert_equals(res['customers'].name, 'customers')
        successCounter.tick()
        PicoStoreInstance.get('customers').add(data, addOptions).then(lambda res: successAdd(res), lambda err: fail(err))


    def successDestroy(res):
        assert_equals(res, 0)
        successCounter.tick()
        PicoStoreInstance.init(collection).then(lambda res: successInit(res), lambda err: fail(err))

    PicoStoreInstance.destroy().then(lambda res: successDestroy(res), lambda err: fail(err))
    assert_equals(9, successCounter.value())
    assert_equals(0, failCounter.value())

def testAddWhenDirtyFalse():
    PicoStoreInstance = PicoStore()
    successCounter = Counter()
    failCounter = Counter()
    collection =  {
        'customers' : {
                'searchFields' : {'name': 'string', 'age' : 'integer'}
        }
    }

    data = [
        {'name': 'shin', 'age': 1},
        {'name': 'shuu', 'age': 2},
        {'name': 'kenshin', 'age': 3}
    ]

    addOptions = {
        'markDirty': False
    }

    def fail(err):
        failCounter.tick()
        print 'Failed with ' + err

    def successDirty(res):
        assert_equals(len(res), 0)
        successCounter.tick()

    def successAdd(res):
        assert_equals(res, 3)
        successCounter.tick()
        PicoStoreInstance.get('customers').getAllDirtyDocuments().then(lambda res: successDirty(res), lambda err: fail(err)) 

    def successInit(res):
        assert_equals(res['customers'].name, 'customers')
        successCounter.tick()
        PicoStoreInstance.get('customers').add(data, addOptions).then(lambda res: successAdd(res), lambda err: fail(err))


    def successDestroy(res):
        assert_equals(res, 0)
        successCounter.tick()
        PicoStoreInstance.init(collection).then(lambda res: successInit(res), lambda err: fail(err))

    PicoStoreInstance.destroy().then(lambda res: successDestroy(res), lambda err: fail(err))
    assert_equals(4, successCounter.value())
    assert_equals(0, failCounter.value())

def testReplaceWithDirtyTrue():
    PicoStoreInstance = PicoStore()
    successCounter = Counter()
    failCounter = Counter()
    collection =  {
        'customers' : {
                'searchFields' : {'name': 'string', 'age' : 'integer'}
        }
    }

    data = [
        {'name': 'shin', 'age': 1},
        {'name': 'shuu', 'age': 2},
        {'name': 'kenshin', 'age': 3}
    ]

    replaceOptions = {
        'markDirty': True
    }
    addOptions = {
        'markDirty': False
    }

    def fail(err):
        failCounter.tick()
        print 'Failed with ' + err

    def successDirty2(res):
        assert_equals(len(res), 1)
        successCounter.tick()
        assert_equals(res[0]['_json']['name'], 'SHIN')
        successCounter.tick()
        assert_equals(res[0]['_json']['age'], 99)

    def successReplace(res):
        assert_equals(res, 1)
        successCounter.tick()
        PicoStoreInstance.get('customers').getAllDirtyDocuments().then(lambda res: successDirty2(res), lambda err: fail(err))

    def successDirty1(res):
        assert_equals(len(res), 0)
        successCounter.tick()
        PicoStoreInstance.get('customers').replace({'_id': 1, '_json': {'name': 'SHIN', 'age': 99}}, replaceOptions).then(lambda res: successReplace(res), lambda err: fail(err))

    def successAdd(res):
        assert_equals(res, 3)
        successCounter.tick()
        PicoStoreInstance.get('customers').getAllDirtyDocuments().then(lambda res: successDirty1(res), lambda err: fail(err)) 

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

def testReplaceWithDirtyFalse():
    PicoStoreInstance = PicoStore()
    successCounter = Counter()
    failCounter = Counter()
    collection =  {
        'customers' : {
                'searchFields' : {'name': 'string', 'age' : 'integer'}
        }
    }

    data = [
        {'name': 'shin', 'age': 1},
        {'name': 'shuu', 'age': 2},
        {'name': 'kenshin', 'age': 3}
    ]

    replaceOptions = {
        'markDirty': False
    }
    addOptions = {
        'markDirty': False
    }

    def fail(err):
        failCounter.tick()
        print 'Failed with ' + err


    def successFindAll(res):
        assert_equals(len(res), 3)
        assert_equals(res[0]['_json']['name'], 'SHIN')
        successCounter.tick()
        assert_equals(res[0]['_json']['age'], 99)
        successCounter.tick()
        assert_equals(res[1]['_json']['name'], 'shuu')
        successCounter.tick()
        assert_equals(res[1]['_json']['age'], 2)
        successCounter.tick()
        assert_equals(res[2]['_json']['name'], 'kenshin')
        successCounter.tick()
        assert_equals(res[2]['_json']['age'], 3)
        successCounter.tick()

    def successDirty2(res):
        assert_equals(len(res), 0)
        successCounter.tick()
        PicoStoreInstance.get('customers').findAll().then(lambda res: successFindAll(res), lambda err: fail(err))

    def successReplace(res):
        assert_equals(res, 1)
        successCounter.tick()
        PicoStoreInstance.get('customers').getAllDirtyDocuments().then(lambda res: successDirty2(res), lambda err: fail(err))

    def successDirty1(res):
        assert_equals(len(res), 0)
        successCounter.tick()
        PicoStoreInstance.get('customers').replace({'_id': 1, '_json': {'name': 'SHIN', 'age': 99}}, replaceOptions).then(lambda res: successReplace(res), lambda err: fail(err))

    def successAdd(res):
        assert_equals(res, 3)
        successCounter.tick()
        PicoStoreInstance.get('customers').getAllDirtyDocuments().then(lambda res: successDirty1(res), lambda err: fail(err)) 

    def successInit(res):
        assert_equals(res['customers'].name, 'customers')
        successCounter.tick()
        PicoStoreInstance.get('customers').add(data, addOptions).then(lambda res: successAdd(res), lambda err: fail(err))


    def successDestroy(res):
        assert_equals(res, 0)
        successCounter.tick()
        PicoStoreInstance.init(collection).then(lambda res: successInit(res), lambda err: fail(err))

    PicoStoreInstance.destroy().then(lambda res: successDestroy(res), lambda err: fail(err))
    assert_equals(12, successCounter.value())
    assert_equals(0, failCounter.value())  