from nose.tools import *    
import pdb
import sys
sys.path.insert(0, "../")
from picostore import PicoStore


#Replace

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



def testSimpleReplace():
    PicoStoreInstance = PicoStore()
    successCounter = Counter()
    failCounter = Counter()
    collection =  {
        'customers' : {
                'searchFields' : {'fn' : 'string', 'ln': 'string', 'age': 'integer'},
                'additionalSearchFields': {'orderId': 'string'}
        }
    }

    addOptions = {
        'additionalSearchFields': {
            'orderId': '1337'
        }
    }

    data = [{'fn': 'shin', 'ln': 'Hayata', 'age': 1}, {'fn': 'Ii', 'ln': 'Hissori' ,'age': 2}, {'fn': 'Tama', 'ln': 'Mochizuki', 'age': 3}]

    def fail(err):
        failCounter.tick()
        print 'Failed with ' + err

    def successFind2(res):
        assert_equals(len(res), 3)
        successCounter.tick()
        assert_equals(res[0]['_json']['fn'], 'SHIN')
        successCounter.tick()
        assert_equals(res[0]['_json']['ln'], 'HAYATA')
        successCounter.tick()
        assert_equals(res[0]['_json']['age'], 99)
        successCounter.tick()
        assert_equals(res[1]['_json']['fn'], 'Ii')
        successCounter.tick()
        assert_equals(res[1]['_json']['ln'], 'Hissori')
        successCounter.tick()
        assert_equals(res[1]['_json']['age'], 2)
        successCounter.tick()
        assert_equals(res[2]['_json']['fn'], 'Tama')
        successCounter.tick()
        assert_equals(res[2]['_json']['ln'], 'Mochizuki')
        successCounter.tick()
        assert_equals(res[2]['_json']['age'], 3)
        successCounter.tick()


    def successReplace(res):
        assert_equals(res, 1)
        successCounter.tick()
        PicoStoreInstance.get('customers').findAll().then(lambda res: successFind2(res), lambda err: fail(err))

    def successFind1(res):
        assert_equals(len(res), 3)
        successCounter.tick()
        assert_equals(res[0]['_json']['fn'], 'shin')
        successCounter.tick()
        assert_equals(res[0]['_json']['ln'], 'Hayata')
        successCounter.tick()
        assert_equals(res[0]['_json']['age'], 1)
        successCounter.tick()
        assert_equals(res[1]['_json']['fn'], 'Ii')
        successCounter.tick()
        assert_equals(res[1]['_json']['ln'], 'Hissori')
        successCounter.tick()
        assert_equals(res[1]['_json']['age'], 2)
        successCounter.tick()
        assert_equals(res[2]['_json']['fn'], 'Tama')
        successCounter.tick()
        assert_equals(res[2]['_json']['ln'], 'Mochizuki')
        successCounter.tick()
        assert_equals(res[2]['_json']['age'], 3)
        PicoStoreInstance.get('customers').replace({'_id': 1, '_json': {'fn': 'SHIN', 'ln': 'HAYATA', 'age': 99}}).then(lambda res: successReplace(res), lambda err: fail(err))


    def successAdd(res):
        assert_equals(res, 3)
        successCounter.tick()
        PicoStoreInstance.get('customers').findAll().then(lambda res: successFind1(res), lambda err: fail(err))
        

    def successInit(res):
        assert_equals(res['customers'].name, 'customers')
        successCounter.tick()
        PicoStoreInstance.get('customers').add(data, addOptions).then(lambda res: successAdd(res), lambda err: fail(err))


    def successDestroy(res):
        assert_equals(res, 0)
        successCounter.tick()
        PicoStoreInstance.init(collection).then(lambda res: successInit(res), lambda err: fail(err))


    PicoStoreInstance.destroy().then(lambda res: successDestroy(res), lambda err: fail(err))
    assert_equals(23, successCounter.value())
    assert_equals(0, failCounter.value())

def testAttemptToReplaceWithEmptyArray():
    PicoStoreInstance = PicoStore()
    successCounter = Counter()
    failCounter = Counter()
    collection =  {
        'customers' : {
                'searchFields' : {'fn' : 'string', 'ln': 'string', 'age': 'integer'},
                'additionalSearchFields': {'orderId': 'string'}
        }
    }

    addOptions = {
        'additionalSearchFields': {
            'orderId': '1337'
        }
    }

    data = [{'fn': 'Kitsune', 'ln': 'Shinrya', 'age': 1}, {'fn': 'Jinichi', 'ln': 'Takahashi', 'age': 2}, {'fn': 'Shin', 'ln': 'Kurogane', 'age': 3}]

    def fail(err):
        failCounter.tick()
        print 'Failed with ' + err

    def successReplace(res):
        assert_equals(res,0)
        successCounter.tick()

    def successFind(res):
        assert_equals(len(res), 3)
        successCounter.tick()
        assert_equals(res[0]['_json']['fn'], 'Kitsune')
        successCounter.tick()
        assert_equals(res[0]['_json']['ln'], 'Shinrya')
        successCounter.tick()
        assert_equals(res[0]['_json']['age'], 1)
        successCounter.tick()
        assert_equals(res[1]['_json']['fn'], 'Jinichi')
        successCounter.tick()
        assert_equals(res[1]['_json']['ln'], 'Takahashi')
        successCounter.tick()
        assert_equals(res[1]['_json']['age'], 2)
        successCounter.tick()
        assert_equals(res[2]['_json']['fn'], 'Shin')
        successCounter.tick()
        assert_equals(res[2]['_json']['ln'], 'Kurogane')
        successCounter.tick()
        assert_equals(res[2]['_json']['age'], 3)
        successCounter.tick()
        PicoStore.get('customers').replace([]).then(lambda res: successReplace(res), lambda err: fail(err))
    

    def successAdd(res):
        assert_equals(res, 3)
        successCounter.tick()
        PicoStoreInstance.get('customers').findAll().then(lambda res: successFind(res), lambda err: fail(err))
        

    def successInit(res):
        assert_equals(res['customers'].name, 'customers')
        successCounter.tick()
        PicoStoreInstance.get('customers').add(data, addOptions).then(lambda res: successAdd(res), lambda err: fail(err))


    def successDestroy(res):
        assert_equals(res, 0)
        successCounter.tick()
        PicoStoreInstance.init(collection).then(lambda res: successInit(res), lambda err: fail(err))


    PicoStoreInstance.destroy().then(lambda res: successDestroy(res), lambda err: fail(err))
    assert_equals(13, successCounter.value())
    assert_equals(0, failCounter.value())


def testReplaceAllDocs():
    PicoStoreInstance = PicoStore()
    successCounter = Counter()
    failCounter = Counter()
    collection =  {
        'customers' : {
                'searchFields' : {'fn' : 'string', 'ln': 'string', 'age': 'integer'},
                'additionalSearchFields': {'orderId': 'string'}
        }
    }

    addOptions = {
        'additionalSearchFields': {
            'orderId': '1337'
        }
    }

    data = [{'fn': 'Kitsune', 'ln': 'Shinrya', 'age': 1}, {'fn': 'Jinichi', 'ln': 'Takahashi' ,'age': 2}, {'fn': 'Shin', 'ln': 'Kurogane', 'age': 3}]

    def fail(err):
        failCounter.tick()
        print 'Failed with ' + err

    def successReplace(res):
        assert_equals(res, 3)
        successCounter.tick()
        assert_equals(res[0]['_json']['fn'], 'Kitsune')
        successCounter.tick()
        assert_equals(res[0]['_json']['ln'], 'Shinrya')
        successCounter.tick()
        assert_equals(res[0]['_json']['age'], 10)
        successCounter.tick()
        assert_equals(res[1]['_json']['fn'], 'Jinichi')
        successCounter.tick()
        assert_equals(res[1]['_json']['ln'], 'Takahashi')
        successCounter.tick()
        assert_equals(res[1]['_json']['age'], 20)
        successCounter.tick()
        assert_equals(res[2]['_json']['fn'], 'Shin')
        successCounter.tick()
        assert_equals(res[2]['_json']['ln'], 'Kurogane')
        successCounter.tick()
        assert_equals(res[2]['_json']['age'], 30)

    def successFind(res):
        assert_equals(len(res), 3)
        successCounter.tick()
        assert_equals(res[0]['_json']['fn'], 'Kitsune')
        successCounter.tick()
        assert_equals(res[0]['_json']['ln'], 'Shinrya')
        successCounter.tick()
        assert_equals(res[0]['_json']['age'], 1)
        successCounter.tick()
        assert_equals(res[1]['_json']['fn'], 'Jinichi')
        successCounter.tick()
        assert_equals(res[1]['_json']['ln'], 'Takahashi')
        successCounter.tick()
        assert_equals(res[1]['_json']['age'], 2)
        successCounter.tick()
        assert_equals(res[2]['_json']['fn'], 'Shin')
        successCounter.tick()
        assert_equals(res[2]['_json']['ln'], 'Kurogane')
        successCounter.tick()
        assert_equals(res[2]['_json']['age'], 3)

        for x in range(len(res)):
            res[x]['_json']['age'] = res[x]['_json']['age'] * 10
        PicoStoreInstance.get('customers').replace(res).then(lambda res: successReplace(res), lambda err: fail(err))
    

    def successAdd(res):
        assert_equals(res, 3)
        successCounter.tick()
        PicoStoreInstance.get('customers').findAll().then(lambda res: successFind(res), lambda err: fail(err))
        

    def successInit(res):
        assert_equals(res['customers'].name, 'customers')
        successCounter.tick()
        PicoStoreInstance.get('customers').add(data, addOptions).then(lambda res: successAdd(res), lambda err: fail(err))


    def successDestroy(res):
        assert_equals(res, 0)
        successCounter.tick()
        PicoStoreInstance.init(collection).then(lambda res: successInit(res), lambda err: fail(err))


    PicoStoreInstance.destroy().then(lambda res: successDestroy(res), lambda err: fail(err))
    assert_equals(13, successCounter.value())
    assert_equals(0, failCounter.value())







