import unittest

from Queue import Queue
import sys
sys.path.append('../')

import workerpool

class Counter(object):
    "Counter resource used for testing EquippedWorker."
    def __init__(self):
        self.count = 0

class CountJob(workerpool.Job):
    "Job that just increments the count in its resource and append it to the results queue."
    def __init__(self, results):
        self.results = results

    def run(self, toolbox):
        "Append the current count to results and increment."
        self.results.put(toolbox.count)
        toolbox.count += 1

class TestEquippedWorkers(unittest.TestCase):
    def test_equipped(self):
        """
        Created equipped worker that will use an internal Counter resource to
        keep track of the job count.
        """
        results = Queue()
        pool = workerpool.WorkerPool(1, WorkerClass=workerpool.EquippedWorker, workerargs={'toolbox': (Counter, [])})

        # Run 10 jobs
        for i in xrange(10):
            j = CountJob(results)
            pool.put(j)

        # Get 10 results
        for i in xrange(10):
            r = results.get()
            # Each result should be an incremented value
            self.assertEquals(r, i)