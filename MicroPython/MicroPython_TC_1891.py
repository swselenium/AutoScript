import sys
import ure
import mptf
from time import sleep 

def run(log_path):

    obj = mptf.mptf(log_path)
    obj.Input('cls' + mptf.ENTER)
    obj.Input('fs0:' + mptf.ENTER)
    obj.SetTickTock(200)

    #ls list
    obj.Info('Shell Command \'ls\': ',True)

    obj.Input('ls')
    obj.FuncKey(mptf.ENTER)

    if obj.WaitUntil('Dir', 10):
        obj.Pass('PASS',True)
    else:
        obj.Fail('FAIL',True)

    obj.Input('cls' + mptf.ENTER)
    obj.Input('echo reset test' + mptf.ENTER)
    if obj.Verify('reset test', None):
        obj.Pass('Print Reset PASS',True)
    else:
        obj.Fail('Print Reset FAIL',True)
    obj.Input('reset' + mptf.ENTER)
    sleep(5)
    try:
        if obi.WaitUntil('UEFI shell', 60):
            obj.Pass('Reset function test PASS',True)
        else:
            obj.Fail('Reset function test FAIL',True)
    finally:
            obj.Close()
            print ("Finish 1891 test")