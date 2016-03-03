from nose.tools import *
#import pytest
import pdb
import sys
sys.path.insert(0, "../")
from picostore import PicoStore


#Count

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

def testSimpleCount():
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

    query = [
        {'equal': [{'name': 'shin'}]}
    ]


    def fail(err):
        failCounter.tick()
        print 'Failed with ' + err

    def successCount(res):
        assert_equals(res, 1)
        successCounter.tick()

    def successAdd(res):
        assert_equals(res, 3)
        successCounter.tick()
        PicoStoreInstance.get('customers').count(query).then(lambda res: successCount(res), lambda err: fail(err)) 

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

def testCountWithLike():
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

    query = [
        {'like': [{'name': 'sh'}]}
    ]


    def fail(err):
        failCounter.tick()
        print 'Failed with ' + err

    def successCount(res):
        assert_equals(res, 2)
        successCounter.tick()

    def successAdd(res):
        assert_equals(res, 3)
        successCounter.tick()
        PicoStoreInstance.get('customers').count(query).then(lambda res: successCount(res), lambda err: fail(err)) 

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



def testCountAll():
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

    def fail(err):
        failCounter.tick()
        print 'Failed with ' + err

    def successCount(res):
        assert_equals(res, 3)
        successCounter.tick()

    def successAdd(res):
        assert_equals(res, 3)
        successCounter.tick()
        PicoStoreInstance.get('customers').count().then(lambda res: successCount(res), lambda err: fail(err)) 

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


def testCountOnTwoSearchFields():
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

    query = [
        {'equal': [{'name': 'shin'}, {'age': 1}]}
    ]


    def fail(err):
        failCounter.tick()
        print 'Failed with ' + err

    def successCount(res):
        assert_equals(res, 1)
        successCounter.tick()

    def successAdd(res):
        assert_equals(res, 3)
        successCounter.tick()
        PicoStoreInstance.get('customers').count(query).then(lambda res: successCount(res), lambda err: fail(err)) 

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







