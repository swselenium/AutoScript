import sys
import ure
import mptf
import uefi


def run(log_path):

    obj = mptf.mptf(log_path)
    obj.Input('cls' + mptf.ENTER)
    obj.Input('fs0:' + mptf.ENTER)
    obj.SetTickTock(200)

    obj.Info('Shell Command \'exit\': ',True)
    obj.Input('exit' + mptf.ENTER)
    obj.Info('Shell Command \'exit\': ',True)
 
    result = obj.SelectOption('TPV EFI Device Manager',mptf.LIGHTGRAY + mptf.BACKBLACK)
    obj.Debug ('TPV EFI Device Manager result = ' + str(result))
    if result:
        obj.FuncKey(mptf.ENTER)
        obj.Pass('Find TPV EFI Device Manager PASS',True)
    else:
        obj.Fail('Find TPV EFI Device Manager FAIL',True)
    result_next = obj.SelectOption('User Password Management', mptf.LIGHTGRAY + mptf.BACKBLACK)
    obj.Debug ('User Password Management result = ' + str(result_next))
    if result_next:
        obj.FuncKey(mptf.ENTER)
        obj.Pass('Find User Password Management PASS',True)
    else:
        obj.Fail('Find User Password Management FAIL',True)
    result_setpw = obj.SelectOption('Change Admin Password')
    obj.Debug ('Change Admin Password result = ' + str(result_setpw))
    if result_setpw:
        obj.FuncKey(mptf.ENTER)
        obj.Pass('Find Change Admin Password PASS',True)
    else:
        obj.Fail('Find Change Admin Password FAIL',True)
    try:
        obj.Input('!QAZ1qaz' + mptf.ENTER)
        obj.Input('!QAZ1qaz' + mptf.ENTER + mptf.ENTER)
    except Exception as e:
        obj.Fail('Set password FAIL: %s' %e,True)
    obj.FuncKey(mptf.ESC, 2)
    result_reset = obj.SelectOption('Reset')
    obj.Debug ('Reset result = ' + str(result_reset))
    if result_reset:
        obj.FuncKey(mptf.ENTER)
        obj.Pass('Find reset PASS',True)
    else:
        obj.Fail('Find reset FAIL',True)
    obj.FuncKey(mptf.ENTER)

    obj.Close()