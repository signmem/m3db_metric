#/usr/bin/python

# apiURL = m3query api recommend;  [ optional  m3db api ]
# queryRUL = m3query api 
# savepath  use to save metrics to localdir

m3info=[{"namespace":"app","apiURL":"http://app_namespace_m3query_ipaddr:m3queryport","queryURL":"http://m3query_api_ipaddr:port"}]
label_api="/api/v1/labels"
metric_api="/api/v1/label/__name__/values"
query_api="/api/v1/query?"
db={"host":"localhost","user":"db_username","password":"db_password", "dbname":"db_name"}
savepath="m3db"
