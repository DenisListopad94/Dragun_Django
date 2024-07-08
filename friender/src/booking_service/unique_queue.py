from .models import Queue

#todo реализация без модели
# class UniqueQueue:
#     def __init__(self) -> None:
#         self.queue = []
#         pass

#     def add(self, elem):
#         if elem not in self.queue:
#             self.queue.append(elem)

#     def get_last(self):
#         if not self.queue:
#             return None
#         else:
#             return self.queue[-1]

#     # позволяет проверить принадлежность объекта
#     def __contains__(self, elem):
#         return elem in self.queue
    
#     def __len__(self):
#         return len(self.queue)

#     def __repr__(self):
#         return f"UniqueQueue: {self.queue}"

# unique_queue = UniqueQueue()

# print('p1: ', unique_queue)

# unique_queue.add(1)
# unique_queue.add(2)
# unique_queue.add(2)
# unique_queue.add(3)
# unique_queue.add(3)
# unique_queue.add(4)
# unique_queue.add(34)

# print('p2: ',unique_queue)

# # __contains__
# print(4 in unique_queue) # True
# print(5 in unique_queue) # False

# # __len__
# print('len: ',len(unique_queue))

# print('get_last: ', unique_queue.get_last())



class UniqueQueue:
    def __init__(self) -> None:
        self.queue = Queue.objects.all()
        pass

    def add(self, elem):
        if not Queue.objects.filter(value=elem).exists():
            Queue.objects.create(value=elem)

    def get_last(self):
        if not self.queue:
            return None
        else:
            return self.queue.order_by('-id').first().value

    def __contains__(self, elem):
        return Queue.objects.filter(value=elem).exists()
    
    def __len__(self):
        return Queue.objects.count()
    
    def __repr__(self):
        return f"UniqueQueue: {list(Queue.objects.values_list('value', flat=True))}"