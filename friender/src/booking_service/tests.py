import unittest
from django.test import TestCase

from booking_service.unique_queue import UniqueQueue


# todo python3 -m unittest path/file.py
# class TestUniqueQueue(unittest.TestCase):
#     def setUp(self):
#         self.queue = UniqueQueue()

#     def test_add_unique_elements(self):
#         self.queue.add(1)
#         self.queue.add(2)
#         self.queue.add(3)
#         self.assertEqual(len(self.queue), 3)

#     def test_add_duplicate_elements(self):
#         self.queue.add(1)
#         self.queue.add(2)
#         self.queue.add(2)
#         self.assertEqual(len(self.queue), 2)

#     def test_queue_length(self):
#         self.queue.add(1)
#         self.queue.add(2)
#         self.assertEqual(len(self.queue), 2)
#         self.queue.add(3)
#         self.assertEqual(len(self.queue), 3)

#     def test_get_last_elem(self):
#         self.queue.add(1)
#         self.queue.add(2)
#         self.assertEqual(self.queue.get_last(), 2)
#         self.queue.add(3)
#         self.assertEqual(self.queue.get_last(), 3)

#     def test_empty_queue_behaviour(self):
#         self.assertEqual(self.queue.get_last(), None)

# if __name__ == '__main__':
#     unittest.main()


class TestUniqueQueue(TestCase):
    def setUp(self):
        self.queue = UniqueQueue()

    def test_add_unique_elements(self):
        self.queue.add(1)
        self.queue.add(2)
        self.queue.add(3)
        self.assertEqual(len(self.queue), 3)

    def test_add_duplicate_elements(self):
        self.queue.add(1)
        self.queue.add(2)
        self.queue.add(2)
        self.assertEqual(len(self.queue), 2)

    def test_queue_length(self):
        self.queue.add(1)
        self.queue.add(2)
        self.assertEqual(len(self.queue), 2)
        self.queue.add(3)
        self.assertEqual(len(self.queue), 3)

    def test_get_last_elem(self):
        self.queue.add(1)
        self.queue.add(2)
        self.assertEqual(self.queue.get_last(), 2)
        self.queue.add(3)
        self.assertEqual(self.queue.get_last(), 3)

    def test_empty_queue_behaviour(self):
        self.assertEqual(self.queue.get_last(), None)


