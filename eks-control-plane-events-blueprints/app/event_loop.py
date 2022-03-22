import sched, time
from kubernetes import client, config, watch
config.load_incluster_config()

v1 = client.CoreV1Api()
s = sched.scheduler(time.time, time.sleep)
def lookup_events(sc):
    for event in watch.Watch().stream(v1.list_pod_for_all_namespaces, timeout_seconds=10):
           print( "Event: %s %s %s" % ( event["type"],event["object"].kind,event["object"].metadata.name)) 
           s.enter(5, 1, lookup_events, (sc,))

s.enter(5, 1, lookup_events, (s,))
s.run()
