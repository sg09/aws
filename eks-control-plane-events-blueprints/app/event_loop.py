import sched, time
from kubernetes import client, config, watch

#Config varables
TIMER_FREQUENCY_IN_SECONDS=3600
INITIAL_DELAY_IN_SECONDS = 10

#Load K8s cluster configuration
config.load_incluster_config()

#Get api client
v1 = client.CoreV1Api()

#Initialize the scheduler
s = sched.scheduler(time.time, time.sleep)

def lookup_pod_events():
    for event in watch.Watch().stream(v1.list_pod_for_all_namespaces, timeout_seconds=10):
           print( "Event: %s %s %s" % ( event["type"],event["object"].kind,event["object"].metadata.name)) 

def lookup_ns_events():
    for event in watch.Watch().stream(v1.list_namespace, timeout_seconds=10):
           print( "Event: %s %s %s" % ( event["type"],event["object"].kind,event["object"].metadata.name)) 

def lookup_events(sc):
    #Get pod events
    lookup_pod_events()
    #Get namespace events
    lookup_ns_events()
    #Rinse and repeat       
    s.enter(TIMER_FREQUENCY_IN_SECONDS, 1, lookup_events, (sc,))

#Start here
s.enter(INITIAL_DELAY_IN_SECONDS, 1, lookup_events, (s,))
s.run()
