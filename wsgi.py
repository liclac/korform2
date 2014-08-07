import newrelic.agent
newrelic.agent.initialize('newrelic.ini')

from korform2 import app as application

