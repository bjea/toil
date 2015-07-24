import os
from jobTree.lib.bioio import getTempFile
from jobTree.target import Target as T
from jobTree.test import JobTreeTest
from jobTree.test.src.targetTest import f

class TargetEncapsulationTest(JobTreeTest):
    """
    Tests testing the EncapsulationTarget class
    """
    def testEncapsulation(self):
        """
        Tests the Target.encapsulation method, which uses the EncapsulationTarget 
        class.
        """
        #Temporary file
        outFile = getTempFile(rootDir=os.getcwd())
        #Make a target graph
        a = T.wrapFn(f, "A", outFile)
        b = a.addChildFn(f, a.rv(), outFile)
        c = a.addFollowOnFn(f, b.rv(), outFile)
        #Encapsulate it
        a = a.encapsulate()
        #Now add children/follow to the encapsulated graph
        d = T.wrapFn(f, c.rv(), outFile)
        e = T.wrapFn(f, d.rv(), outFile)
        a.addChild(d)
        a.addFollowOn(e)
        #Create the runner for the workflow.
        options = T.Runner.getDefaultOptions()
        options.logLevel = "INFO"
        #Run the workflow, the return value being the number of failed jobs
        self.assertEquals(T.Runner.startJobTree(a, options), 0)
        T.Runner.cleanup(options) #This removes the jobStore
        #Check output
        self.assertEquals(open(outFile, 'r').readline(), "ABCDE")
        #Cleanup
        os.remove(outFile)