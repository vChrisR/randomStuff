from java.util import *
from javax.management import *
import sys, traceback

adminServerURL = "t3://localhost:${wlAdminServerPort}"

def saveAndActivate():
    save()
    activate(block="true")
    return

def editStartEdit():
    edit()
    startEdit(exclusive="true", waitTimeInMillis=36000)
    return
	
connect("weblogic", "$wlAdminPassword", adminServerURL)
editStartEdit()
cluster = cmo.createCluster("$wlClusterName")
cluster.setClusterMessagingMode("unicast")

# CREATE MACHINE
machine = cmo.createMachine("${wlManagedServerName}_machine01")
nodeManager = machine.getNodeManager()
nodeManager.setListenAddress("$wlNodeManagerAddr")
nodeManager.setListenPort($wlNodeManagerPort)
nodeManager.setUserName("$wlNodeManagerUser")
nodeManager.setPassword("$wlNodeManagerPassword")
nodeManager.setNodeManagerHome("$INSTALLDIR/user_projects/domains/$wlDomainName/nodemanager")
nodeManager.setDebugEnabled(true)
nodeManager.setNMType("plain")

# CREATING MANAGED SERVER
server = cmo.createServer("$wlManagedServerName")
server.setListenAddress("$wlManagedServerAddr")
server.setListenPort($wlManagedServerPort)
server.setAutoRestart(true)
server.setAutoKillIfFailed(true)
server.setRestartMax(2)
server.setRestartDelaySeconds(60)
serverStartConfig = server.getServerStart()
serverStartConfig.setBeaHome("$INSTALLDIR")
serverStartConfig.setRootDirectory("$INSTALLDIR")
serverStartConfig.setUsername("$wlManagedServerUser")
serverStartConfig.setPassword("$wlManagedServerPassword")
serverStartConfig.setJavaHome("$INSTALLDIR")
serverStartConfig.setArguments("${wlManagedServerJvmArgs} -Djava.library.path=$INSTALLDIR/wlserver/server/native/linux")

# ADD MANAGED SERVERS TO CLUSTER
server.setCluster(getMBean("/Clusters/" + "$wlClusterName"))

# ADD MANAGED SERVERS TO MACHINE
server.setMachine(machine)
saveAndActivate()
disconnect()

except:
apply(traceback.print_exception, sys.exc_info())
dumpStack()
exit(exitcode=-1)

exit()
