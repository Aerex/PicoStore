from nose.tools import *
import pdb
import sys
sys.path.insert(0, "../")
from picostore import PicoStore


#Init

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

def test_initoffline():
    PicoStoreInstance = PicoStore()
    successCounter = Counter()
    failCounter = Counter()
    collection =  {
        'customers' : {
                'searchFields' : {'id' : 'integer'}
        }
    }

    data = [
        {'id' : 1, 'name': 'carlos', 'age': 1},
        {'id': 2, 'name': 'dgonz', 'age': 2},
        {'id': 3, 'name': 'mike', 'age': 3}
    ]

    def fail(err):
        failCounter.tick()
        print 'Failed with ' + err

    def successInit(res):
        assert_equals(res['customers'].name, 'customers')
        successCounter.tick()
        successCounter.message('collection name is customers')


    def successDestroy(res):
        assert_equals(res, 0)
        successCounter.tick()
        PicoStoreInstance.init(collection).then(lambda res: successInit(res), lambda err: fail(err))

    PicoStoreInstance.destroy().then(lambda res: successDestroy(res), lambda err: fail(err))
    assert_equals(2, successCounter.value())
    assert_equals(0, failCounter.value())

def testInitWithPass():
    PicoStoreInstance = PicoStore()
    successCounter = Counter()
    failCounter = Counter()

    collection =  {
        'customers' : {
            'searchFields' : {'id' : 'integer'}
        }
    }

    data = [
        {'id' : 1, 'name': 'carlos', 'age': 1},
        {'id': 2, 'name': 'dgonz', 'age': 2},
        {'id': 3, 'name': 'mike', 'age': 3}
    ]

    options = {
        'username': 'carlos',
        'password': '123'
    }

    def fail(err):
        failCounter.tick()
        print 'Failed with ' + err

    def successInit(res):
        assert_equals(res['customers'].name, 'customers')
        successCounter.tick()

    def successDestroy(res):
        assert_equals(res, 0)
        successCounter.tick()
        PicoStoreInstance.init(collection).then(lambda res: successInit(res), lambda err: fail(err))


    PicoStoreInstance.destroy().then(lambda res: successDestroy(res), lambda err: fail(err))
    assert_equals(2, successCounter.value())
    assert_equals(0, failCounter.value())

def testInitWithEmptyCollection():
    PicoStoreInstance = PicoStore()
    successCounter = Counter()
    failCounter = Counter()
    collection = {}

    def fail(err):
        failCounter.tick()
        print 'Failed with ' + err

    def successInit(res):
        assert_equals(len(res), 0)
        successCounter.tick()
        assert_true(type(res) is dict)
        successCounter.tick()

    def successDestroy(res):
        assert_equals(res, 0)
        successCounter.tick()
        PicoStoreInstance.init(collection).then(lambda res: successInit(res), lambda err: fail(err))


    PicoStoreInstance.destroy().then(lambda res: successDestroy(res), lambda err: fail(err))
    assert_equals(3, successCounter.value())
    assert_equals(0, failCounter.value())

def testInitWithEmptyColObj():
    PicoStoreInstance = PicoStore()
    successCounter = Counter()
    failCounter = Counter()

    collection = {
        'customers': {}
    }

    def fail(err):
        print 'Failed with ' + err
        failCounter.tick()

    def successInit(res):
        assert_equals(len(res['customers'].searchFields), 0)
        successCounter.tick()
        assert_true(type(res['customers'].searchFields) is dict)
        successCounter.tick()

    def successDestroy(res):
        assert_equals(res, 0)
        successCounter.tick()
        PicoStoreInstance.init(collection).then(lambda res: successInit(res), lambda err: fail(err))

    PicoStoreInstance.destroy().then(lambda res: successDestroy(res), lambda err: fail(err))
    assert_equals(3, successCounter.value())
    assert_equals(0, failCounter.value())

def testInitWithEmptySearchFields():
    PicoStoreInstance = PicoStore()
    successCounter = Counter()
    failCounter = Counter()

    collection = {
        'customers': {
            'searchFields' : {}
        }
    }

    def fail(err):
        print 'Failed with ' + err
        failCounter.tick()

    def successInit(res):
        assert_equals(len(res['customers'].searchFields), 0)
        successCounter.tick()
        assert_true(type(res['customers'].searchFields) is dict)
        successCounter.tick()

    def successDestroy(res):
        assert_equals(res, 0)
        successCounter.tick()
        PicoStoreInstance.init(collection).then(lambda res: successInit(res), lambda err: fail(err))

    PicoStoreInstance.destroy().then(lambda res: successDestroy(res), lambda err: fail(err))
    assert_equals(3, successCounter.value())
    assert_equals(0, failCounter.value())

def testInitWithInvalidSearchFields():
    PicoStoreInstance = PicoStore()
    successCounter = Counter()
    failCounter = Counter()

    collection = {
        'customers': {
            'searchFields': {'hello': 'thisisnotvalidman'}
        }
    }

    def fail(err):
        errorObject = err.getErrorObject()
        assert_equals(errorObject['err'], -12)
        failCounter.tick()

    def successInit(res):
        successCounter.tick()

    def successDestroy(res):
        assert_equals(res, 0)
        successCounter.tick()
        PicoStoreInstance.init(collection).then(lambda res: successInit(res), lambda err: fail(err))

    PicoStoreInstance.destroy().then(lambda res: successDestroy(res), lambda err: fail(err))
    assert_equals(1, successCounter.value())
    assert_equals(1, failCounter.value())

def testCheckCloseAllClearsInstances():
    PicoStoreInstance = PicoStore()
    successCounter = Counter()
    failCounter = Counter()

    collections = {
        'customers': {
            'searchFields' : {'fn': 'string'}
        },
        'orders': {
            'searchFields': {'active': 'boolean'}
        }
    }

    def fail(err):
        failCounter.tick()

    def successCloseAll(res):
        assert_equals(res, 0)
        successCounter.tick()
        assert_equals(PicoStoreInstance.get('customers'), None)
        successCounter.tick()
        assert_equals(PicoStoreInstance.get('orders'), None)
        successCounter.tick()


    def successInit(res):
        assert_equals(res['customers'].name, 'customers')
        successCounter.tick()
        assert_equals(res['orders'].name, 'orders')
        successCounter.tick()
        assert_equals(PicoStoreInstance.get('orders').name, 'orders')
        successCounter.tick()
        assert_equals(PicoStoreInstance.get('customers').name, 'customers')
        successCounter.tick()
        PicoStoreInstance.closeAll().then(lambda res: successCloseAll(res), lambda err: fail(err))


    def successDestroy(res):
        assert_equals(res, 0)
        successCounter.tick()
        PicoStoreInstance.init(collections).then(lambda res: successInit(res), lambda err: fail(err))

    PicoStoreInstance.destroy().then(lambda res: successDestroy(res), lambda err: fail(err))
    assert_equals(8, successCounter.value())
    assert_equals(0, failCounter.value())

def testDestroyClearsInstance():
    PicoStoreInstance = PicoStore()
    successCounter = Counter()
    failCounter = Counter()

    collections = {
        'customers': {
            'searchFields' : {'fn': 'string'}
        },
        'orders': {
            'searchFields': {'active': 'boolean'}
        }
    }

    def fail(err):
        failCounter.tick()

    def successDestroyTwo(res):
        assert_equals(res, 0)
        successCounter.tick()
        assert_equals(PicoStoreInstance.get('customers'), None)
        successCounter.tick()
        assert_equals(PicoStoreInstance.get('orders'), None)
        successCounter.tick()

    def successInit(res):
        assert_equals(res['customers'].name, 'customers')
        successCounter.tick()
        assert_equals(res['orders'].name, 'orders')
        successCounter.tick()
        assert_equals(PicoStoreInstance.get('orders').name, 'orders')
        successCounter.tick()
        assert_equals(PicoStoreInstance.get('customers').name, 'customers')
        successCounter.tick()
        PicoStoreInstance.destroy().then(lambda res: successDestroyTwo(res), lambda err: fail(err))


    def successDestroyOne(res):
        assert_equals(res, 0)
        successCounter.tick()
        PicoStoreInstance.init(collections).then(lambda res: successInit(res), lambda err: fail(err))


    PicoStoreInstance.destroy().then(lambda res: successDestroyOne(res), lambda err: fail(err))
    assert_equals(8, successCounter.value())
    assert_equals(0, failCounter.value())

def testPassNoSearchFieldsTwoSecondCollection():
    PicoStoreInstance = PicoStore()
    successCounter = Counter()
    failCounter = Counter()

    collections = {
        'customers': {
            'searchFields' : {'fn': 'string'}
        },
        'orders': {
        }
    }

    def fail(err):
        failCounter.tick()

    def successInit(res):
        assert_equals(res['customers'].name, 'customers')
        successCounter.tick()
        assert_equals(res['orders'].name, 'orders')
        successCounter.tick()
        assert_equals(res['customers'].searchFields, {'fn': 'string'})
        successCounter.tick()
        assert_equals(res['orders'].searchFields, {})


    def successDestroy(res):
        assert_equals(res, 0)
        successCounter.tick()
        PicoStoreInstance.init(collections).then(lambda res: successInit(res), lambda err: fail(err))

    PicoStoreInstance.destroy().then(lambda res: successDestroy(res), lambda err: fail(err))
    assert_equals(4, successCounter.value())
    assert_equals(0, failCounter.value())


def testInitWithInvalidObject():
    PicoStoreInstance = PicoStore()
    successCounter = Counter()
    failCounter = Counter()
    def func():
        pass
    index = -1
    params = [True, {},[], [1,2,3],func, 123]


    def fail(err):
        failCounter.tick()

    def successInit(res, index):
        assert_equals(res, {})
        index+=1
        successCounter.tick()
        if index < 6:
            PicoStoreInstance.init(params[index]).then(lambda res: successInit(res, index), lambda err: fail(err))

    def successDestroy(res):
        assert_equals(res, 0)
        successCounter.tick()
        PicoStoreInstance.init(None).then(lambda res: successInit(res, index), lambda err: fail(err))

    PicoStoreInstance.destroy().then(lambda res: successDestroy(res), lambda err: fail(err))
    assert_equals(8, successCounter.value())
    assert_equals(0, failCounter.value())

def testInitWithAdditionalSearchFields():
    PicoStoreInstance = PicoStore()
    successCounter = Counter()
    failCounter = Counter()
    collection = {
        'customers': {
            'searchFields': {'fn': 'string'},
            'additionalSearchFields': {'id': 'integer'}
        },
        'orders': {
            'searchFields': {'fn': 'string'},
            'additionalSearchFields': {'value': 'integer'}
        }
    }


    def fail(err):
        failCounter.tick()

    def successInit(res):
        assert_equals(res['customers'].name, 'customers')
        successCounter.tick()
        assert_equals(res['orders'].name, 'orders')
        successCounter.tick()
        assert_equals(res['customers'].searchFields, {'fn': 'string'})
        successCounter.tick()
        assert_equals(res['orders'].searchFields, {'fn': 'string'})
        successCounter.tick()
        assert_equals(res['customers'].additionalSearchFields, {'id': 'integer'})
        successCounter.tick()
        assert_equals(res['orders'].additionalSearchFields, {'value': 'integer'})


    def successDestroy(res):
        assert_equals(res, 0)
        successCounter.tick()
        PicoStoreInstance.init(collection).then(lambda res: successInit(res), lambda err: fail(err))

    PicoStoreInstance.destroy().then(lambda res: successDestroy(res), lambda err: fail(err))
    assert_equals(6, successCounter.value())
    assert_equals(0, failCounter.value())




