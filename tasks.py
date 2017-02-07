# Copyright (c) 2015 Snowplow Analytics Ltd. All rights reserved.
#
# This program is licensed to you under the Apache License Version 2.0,
# and you may not use this file except in compliance with the Apache License Version 2.0.
# You may obtain a copy of the Apache License Version 2.0 at http://www.apache.org/licenses/LICENSE-2.0.
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the Apache License Version 2.0 is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the Apache License Version 2.0 for the specific language governing permissions and limitations there under.

import datetime, json, uuid, time
from functools import partial
from random import choice

from invoke import run, task


JAR_FILE = "gcp-dataflow-example-project-0.0.0.jar"

# Selection of EventType values
COLORS = ['Red','Orange','Yellow','Green','Blue']
        

# GCP Pub/Sub Data Generator
def picker(seq):
  """
  Returns a new function that can be called without arguments
  to select and return a random color
  """
  return partial(choice, seq)

def create_event():
  """
  Returns a choice of color and builds and event
  """
  event_id = str(uuid.uuid4())
  color_choice = picker(COLORS)

  return (event_id, {
    "id": event_id,
    "timestamp": datetime.datetime.now().isoformat(),
    "type": color_choice()
  })

def write_event(conn, stream_name):
  """
  Returns the event and event event_payload
  """
  event_id, event_payload = create_event()
  event_json = json.dumps(event_payload)
  conn.put_record(stream_name, event_json, event_id)
  return event_json


@task
def generate_events(profile, region, stream):
    """
    load demo data with python generator script for SimpleEvents
    """
    conn = kinesis.connect_to_region(region, profile_name=profile)
    while True:
        event_json = write_event(conn, stream)
        print "Event sent to Kinesis: {}".format(event_json)
        #time.sleep(5)


@task
def build_project():
    """
    build gcp-dataflow-example-project
    and package into "fat jar" ready for Dataflow deploy
    """
    run("sbt assembly", pty=True)


@task
def set_project(project):
    """
    set the appropriate project 
    """
    pass


@task
def create_bigtable_table(project, region, table):
    """
    Cloud Bigtable table creation 
    """
    pass

@task
def create_pubsub_topic(project, topic):
    """
    create our pubsub topic
    """
    pass


@task
def run_project(config_path):
    """
    Submits the compiled "fat jar" to Cloud Dataflow and
    starts Cloud Dataflow based on project settings
    """
    pass

#    run("./spark-master/bin/spark-submit \
#        --class com.snowplowanalytics.spark.streaming.StreamingCountsApp \
#        --master local[4] \
#        ./target/scala-2.10/{} \
#        --config {}".format(JAR_FILE, config_path),
#        pty=True)
