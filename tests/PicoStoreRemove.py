from nose.tools import *    
import pdb
import sys
sys.path.insert(0, "../")
from picostore import PicoStore


#Remove

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


def testSimpleRemove():
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

    query = [
        {'equal': [{'name': 'Matsuura'}]}
    ]

    def fail(err):
        failCounter.tick()
        print 'Failed with ' + err 

    def successFindAll2(res):
        assert_equals(len(res), 2)
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
        successCounter.tick()


    def successRemove(res):
        assert_equals(res, 1)
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
        PicoStoreInstance.get('customers').remove(query).then(lambda res: successRemove(res), lambda err: fail(err))


    def successAdd(res):
        assert_equals(res, 3)
        successCounter.tick()
        PicoStoreInstance.get('customers').findAll().then(lambda res: successFindAll1(res), lambda err: fail(err))


    def successInit(res):
        assert_equals(res['customers'].name, 'customers')
        successCounter.tick()
        PicoStoreInstance.get('customers').add(data).then(lambda res: successAdd(res), lambda err: fail(err))

    def successDestroy(res):
        assert_equals(res, 0)
        successCounter.tick()
        PicoStoreInstance.init(collection).then(lambda res: successInit(res), lambda err: fail(err))


    PicoStoreInstance.destroy().then(lambda res: successDestroy(res), lambda err: fail(err))
    assert_equals(12, successCounter.value())
    assert_equals(0, failCounter.value())

def testRemoveWithMultipleSearchFields():
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


    def successFindAll2(res):
        assert_equals(len(res), 4)
        successCounter.tick()
        assert_equals(res[0]['_json']['name'], 'shin')
        successCounter.tick()
        assert_equals(res[0]['_json']['gpa'], 1.0)
        successCounter.tick()
        assert_equals(res[0]['_json']['ssn'], 123)
        successCounter.tick()
        assert_equals(res[0]['_json']['active'], True)
        successCounter.tick()

        assert_equals(res[1]['_json']['name'], 'masao')
        successCounter.tick()
        assert_equals(res[1]['_json']['gpa'], 2.4)
        successCounter.tick()
        assert_equals(res[1]['_json']['ssn'], 345)
        successCounter.tick()
        assert_equals(res[1]['_json']['active'], True)
        successCounter.tick()
        
        assert_equals(res[2]['_json']['name'], 'saito')
        successCounter.tick()
        assert_equals(res[2]['_json']['gpa'], 3.6)
        successCounter.tick()
        assert_equals(res[2]['_json']['ssn'], 789)
        successCounter.tick()
        assert_equals(res[2]['_json']['active'], False)
        successCounter.tick()
        
        assert_equals(res[3]['_json']['name'], 'aiko')
        successCounter.tick()
        assert_equals(res[3]['_json']['gpa'], 4.8)
        successCounter.tick()
        assert_equals(res[3]['_json']['ssn'], 890)
        successCounter.tick()
        assert_equals(res[3]['_json']['active'], True)
        successCounter.tick()

    def successRemove(res):
        assert_equals(res, 1)
        successCounter.tick()
        PicoStoreInstance.get('customers').findAll().then(lambda res: successFindAll2(res), lambda err: fail(err))


    def successFindAll1(res):
        assert_equals(len(res), 5)
        successCounter.tick()
        assert_equals(res[0]['_json']['name'], 'shin')
        successCounter.tick()
        assert_equals(res[0]['_json']['gpa'], 1.0)
        successCounter.tick()
        assert_equals(res[0]['_json']['ssn'], 123)
        successCounter.tick()
        assert_equals(res[0]['_json']['active'], True)
        successCounter.tick()

        assert_equals(res[1]['_json']['name'], 'shu')
        successCounter.tick()
        assert_equals(res[1]['_json']['gpa'], 2.2)
        successCounter.tick()
        assert_equals(res[1]['_json']['ssn'], 345)
        successCounter.tick()
        assert_equals(res[1]['_json']['active'], False)
        successCounter.tick()
        
        assert_equals(res[2]['_json']['name'], 'masao')
        successCounter.tick()
        assert_equals(res[2]['_json']['gpa'], 2.4)
        successCounter.tick()
        assert_equals(res[2]['_json']['ssn'], 567)
        successCounter.tick()
        assert_equals(res[2]['_json']['active'], True)
        successCounter.tick()
        
        assert_equals(res[3]['_json']['name'], 'saito')
        successCounter.tick()
        assert_equals(res[3]['_json']['gpa'], 3.6)
        successCounter.tick()
        assert_equals(res[3]['_json']['ssn'], 789)
        successCounter.tick()
        assert_equals(res[3]['_json']['active'], False)
        successCounter.tick()
        
        assert_equals(res[4]['_json']['name'], 'aiko')
        successCounter.tick()
        assert_equals(res[4]['_json']['gpa'], 4.8)
        successCounter.tick()
        assert_equals(res[4]['_json']['ssn'], 890)
        successCounter.tick()
        assert_equals(res[4]['_json']['active'], True)
        successCounter.tick()
        PicoStoreInstance.get('customers').remove(query).then(lambda res: successRemove(res), lambda err: fail(err))


    def successAdd(res):
        assert_equals(res, 5)
        successCounter.tick()
        PicoStoreInstance.get('customers').findAll().then(lambda res: successFindAll1(res), lambda err: fail(err))

    def successInit(res):
        assert_equals(res['customers'].name, 'customers')
        successCounter.tick()
        PicoStoreInstance.get('customers').add(data).then(lambda res: successAdd(res), lambda err: fail(err))


    def successDestroy(res):
        assert_equals(res, 0)
        successCounter.tick()
        PicoStoreInstance.init(collection).then(lambda res: successInit(res), lambda err: fail(err))


    PicoStoreInstance.destroy().then(lambda res: successDestroy(res), lambda err: fail(err))
    assert_equals(32, successCounter.value())
    assert_equals(0, failCounter.value())





