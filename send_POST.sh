host=http://localhost:8000
#host=https://www.srvusd-lunch.com/flameless
curl -X POST -H 'Content-Type: application/json' -d @requests.json ${host}/flameless
