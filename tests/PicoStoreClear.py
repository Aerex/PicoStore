from nose.tools import *    
import pdb
import sys
sys.path.insert(0, "../")
from picostore import PicoStore


#Clear

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


def testSimpleClear():
    PicoStoreInstance = PicoStore()
    successCounter = Counter()
    failCounter = Counter()
    collection =  {
        'customers' : {
                'searchFields' : {'name': 'string', 'age': 'integer'}
        }
    } 
    data = [
        {'name': 'Matsuura', 'age': 1},
        {'name': 'Nobuyuki', 'age': 2},
        {'name': 'Saito', 'age': 3}
    ] 

    def fail(err):
        failCounter.tick()
        print 'Failed with ' + err 

    def successFindAll2(res):
        assert_equals(len(res), 0)
        successCounter.tick()

    def successClear(res):
        assert_equals(res, 0)
        successCounter.tick()
        PicoStoreInstance.get('customers').findAll().then(lambda res: successFindAll2(res), lambda err: fail(err))


    def successFindAll1(res):
        assert_equals(len(res), 3)
        successCounter.tick()
        assert_equals(res[0]['_json']['name'], 'Matsuura')
        successCounter.tick()
        assert_equals(res[0]['_json']['age'], 1)
        successCounter.tick()
        assert_equals(res[1]['_json']['name'], 'Nobuyuki')
        successCounter.tick()
        assert_equals(res[1]['_json']['age'], 2)
        successCounter.tick()
        assert_equals(res[2]['_json']['name'], 'Saito')
        successCounter.tick()
        assert_equals(res[2]['_json']['age'], 3)
        successCounter.tick()
        PicoStoreInstance.get('customers').clear().then(lambda res: successClear(res), lambda err: fail(err))


    def successAdd1(res):
        assert_equals(res, 3)
        successCounter.tick()
        PicoStoreInstance.get('customers').findAll().then(lambda res: successFindAll1(res), lambda err: fail(err))


    def successInit(res):
        assert_equals(res['customers'].name, 'customers')
        successCounter.tick()
        PicoStoreInstance.get('customers').add(data).then(lambda res: successAdd1(res), lambda err: fail(err))

    def successDestroy(res):
        assert_equals(res, 0)
        successCounter.tick()
        PicoStoreInstance.init(collection).then(lambda res: successInit(res), lambda err: fail(err))


    PicoStoreInstance.destroy().then(lambda res: successDestroy(res), lambda err: fail(err))
    assert_equals(12, successCounter.value())
    assert_equals(0, failCounter.value())


def testClearWithMultipleCollections():
    PicoStoreInstance = PicoStore()
    successCounter = Counter()
    failCounter = Counter()
    collection1 =  {
        'customers' : {
                'searchFields' : {'name': 'string', 'age': 'integer'}
        }
    } 

    collection2 = {
        'orders': {
            'searchFields': {'name': 'string', 'id': 'integer'}
        }
    }

    data1 = [
        {'name': 'Matsuura', 'age': 1},
        {'name': 'Nobuyuki', 'age': 2},
        {'name': 'Saito', 'age': 3}
    ] 

    data2 = [
        {'name': 'order1', 'id': 1},
        {'name': 'order2', 'id': 2},
        {'name': 'order3', 'id': 3},

    ]

    def fail(err):
        failCounter.tick()
        print 'Failed with ' + err 

    def successFindAll4(res):
        assert_equals(len(res), 0)
        successCounter.tick()
       

    def successClear2(res):
        assert_equals(res, 0)
        successCounter.tick()
        PicoStoreInstance.get('orders').findAll().then(lambda res: successFindAll4(res), lambda err: fail(err))



    def successFindAll3(res):
        assert_equals(len(res), 3)
        successCounter.tick()
        assert_equals(res[0]['_json']['name'], 'order1')
        successCounter.tick()
        assert_equals(res[0]['_json']['id'], 1)
        successCounter.tick()
        assert_equals(res[1]['_json']['name'], 'order2')
        successCounter.tick()
        assert_equals(res[1]['_json']['id'], 2)
        successCounter.tick()
        assert_equals(res[2]['_json']['name'], 'order3')
        successCounter.tick()
        assert_equals(res[2]['_json']['id'], 3)
        successCounter.tick()
        PicoStoreInstance.get('orders').clear().then(lambda res: successClear2(res), lambda err: fail(err))



    def successAdd2(res):
        assert_equals(res, 3)
        successCounter.tick()
        PicoStoreInstance.get('orders').findAll().then(lambda res: successFindAll3(res), lambda err: fail(err))

    def successInit2(res):
        assert_equals(res['orders'].name, 'orders')
        successCounter.tick()
        PicoStoreInstance.get('orders').add(data2).then(lambda res: successAdd2(res), lambda err: fail(err))


    def successFindAll2(res):
        assert_equals(len(res), 0)
        successCounter.tick()
        PicoStoreInstance.init(collection2).then(lambda res: successInit2(res), lambda err: fail(err))

    def successClear1(res):
        assert_equals(res, 0)
        successCounter.tick()
        PicoStoreInstance.get('customers').findAll().then(lambda res: successFindAll2(res), lambda err: fail(err))


    def successFindAll1(res):
        assert_equals(len(res), 3)
        successCounter.tick()
        assert_equals(res[0]['_json']['name'], 'Matsuura')
        successCounter.tick()
        assert_equals(res[0]['_json']['age'], 1)
        successCounter.tick()
        assert_equals(res[1]['_json']['name'], 'Nobuyuki')
        successCounter.tick()
        assert_equals(res[1]['_json']['age'], 2)
        successCounter.tick()
        assert_equals(res[2]['_json']['name'], 'Saito')
        successCounter.tick()
        assert_equals(res[2]['_json']['age'], 3)
        successCounter.tick()
        PicoStoreInstance.get('customers').clear().then(lambda res: successClear1(res), lambda err: fail(err))


    def successAdd1(res):
        assert_equals(res, 3)
        successCounter.tick()
        PicoStoreInstance.get('customers').findAll().then(lambda res: successFindAll1(res), lambda err: fail(err))


    def successInit1(res):
        assert_equals(res['customers'].name, 'customers')
        successCounter.tick()
        PicoStoreInstance.get('customers').add(data1).then(lambda res: successAdd1(res), lambda err: fail(err))

    def successDestroy(res):
        assert_equals(res, 0)
        successCounter.tick()
        PicoStoreInstance.init(collection1).then(lambda res: successInit1(res), lambda err: fail(err))


    PicoStoreInstance.destroy().then(lambda res: successDestroy(res), lambda err: fail(err))
    assert_equals(23, successCounter.value())
    assert_equals(0, failCounter.value())


def testClearWithClosedCollection():
    PicoStoreInstance = PicoStore()
    successCounter = Counter()
    failCounter = Counter()
    collection =  {
        'customers' : {
                'searchFields' : {'name': 'string', 'age': 'integer'}
        }
    }  

    def fail(err):
        failCounter.tick()
        print 'Failed with ' + err  

    def successClear(res):
        assert_equals(res, 0)
        successCounter.tick()   

    def successCloseAll(res):
        assert_equals(res, 0)
        successCounter.tick()
        accessor.clear().then(lambda res: successClear(res), lambda err: fail(err))

    def successInit(res):
        assert_equals(res['customers'].name, 'customers')
        successCounter.tick()
        global accessor
        accessor = res['customers']
        PicoStoreInstance.closeAll().then(lambda res: successCloseAll(res), lambda err: fail(err))

    def successDestroy(res):
        assert_equals(res, 0)
        successCounter.tick()
        PicoStoreInstance.init(collection).then(lambda res: successInit(res), lambda err: fail(err))


    PicoStoreInstance.destroy().then(lambda res: successDestroy(res), lambda err: fail(err))
    assert_equals(3, successCounter.value())
    assert_equals(1, failCounter.value())

def testAddDataAfterClear():
    PicoStoreInstance = PicoStore()
    successCounter = Counter()
    failCounter = Counter()
    collection =  {
        'customers' : {
                'searchFields' : {'name': 'string', 'age': 'integer'}
        }
    } 
    data = [
        {'name': 'Matsuura', 'age': 1},
        {'name': 'Nobuyuki', 'age': 2},
        {'name': 'Saito', 'age': 3}
    ] 

    newData = [
        {'name': 'Shita', 'age': 1},
        {'name': 'Rirakkusu', 'age': 2},
        {'name': 'Junko', 'age': 3}
    ]

    def fail(err):
        failCounter.tick()
        print 'Failed with ' + err 

    def successFindAll2(res):
        assert_equals(len(res), 3)
        successCounter.tick()
        assert_equals(res[0]['_json']['name'], 'Shita')
        successCounter.tick()
        assert_equals(res[0]['_json']['age'], 1)
        successCounter.tick()
        assert_equals(res[1]['_json']['name'], 'Rirakkusu')
        successCounter.tick()
        assert_equals(res[1]['_json']['age'], 2)
        successCounter.tick()
        assert_equals(res[2]['_json']['name'], 'Junko')
        successCounter.tick()
        assert_equals(res[2]['_json']['age'], 3)
        successCounter.tick() 

    def successAdd2(res):
        assert_equals(res, 3)
        successCounter.tick()
        PicoStoreInstance.get('customers').findAll().then(lambda res: successFindAll2(res), lambda err: fail(err))

    def successClear(res):
        assert_equals(res, 0)
        successCounter.tick()
        PicoStoreInstance.get('customers').add(newData).then(lambda res: successAdd2(res), lambda err: fail(err))


    def successFindAll1(res):
        assert_equals(len(res), 3)
        successCounter.tick()
        assert_equals(res[0]['_json']['name'], 'Matsuura')
        successCounter.tick()
        assert_equals(res[0]['_json']['age'], 1)
        successCounter.tick()
        assert_equals(res[1]['_json']['name'], 'Nobuyuki')
        successCounter.tick()
        assert_equals(res[1]['_json']['age'], 2)
        successCounter.tick()
        assert_equals(res[2]['_json']['name'], 'Saito')
        successCounter.tick()
        assert_equals(res[2]['_json']['age'], 3)
        successCounter.tick()
        PicoStoreInstance.get('customers').clear().then(lambda res: successClear(res), lambda err: fail(err))


    def successAdd1(res):
        assert_equals(res, 3)
        successCounter.tick()
        PicoStoreInstance.get('customers').findAll().then(lambda res: successFindAll1(res), lambda err: fail(err))


    def successInit(res):
        assert_equals(res['customers'].name, 'customers')
        successCounter.tick()
        PicoStoreInstance.get('customers').add(data).then(lambda res: successAdd1(res), lambda err: fail(err))

    def successDestroy(res):
        assert_equals(res, 0)
        successCounter.tick()
        PicoStoreInstance.init(collection).then(lambda res: successInit(res), lambda err: fail(err))


    PicoStoreInstance.destroy().then(lambda res: successDestroy(res), lambda err: fail(err))
    assert_equals(19, successCounter.value())
    assert_equals(0, failCounter.value())

