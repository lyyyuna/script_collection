# -*- coding:utf-8 -*-
s = """
{"info":[[0,1,25,16777215,1452421982,"1452419087",0,"f88285a0",0],"你玩过GTA5吗？？？？",[21161186,"最爱动漫宅",0,0],[],[0,">100000"],[]],"cmd":"DANMU_MSG","roomid":17122}
"""

import json
j = json.loads(s)

print j['cmd']

print j['info'][1].encode('utf8')
print j['info'][2][1].encode('utf8')