import subprocess
import time
from timeloop import Timeloop
from datetime import timedelta
# from CommonHelper import GlobalVariables
# from CommonHelper import Common
from subprocess import call
from CommonHelper.GVar import tblFunctionList, funcNotyetStatus
from MySQLHelper import Query


tl = Timeloop()


@tl.job(interval=timedelta(seconds=1))
def job_every_2s():
    print("Scanning to do job {}".format(time.ctime()))
    ListFuncTodo = Query.GetFunctionStatus(funcNotyetStatus)
    for x in ListFuncTodo:
        print("Calling function: ", x[0])
        Query.SetFuntionIsRunning(x[0], 'running')
        call(["python", x[0] + ".py"])


if __name__ == "__main__":
    tl.start(block=True)
