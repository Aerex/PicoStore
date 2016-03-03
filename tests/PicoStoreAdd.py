from nose.tools import *
#import pytest
import pdb
import sys
sys.path.insert(0, "../")
from picostore import PicoStore


#Add

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

def testSimpleAdd():
    PicoStoreInstance = PicoStore()
    successCounter = Counter()
    failCounter = Counter()
    collection =  {
        'customers' : {
                'searchFields' : {'id' : 'integer'}
        }
    }

    data = [
        {'id' : 1, 'name': 'shin', 'age': 1},
        {'id': 2, 'name': 'shuu', 'age': 2},
        {'id': 3, 'name': 'kenshin', 'age': 3}
    ]

    def fail(err):
        failCounter.tick()
        print 'Failed with ' + err

    def successAdd(res):
        assert_equals(res, 3)
        successCounter.tick()

    def successInit(res):
        assert_equals(res['customers'].name, 'customers')
        successCounter.tick()
        PicoStoreInstance.get('customers').add(data).then(lambda res: successAdd(res), lambda err: fail(err))


    def successDestroy(res):
        assert_equals(res, 0)
        successCounter.tick()
        PicoStoreInstance.init(collection).then(lambda res: successInit(res), lambda err: fail(err))

    PicoStoreInstance.destroy().then(lambda res: successDestroy(res), lambda err: fail(err))
    assert_equals(3, successCounter.value())
    assert_equals(0, failCounter.value())

def testAddEmptyData():
    PicoStoreInstance = PicoStore()
    successCounter = Counter()
    failCounter = Counter()

    collection = {
        'customers': {
            'searchFields': {'name': 'string', 'age': 'integer'}
        }
    }

    def fail(err):
        failCounter.tick()
        print 'Failed with ' + err

    def successAdd(res):
        assert_equals(res, 1)
        successCounter.tick()

    def successInit(res):
        assert_equals(res['customers'].name, 'customers')
        successCounter.tick()
        PicoStoreInstance.get('customers').add({}).then(lambda res: successAdd(res), lambda err: fail(err))


    def successDestroy(res):
        assert_equals(res, 0)
        successCounter.tick()
        PicoStoreInstance.init(collection).then(lambda res: successInit(res), lambda err: fail(err))

    PicoStoreInstance.destroy().then(lambda res: successDestroy(res), lambda err: fail(err))
    assert_equals(2, successCounter.value())
    assert_equals(0, failCounter.value())


def testAddingByParts():
    PicoStoreInstance = PicoStore()
    successCounter = Counter()
    failCounter = Counter()

    collection = {
        'customers': {
            'searchFields': {'name': 'string', 'age': 'integer'}
        }
    }

    data = [{'name': 'shin', 'age': 1}, {'name': 'shu', 'age': 2}, {'name': 'kenshin', 'age': 3}, {'name': 'deta', 'age': 4}]


    def fail(err):
        failCounter.tick()
        print 'Failed with ' + err

    def successAdd2(res):
        assert_equals(res, 2)
        successCounter.tick()

    def successAdd1(res):
        assert_equals(res, 2)
        successCounter.tick()
        PicoStoreInstance.get('customers').add([data[2],data[3]]).then(lambda res: successAdd2(res), lambda err: fail(err))

    def successInit(res):
        assert_equals(res['customers'].name, 'customers')
        successCounter.tick()
        PicoStoreInstance.get('customers').add([data[0], data[1]]).then(lambda res: successAdd1(res), lambda err: fail(err))


    def successDestroy(res):
        assert_equals(res, 0)
        successCounter.tick()
        PicoStoreInstance.init(collection).then(lambda res: successInit(res), lambda err: fail(err))

    PicoStoreInstance.destroy().then(lambda res: successDestroy(res), lambda err: fail(err))
    assert_equals(4, successCounter.value())
    assert_equals(0, failCounter.value())


def testAddEmptyDataArray():
    PicoStoreInstance = PicoStore()
    successCounter = Counter()
    failCounter = Counter()

    collection = {
        'customers': {
            'searchFields': {'name': 'string', 'age': 'integer'}
        }
    }


    def fail(err):
        failCounter.tick()
        print 'Failed with ' + err

    def successAdd(res):
        assert_equals(res, 0)
        successCounter.tick()

    def successInit(res):
        assert_equals(res['customers'].name, 'customers')
        successCounter.tick()
        PicoStoreInstance.get('customers').add([]).then(lambda res: successAdd(res), lambda err: fail(err))


    def successDestroy(res):
        assert_equals(res, 0)
        successCounter.tick()
        PicoStoreInstance.init(collection).then(lambda res: successInit(res), lambda err: fail(err))

    PicoStoreInstance.destroy().then(lambda res: successDestroy(res), lambda err: fail(err))
    assert_equals(3, successCounter.value())
    assert_equals(0, failCounter.value())

def testAddWithUnderscoreID():
    PicoStoreInstance = PicoStore()
    successCounter = Counter()
    failCounter = Counter()

    collection = {
        'customers': {
            'searchFields': {'_id': 'integer', 'name': 'string', 'age': 'integer'}
        }
    }

    def shouldFail(res):
        errorObject = res.getErrorObject()
        assert_equals(errorObject['err'], -12)
        successCounter.tick()

    def shouldNotSuccess(err):
        failCounter.value()
        print 'Failed with ' + err

    def successDestroy(res):
        assert_equals(res, 0)
        successCounter.tick()
        PicoStoreInstance.init(collection).then(lambda res: shouldNotSuccess(res), lambda err: shouldFail(err))

    PicoStoreInstance.destroy().then(lambda res: successDestroy(res), lambda err: fail(err))
    assert_equals(2, successCounter.value())
    assert_equals(0, failCounter.value())







