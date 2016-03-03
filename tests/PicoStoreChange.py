from nose.tools import *    
import pdb
import sys
sys.path.insert(0, "../")
from picostore import PicoStore


#Change

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



def testSimpleChange():
    PicoStoreInstance = PicoStore()
    successCounter = Counter()
    failCounter = Counter()
    collection =  {
        'customers' : {
                'searchFields' : {'fn' : 'string', 'ln': 'string', 'age': 'integer'}
        }
    }

    data = [{'fn': 'Ayumu', 'ln': 'Kogami', 'age': 1}, {'fn': 'Rirakkusu', 'ln': 'Shita' ,'age': 2}, {'fn': 'Harupia', 'ln': 'Sunaku', 'age': 3}]

    newData = [
        {'fn': 'Ayumu', 'ln': 'Kogami', 'age': 1},
        {'fn': 'Rirakkusu', 'ln': 'SHITA', 'age': 2},
        {'fn': 'SHIN', 'ln': 'HAYATA', 'age': 3},
        {'fn': 'Harupia', 'ln': 'SAND', 'age': 4}
    ]

    changeOptions = {'addNew': True, 'markDirty': True, 'replaceCriteria': ['age']}
    

    def fail(err):
        failCounter.tick()
        print 'Failed with ' + err

    def successFind2(res):
        assert_equals(len(res), 4)
        successCounter.tick()
        assert_equals(res[0]['_json']['fn'], 'Ayumu')
        successCounter.tick()
        assert_equals(res[0]['_json']['ln'], 'Kogami')
        successCounter.tick()
        assert_equals(res[0]['_json']['age'], 1)
        successCounter.tick()
        assert_equals(res[1]['_json']['fn'], 'Rirakkusu')
        successCounter.tick()
        assert_equals(res[1]['_json']['ln'], 'SHITA')
        successCounter.tick()
        assert_equals(res[1]['_json']['age'], 2)
        successCounter.tick()
        assert_equals(res[2]['_json']['fn'], 'SHIN')
        successCounter.tick()
        assert_equals(res[2]['_json']['ln'], 'HAYATA')
        successCounter.tick()
        assert_equals(res[2]['_json']['age'], 3)
        successCounter.tick()
        assert_equals(res[3]['_json']['fn'], 'Harupia')
        successCounter.tick()
        assert_equals(res[3]['_json']['ln'], 'SAND')
        successCounter.tick()
        assert_equals(res[3]['_json']['age'], 4)
        successCounter.tick()


    def successChange(res):
        assert_equals(res, 4)
        successCounter.tick()
        PicoStoreInstance.get('customers').findAll().then(lambda res: successFind2(res), lambda err: fail(err))

    def successFind1(res):
        assert_equals(len(res), 3)
        successCounter.tick()
        assert_equals(res[0]['_json']['fn'], 'Ayumu')
        successCounter.tick()
        assert_equals(res[0]['_json']['ln'], 'Kogami')
        successCounter.tick()
        assert_equals(res[0]['_json']['age'], 1)
        successCounter.tick()
        assert_equals(res[1]['_json']['fn'], 'Rirakkusu')
        successCounter.tick()
        assert_equals(res[1]['_json']['ln'], 'Shita')
        successCounter.tick()
        assert_equals(res[1]['_json']['age'], 2)
        successCounter.tick()
        assert_equals(res[2]['_json']['fn'], 'Harupia')
        successCounter.tick()
        assert_equals(res[2]['_json']['ln'], 'Sunaku')
        successCounter.tick()
        assert_equals(res[2]['_json']['age'], 3)
        PicoStoreInstance.get('customers').change(newData, changeOptions).then(lambda res: successChange(res), lambda err: fail(err))


    def successAdd(res):
        assert_equals(res, 3)
        successCounter.tick()
        PicoStoreInstance.get('customers').findAll().then(lambda res: successFind1(res), lambda err: fail(err))
        

    def successInit(res):
        assert_equals(res['customers'].name, 'customers')
        successCounter.tick()
        PicoStoreInstance.get('customers').add(data).then(lambda res: successAdd(res), lambda err: fail(err))


    def successDestroy(res):
        assert_equals(res, 0)
        successCounter.tick()
        PicoStoreInstance.init(collection).then(lambda res: successInit(res), lambda err: fail(err))


    PicoStoreInstance.destroy().then(lambda res: successDestroy(res), lambda err: fail(err))
    assert_equals(26, successCounter.value())
    assert_equals(0, failCounter.value())

# def testChaneWithMultipleCriteria():
#     PicoStoreInstance = PicoStore()
#     successCounter = Counter()
#     failCounter = Counter()
#     collection =  {
#         'customers' : {
#                 'searchFields' : {'id' : 'integer', 'ssn': 'string', 'name': 'string'}
#         }
#     }

#     data = [{'id': 0, 'ssn': '111-22-333', 'name': 'Akiyama'}, {'id': 1, 'ssn': '111-33-444', 'name': 'Hashigaki'}, {'id': 2, 'ssn': '111-55-666', 'name': 'Mochizuki'}]

#     newData = [
#         {'id': 0, 'name': 'YOLO', 'ssn': '111-22-333'},
#         {'id': 1, 'name': 'Rirakkusu', 'ssn': '111-33-444'},
#         {'id': 2, 'name': 'SHIN', 'ssn': '111-55-666'}
#     ]

#     changeOptions = {'markDirty': True, 'replaceCriteria': ['id', 'ssn']}
    

#     def fail(err):
#         failCounter.tick()
#         print 'Failed with ' + err

#     def successFind2(res):
#         assert_equals(len(res), 3)
#         successCounter.tick()
#         assert_equals(res[0]['_json']['id'], 0)
#         successCounter.tick()
#         assert_equals(res[0]['_json']['ssn'], '111-22-333')
#         successCounter.tick()
#         assert_equals(res[0]['_json']['name'], 'YOLO')
#         successCounter.tick()
#         assert_equals(res[1]['_json']['id'], 1)
#         successCounter.tick()
#         assert_equals(res[1]['_json']['ssn'], '111-33-444')
#         successCounter.tick()
#         assert_equals(res[1]['_json']['name'], 'Rirakkusu')
#         successCounter.tick()
#         assert_equals(res[2]['_json']['id'], 2)
#         successCounter.tick()
#         assert_equals(res[2]['_json']['ssn'], '111-55-666')
#         successCounter.tick()
#         assert_equals(res[2]['_json']['name'], 'SHIN')
#         successCounter.tick()


#     def successChange(res):
#         assert_equals(res, 3)
#         successCounter.tick()
#         PicoStoreInstance.get('customers').findAll().then(lambda res: successFind2(res), lambda err: fail(err))

#     def successFind1(res):
#         assert_equals(len(res), 3)
#         successCounter.tick()
#         assert_equals(res[0]['_json']['id'], 0)
#         successCounter.tick()
#         assert_equals(res[0]['_json']['ssn'], '111-22-333')
#         successCounter.tick()
#         assert_equals(res[0]['_json']['name'], 'Akiyama')
#         successCounter.tick()
#         assert_equals(res[1]['_json']['id'], 1)
#         successCounter.tick()
#         assert_equals(res[1]['_json']['ssn'], '111-33-444')
#         successCounter.tick()
#         assert_equals(res[1]['_json']['name'], 'Hashigaki')
#         successCounter.tick()
#         assert_equals(res[2]['_json']['id'], 2)
#         successCounter.tick()
#         assert_equals(res[2]['_json']['ssn'], '111-55-666')
#         successCounter.tick()
#         assert_equals(res[2]['_json']['name'], 'Mochizuki')
#         PicoStoreInstance.get('customers').change(newData, changeOptions).then(lambda res: successChange(res), lambda err: fail(err))


#     def successAdd(res):
#         assert_equals(res, 3)
#         successCounter.tick()
#         PicoStoreInstance.get('customers').findAll().then(lambda res: successFind1(res), lambda err: fail(err))
        

#     def successInit(res):
#         assert_equals(res['customers'].name, 'customers')
#         successCounter.tick()
#         PicoStoreInstance.get('customers').add(data).then(lambda res: successAdd(res), lambda err: fail(err))


#     def successDestroy(res):
#         assert_equals(res, 0)
#         successCounter.tick()
#         PicoStoreInstance.init(collection).then(lambda res: successInit(res), lambda err: fail(err))


#     PicoStoreInstance.destroy().then(lambda res: successDestroy(res), lambda err: fail(err))
#     assert_equals(23, successCounter.value())
#     assert_equals(0, failCounter.value())

# def testUseChangeToAdd():
#     PicoStoreInstance = PicoStore()
#     successCounter = Counter()
#     failCounter = Counter()
#     collection =  {
#         'customers' : {
#                 'searchFields' : {'fn' : 'string', 'ln': 'string', 'age': 'integer'}
#         }
#     }

#     data = [{'fn': 'Ayumu', 'ln': 'Kogami', 'age': 1}, {'fn': 'Rirakkusu', 'ln': 'Shita' ,'age': 2}, {'fn': 'Harupia', 'ln': 'Sunaku', 'age': 3}]

#     newData = [
#         {'fn': 'Ayumu', 'ln': 'Kogami', 'age': 1},
#         {'fn': 'Rirakkusu', 'ln': 'SHITA', 'age': 2},
#         {'fn': 'SHIN', 'ln': 'HAYATA', 'age': 3},
#         {'fn': 'Harupia', 'ln': 'SAND', 'age': 4}
#     ]

#     changeOptions = {'addNew': True, 'replaceCriteria': ['age']}
    

#     def fail(err):
#         failCounter.tick()
#         print 'Failed with ' + err

#     def successFind1(res):
#         assert_equals(len(res), 3)
#         successCounter.tick()
#         assert_equals(res[0]['_json']['fn'], 'Ayumu')
#         successCounter.tick()
#         assert_equals(res[0]['_json']['ln'], 'Kogami')
#         successCounter.tick()
#         assert_equals(res[0]['_json']['age'], 1)
#         successCounter.tick()
#         assert_equals(res[1]['_json']['fn'], 'Rirakkusu')
#         successCounter.tick()
#         assert_equals(res[1]['_json']['ln'], 'Shita')
#         successCounter.tick()
#         assert_equals(res[1]['_json']['age'], 2)
#         successCounter.tick()
#         assert_equals(res[2]['_json']['fn'], 'Harupia')
#         successCounter.tick()
#         assert_equals(res[2]['_json']['ln'], 'Sunaku')
#         successCounter.tick()
#         assert_equals(res[2]['_json']['age'], 3)

#     def successAdd(res):
#         assert_equals(res, 3)
#         successCounter.tick()
#         PicoStoreInstance.get('customers').findAll().then(lambda res: successFind1(res), lambda err: fail(err))
        

#     def successInit(res):
#         assert_equals(res['customers'].name, 'customers')
#         successCounter.tick()
#         PicoStoreInstance.get('customers').change(data, changeOptions).then(lambda res: successAdd(res), lambda err: fail(err))


#     def successDestroy(res):
#         assert_equals(res, 0)
#         successCounter.tick()
#         PicoStoreInstance.init(collection).then(lambda res: successInit(res), lambda err: fail(err))


#     PicoStoreInstance.destroy().then(lambda res: successDestroy(res), lambda err: fail(err))
#     assert_equals(12, successCounter.value())
#     assert_equals(0, failCounter.value())

# def testAddNewFalse():
#     PicoStoreInstance = PicoStore()
#     successCounter = Counter()
#     failCounter = Counter()
#     collection =  {
#         'customers' : {
#                 'searchFields' : {'fn' : 'string', 'ln': 'string', 'age': 'integer'}
#         }
#     }

#     data = [{'fn': 'Ayumu', 'ln': 'Kogami', 'age': 1}, {'fn': 'Rirakkusu', 'ln': 'Shita' ,'age': 2}, {'fn': 'Harupia', 'ln': 'Sunaku', 'age': 3}]

#     newData = [
#         {'fn': 'Ayumu', 'ln': 'Kogami', 'age': 1},
#         {'fn': 'Rirakkusu', 'ln': 'SHITA', 'age': 2},
#         {'fn': 'SHIN', 'ln': 'HAYATA', 'age': 3},
#         {'fn': 'Harupia', 'ln': 'SAND', 'age': 4}
#     ]

#     changeOptions = {'addNew': False,'replaceCriteria': ['age']}
    

#     def fail(err):
#         failCounter.tick()
#         print 'Failed with ' + err

#     def successFind1(res):
#         assert_equals(len(res), 0)
#         successCounter.tick()


#     def successAdd(res):
#         assert_equals(res, 0)
#         successCounter.tick()
#         PicoStoreInstance.get('customers').findAll().then(lambda res: successFind1(res), lambda err: fail(err))
        

#     def successInit(res):
#         assert_equals(res['customers'].name, 'customers')
#         successCounter.tick()
#         PicoStoreInstance.get('customers').change(data, changeOptions).then(lambda res: successAdd(res), lambda err: fail(err))


#     def successDestroy(res):
#         assert_equals(res, 0)
#         successCounter.tick()
#         PicoStoreInstance.init(collection).then(lambda res: successInit(res), lambda err: fail(err))


#     PicoStoreInstance.destroy().then(lambda res: successDestroy(res), lambda err: fail(err))
#     assert_equals(0, failCounter.value())
#     assert_equals(4, successCounter.value())


# def testImplictAddNewFalse():
#     PicoStoreInstance = PicoStore()
#     successCounter = Counter()
#     failCounter = Counter()
#     collection =  {
#         'customers' : {
#                 'searchFields' : {'fn' : 'string', 'ln': 'string', 'age': 'integer'}
#         }
#     }

#     data = [{'fn': 'Ayumu', 'ln': 'Kogami', 'age': 1}, {'fn': 'Rirakkusu', 'ln': 'Shita' ,'age': 2}, {'fn': 'Harupia', 'ln': 'Sunaku', 'age': 3}]

#     newData = [
#         {'fn': 'Ayumu', 'ln': 'Kogami', 'age': 1},
#         {'fn': 'Rirakkusu', 'ln': 'SHITA', 'age': 2},
#         {'fn': 'SHIN', 'ln': 'HAYATA', 'age': 3},
#         {'fn': 'Harupia', 'ln': 'SAND', 'age': 4}
#     ]

#     changeOptions = {'replaceCriteria': ['age']}
    

#     def fail(err):
#         failCounter.tick()
#         print 'Failed with ' + err

#     def successFind1(res):
#         assert_equals(len(res), 0)
#         successCounter.tick()


#     def successAdd(res):
#         assert_equals(res, 0)
#         successCounter.tick()
#         PicoStoreInstance.get('customers').findAll().then(lambda res: successFind1(res), lambda err: fail(err))
        

#     def successInit(res):
#         assert_equals(res['customers'].name, 'customers')
#         successCounter.tick()
#         PicoStoreInstance.get('customers').change(data, changeOptions).then(lambda res: successAdd(res), lambda err: fail(err))


#     def successDestroy(res):
#         assert_equals(res, 0)
#         successCounter.tick()
#         PicoStoreInstance.init(collection).then(lambda res: successInit(res), lambda err: fail(err))


#     PicoStoreInstance.destroy().then(lambda res: successDestroy(res), lambda err: fail(err))
#     assert_equals(0, failCounter.value())
#     assert_equals(4, successCounter.value())


# def testChangeWithEmptyArray():
#     PicoStoreInstance = PicoStore()
#     successCounter = Counter()
#     failCounter = Counter()
#     collection =  {
#         'customers' : {
#                 'searchFields' : {'fn' : 'string', 'ln': 'string', 'age': 'integer'}
#         }
#     }

#     data = [{'fn': 'Ayumu', 'ln': 'Kogami', 'age': 1}, {'fn': 'Rirakkusu', 'ln': 'Shita' ,'age': 2}, {'fn': 'Harupia', 'ln': 'Sunaku', 'age': 3}]

#     newData = [
#         {'fn': 'Ayumu', 'ln': 'Kogami', 'age': 1},
#         {'fn': 'Rirakkusu', 'ln': 'SHITA', 'age': 2},
#         {'fn': 'SHIN', 'ln': 'HAYATA', 'age': 3},
#         {'fn': 'Harupia', 'ln': 'SAND', 'age': 4}
#     ]

#     changeOptions = {'addNew': False, 'replaceCriteria': ['age']}
    

#     def fail(err):
#         failCounter.tick()
#         print 'Failed with ' + err

#     def successFind2(res):
#         assert_equals(len(res), 3)
#         successCounter.tick()
#         assert_equals(res[0]['_json']['fn'], 'Ayumu')
#         successCounter.tick()
#         assert_equals(res[0]['_json']['ln'], 'Kogami')
#         successCounter.tick()
#         assert_equals(res[0]['_json']['age'], 1)
#         successCounter.tick()
#         assert_equals(res[1]['_json']['fn'], 'Rirakkusu')
#         successCounter.tick()
#         assert_equals(res[1]['_json']['ln'], 'Shita')
#         successCounter.tick()
#         assert_equals(res[1]['_json']['age'], 2)
#         successCounter.tick()
#         assert_equals(res[2]['_json']['fn'], 'Harupia')
#         successCounter.tick()
#         assert_equals(res[2]['_json']['ln'], 'Sunaku')
#         successCounter.tick()
#         assert_equals(res[2]['_json']['age'], 3)


#     def successChange(res):
#         assert_equals(res, 0)
#         successCounter.tick()
#         PicoStoreInstance.get('customers').findAll().then(lambda res: successFind2(res), lambda err: fail(err))

#     def successFind1(res):
#         assert_equals(len(res), 3)
#         successCounter.tick()
#         assert_equals(res[0]['_json']['fn'], 'Ayumu')
#         successCounter.tick()
#         assert_equals(res[0]['_json']['ln'], 'Kogami')
#         successCounter.tick()
#         assert_equals(res[0]['_json']['age'], 1)
#         successCounter.tick()
#         assert_equals(res[1]['_json']['fn'], 'Rirakkusu')
#         successCounter.tick()
#         assert_equals(res[1]['_json']['ln'], 'Shita')
#         successCounter.tick()
#         assert_equals(res[1]['_json']['age'], 2)
#         successCounter.tick()
#         assert_equals(res[2]['_json']['fn'], 'Harupia')
#         successCounter.tick()
#         assert_equals(res[2]['_json']['ln'], 'Sunaku')
#         successCounter.tick()
#         assert_equals(res[2]['_json']['age'], 3)
#         PicoStoreInstance.get('customers').change([], changeOptions).then(lambda res: successChange(res), lambda err: fail(err))


#     def successAdd(res):
#         assert_equals(res, 3)
#         successCounter.tick()
#         PicoStoreInstance.get('customers').findAll().then(lambda res: successFind1(res), lambda err: fail(err))
        

#     def successInit(res):
#         assert_equals(res['customers'].name, 'customers')
#         successCounter.tick()
#         PicoStoreInstance.get('customers').add(data).then(lambda res: successAdd(res), lambda err: fail(err))


#     def successDestroy(res):
#         assert_equals(res, 0)
#         successCounter.tick()
#         PicoStoreInstance.init(collection).then(lambda res: successInit(res), lambda err: fail(err))


#     PicoStoreInstance.destroy().then(lambda res: successDestroy(res), lambda err: fail(err))
#     assert_equals(22, successCounter.value())
#     assert_equals(0, failCounter.value())

# def testWithNoReplaceCriteriaAndAddNewFalse():
#     PicoStoreInstance = PicoStore()
#     successCounter = Counter()
#     failCounter = Counter()
#     collection =  {
#         'customers' : {
#                 'searchFields' : {'fn' : 'string', 'ln': 'string', 'age': 'integer'}
#         }
#     }

#     data = [{'fn': 'Ayumu', 'ln': 'Kogami', 'age': 1}, {'fn': 'Rirakkusu', 'ln': 'Shita' ,'age': 2}, {'fn': 'Harupia', 'ln': 'Sunaku', 'age': 3}]

#     newData = [
#         {'fn': 'Ayumu', 'ln': 'Kogami', 'age': 1},
#         {'fn': 'Rirakkusu', 'ln': 'SHITA', 'age': 2},
#         {'fn': 'SHIN', 'ln': 'HAYATA', 'age': 3},
#         {'fn': 'Harupia', 'ln': 'SAND', 'age': 4}
#     ]

#     changeOptions = {'addNew': False}
    

#     def fail(err):
#         failCounter.tick()
#         print 'Failed with ' + err

#     def successFind2(res):
#         assert_equals(len(res), 3)
#         successCounter.tick()
#         assert_equals(res[0]['_json']['fn'], 'Ayumu')
#         successCounter.tick()
#         assert_equals(res[0]['_json']['ln'], 'Kogami')
#         successCounter.tick()
#         assert_equals(res[0]['_json']['age'], 1)
#         successCounter.tick()
#         assert_equals(res[1]['_json']['fn'], 'Rirakkusu')
#         successCounter.tick()
#         assert_equals(res[1]['_json']['ln'], 'Shita')
#         successCounter.tick()
#         assert_equals(res[1]['_json']['age'], 2)
#         successCounter.tick()
#         assert_equals(res[2]['_json']['fn'], 'Harupia')
#         successCounter.tick()
#         assert_equals(res[2]['_json']['ln'], 'Sunaku')
#         successCounter.tick()
#         assert_equals(res[2]['_json']['age'], 3)


#     def successChange(res):
#         assert_equals(res, 0)
#         successCounter.tick()
#         PicoStoreInstance.get('customers').findAll().then(lambda res: successFind2(res), lambda err: fail(err))

#     def successFind1(res):
#         assert_equals(len(res), 3)
#         successCounter.tick()
#         assert_equals(res[0]['_json']['fn'], 'Ayumu')
#         successCounter.tick()
#         assert_equals(res[0]['_json']['ln'], 'Kogami')
#         successCounter.tick()
#         assert_equals(res[0]['_json']['age'], 1)
#         successCounter.tick()
#         assert_equals(res[1]['_json']['fn'], 'Rirakkusu')
#         successCounter.tick()
#         assert_equals(res[1]['_json']['ln'], 'Shita')
#         successCounter.tick()
#         assert_equals(res[1]['_json']['age'], 2)
#         successCounter.tick()
#         assert_equals(res[2]['_json']['fn'], 'Harupia')
#         successCounter.tick()
#         assert_equals(res[2]['_json']['ln'], 'Sunaku')
#         successCounter.tick()
#         assert_equals(res[2]['_json']['age'], 3)
#         PicoStoreInstance.get('customers').change(newData, changeOptions).then(lambda res: successChange(res), lambda err: fail(err))


#     def successAdd(res):
#         assert_equals(res, 3)
#         successCounter.tick()
#         PicoStoreInstance.get('customers').findAll().then(lambda res: successFind1(res), lambda err: fail(err))
        

#     def successInit(res):
#         assert_equals(res['customers'].name, 'customers')
#         successCounter.tick()
#         PicoStoreInstance.get('customers').add(data).then(lambda res: successAdd(res), lambda err: fail(err))


#     def successDestroy(res):
#         assert_equals(res, 0)
#         successCounter.tick()
#         PicoStoreInstance.init(collection).then(lambda res: successInit(res), lambda err: fail(err))


#     PicoStoreInstance.destroy().then(lambda res: successDestroy(res), lambda err: fail(err))
#     assert_equals(22, successCounter.value())
#     assert_equals(0, failCounter.value())  

# def testWithNoReplaceCriteriaAndAddNewTrue():
#     PicoStoreInstance = PicoStore()
#     successCounter = Counter()
#     failCounter = Counter()
#     collection =  {
#         'customers' : {
#                 'searchFields' : {'fn' : 'string', 'ln': 'string', 'age': 'integer'}
#         }
#     }

#     data = [{'fn': 'Ayumu', 'ln': 'Kogami', 'age': 1}, {'fn': 'Rirakkusu', 'ln': 'Shita' ,'age': 2}, {'fn': 'Harupia', 'ln': 'Sunaku', 'age': 3}]

#     newData = [
#         {'fn': 'Kuro', 'ln': 'Toraono', 'age': 4}
#     ]


#     changeOptions = {'addNew': True}
    

#     def fail(err):
#         failCounter.tick()
#         print 'Failed with ' + err

#     def successFind2(res):
#         assert_equals(len(res), 4)
#         successCounter.tick()
#         assert_equals(res[0]['_json']['fn'], 'Ayumu')
#         successCounter.tick()
#         assert_equals(res[0]['_json']['ln'], 'Kogami')
#         successCounter.tick()
#         assert_equals(res[0]['_json']['age'], 1)
#         successCounter.tick()
#         assert_equals(res[1]['_json']['fn'], 'Rirakkusu')
#         successCounter.tick()
#         assert_equals(res[1]['_json']['ln'], 'Shita')
#         successCounter.tick()
#         assert_equals(res[1]['_json']['age'], 2)
#         successCounter.tick()
#         assert_equals(res[2]['_json']['fn'], 'Harupia')
#         successCounter.tick()
#         assert_equals(res[2]['_json']['ln'], 'Sunaku')
#         successCounter.tick()
#         assert_equals(res[2]['_json']['age'], 3)
#         successCounter.tick()
#         assert_equals(res[2]['_json']['fn'], 'Kuro')
#         successCounter.tick()
#         assert_equals(res[2]['_json']['ln'], 'Toraono')
#         successCounter.tick()
#         assert_equals(res[2]['_json']['age'], 4)




#     def successChange(res):
#         assert_equals(res, 1)
#         successCounter.tick()
#         PicoStoreInstance.get('customers').findAll().then(lambda res: successFind2(res), lambda err: fail(err))

#     def successFind1(res):
#         assert_equals(len(res), 3)
#         successCounter.tick()
#         assert_equals(res[0]['_json']['fn'], 'Ayumu')
#         successCounter.tick()
#         assert_equals(res[0]['_json']['ln'], 'Kogami')
#         successCounter.tick()
#         assert_equals(res[0]['_json']['age'], 1)
#         successCounter.tick()
#         assert_equals(res[1]['_json']['fn'], 'Rirakkusu')
#         successCounter.tick()
#         assert_equals(res[1]['_json']['ln'], 'Shita')
#         successCounter.tick()
#         assert_equals(res[1]['_json']['age'], 2)
#         successCounter.tick()
#         assert_equals(res[2]['_json']['fn'], 'Harupia')
#         successCounter.tick()
#         assert_equals(res[2]['_json']['ln'], 'Sunaku')
#         successCounter.tick()
#         assert_equals(res[2]['_json']['age'], 3)
#         PicoStoreInstance.get('customers').change(newData, changeOptions).then(lambda res: successChange(res), lambda err: fail(err))


#     def successAdd(res):
#         assert_equals(res, 3)
#         successCounter.tick()
#         PicoStoreInstance.get('customers').findAll().then(lambda res: successFind1(res), lambda err: fail(err))
        

#     def successInit(res):
#         assert_equals(res['customers'].name, 'customers')
#         successCounter.tick()
#         PicoStoreInstance.get('customers').add(data).then(lambda res: successAdd(res), lambda err: fail(err))


#     def successDestroy(res):
#         assert_equals(res, 0)
#         successCounter.tick()
#         PicoStoreInstance.init(collection).then(lambda res: successInit(res), lambda err: fail(err))


#     PicoStoreInstance.destroy().then(lambda res: successDestroy(res), lambda err: fail(err))
#     assert_equals(23, successCounter.value())
#     assert_equals(0, failCounter.value())

def testChangeWithMultipleSameDocs():
    PicoStoreInstance = PicoStore()
    successCounter = Counter()
    failCounter = Counter()
    collection =  {
        'customers' : {
                'searchFields' : {'fn' : 'string', 'ln': 'string', 'age': 'integer'}
        }
    }

    data = [{'fn': 'Ayumu', 'ln': 'Kogami', 'age': 1}, {'fn': 'Rirakkusu', 'ln': 'Shita' ,'age': 1}, {'fn': 'Harupia', 'ln': 'Sunaku', 'age': 2}]

    newData = [
        {'fn': 'Karubin', 'ln': 'Hospital', 'age': 1},
        {'fn': 'Harupia', 'ln': 'Sunaku', 'age': 2}
    ]

    changeOptions = {'replaceCriteria': ['age']}
    

    def fail(err):
        failCounter.tick()
        print 'Failed with ' + err

    def successFind2(res):
        assert_equals(len(res), 3)
        successCounter.tick()
        assert_equals(res[0]['_json']['fn'], 'Karubin')
        successCounter.tick()
        assert_equals(res[0]['_json']['ln'], 'Hospital')
        successCounter.tick()
        assert_equals(res[0]['_json']['age'], 1)
        successCounter.tick()
        assert_equals(res[1]['_json']['fn'], 'Karubin')
        successCounter.tick()
        assert_equals(res[1]['_json']['ln'], 'Hospital')
        successCounter.tick()
        assert_equals(res[1]['_json']['age'], 1)
        successCounter.tick()
        assert_equals(res[2]['_json']['fn'], 'Harupia')
        successCounter.tick()
        assert_equals(res[2]['_json']['ln'], 'Sunaku')
        successCounter.tick()
        assert_equals(res[2]['_json']['age'], 2)
        successCounter.tick()
        

    def successChange(res):
        assert_equals(res, 3)
        successCounter.tick()
        PicoStoreInstance.get('customers').findAll().then(lambda res: successFind2(res), lambda err: fail(err))

    def successFind1(res):
        assert_equals(len(res), 3)
        successCounter.tick()
        assert_equals(res[0]['_json']['fn'], 'Ayumu')
        successCounter.tick()
        assert_equals(res[0]['_json']['ln'], 'Kogami')
        successCounter.tick()
        assert_equals(res[0]['_json']['age'], 1)
        successCounter.tick()
        assert_equals(res[1]['_json']['fn'], 'Rirakkusu')
        successCounter.tick()
        assert_equals(res[1]['_json']['ln'], 'Shita')
        successCounter.tick()
        assert_equals(res[1]['_json']['age'], 1)
        successCounter.tick()
        assert_equals(res[2]['_json']['fn'], 'Harupia')
        successCounter.tick()
        assert_equals(res[2]['_json']['ln'], 'Sunaku')
        successCounter.tick()
        assert_equals(res[2]['_json']['age'], 2)
        successCounter.tick()
        PicoStoreInstance.get('customers').change(newData, changeOptions).then(lambda res: successChange(res), lambda err: fail(err))


    def successAdd(res):
        assert_equals(res, 3)
        successCounter.tick()
        PicoStoreInstance.get('customers').findAll().then(lambda res: successFind1(res), lambda err: fail(err))
        

    def successInit(res):
        assert_equals(res['customers'].name, 'customers')
        successCounter.tick()
        PicoStoreInstance.get('customers').add(data).then(lambda res: successAdd(res), lambda err: fail(err))


    def successDestroy(res):
        assert_equals(res, 0)
        successCounter.tick()
        PicoStoreInstance.init(collection).then(lambda res: successInit(res), lambda err: fail(err))


    PicoStoreInstance.destroy().then(lambda res: successDestroy(res), lambda err: fail(err))
    assert_equals(24, successCounter.value())
    assert_equals(0, failCounter.value())