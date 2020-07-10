import subprocess
import sys
import datetime
from growatt import hash_password, GrowattApi, Timespan

# growatt server settings
username = sys.argv[1]
password = sys.argv[2]
deviceSerial = sys.argv[3] 
# pvpower server settings
apiKey = sys.argv[4] 
systemId = sys.argv[5]

with GrowattApi() as api:

    # Login and get info from growatt
    api.login(username, password)
    plant_detail = api.new_inverter_detail(deviceSerial)

    # extract values
    d = datetime.datetime.today().strftime("%Y%m%d")
    t = datetime.datetime.today().strftime("%H:%M")
    v1 = plant_detail["data"]["e_today"] * 1000
    v2 = plant_detail["data"]["pac"]
    v6 = plant_detail["data"]["vacr"]
    
    # format curl command
    curlCmd = f'curl -d "d={d}" -d "t={t}" -d "v1={v1}" -d "v2={v2}" -d "v6={v6}" -H "X-Pvoutput-Apikey: {apiKey}" -H "X-Pvoutput-SystemId: {systemId}" https://pvoutput.org/service/r2/addstatus.jsp'
    #print(curlCmd)
    subprocess.check_output(curlCmd, shell=True, stderr=subprocess.STDOUT)