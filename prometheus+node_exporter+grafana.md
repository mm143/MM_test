# Prometheus + Node_exporter + Grafana + Consul + Alertmanager + prometheus-webhook-dingtalk 实现服务器监控,钉钉报警

## 实现过程
node_exporter 采集机器数据暴露在9100端口, prometheus 通过机器ip:9100去拉取机器的数据, grafana进行数据可视化及美化,Alertmanager定义报警规则,prometheus通过localhost:9093实现报警, Alertmanager触发报警后将告警消息发送给localhost:8060/dingtalk/ops_dingding/send(prometheus-webhook-dingtalk的服务),prometheus-webhook-dingtalk实现转发给钉钉机器人

## Prometheus 安装配置
1. 安装
```sh
# 下载压缩包
wget https://github.com/prometheus/prometheus/releases/download/v2.7.2/prometheus-2.7.2.linux-amd64.tar.gz
# 解压
tar -xzf prometheus-2.7.2.linux-amd64.tar.gz
```
2. 配置
```sh
# 配置文件示例
global:
  scrape_interval:     15s #每15s采集一次数据
  evaluation_interval: 15s #每15s 评估一次规则

# 告警,这里配置为使用了Alertmanager的配置方法
alerting:
  alertmanagers:
  - static_configs:
    - targets: ['localhost:9093']

# 告警规则配置文件目录
rule_files: [ 'rules.yml' ]

scrape_configs:
  - job_name: 'prometheus-server'  
    static_configs:
      - targets: ['localhost:9100']
    
  # 下边为使用了consul自动注册服务的配置
  - job_name: 'node'
    consul_sd_configs:
      - server: '127.0.0.1:8500'
        services: []
    relabel_configs:
      - source_labels: [__meta_consul_tags]
        regex: .*prometheus-target.*
        action: keep
```
3. 启用
 `./prometheus &`

## Node_exporter 安装配置
1. 安装
```sh
# 下载压缩包
wget https://github.com/prometheus/node_exporter/releases/download/v0.18.1/node_exporter-0.18.1.linux-amd64.tar.gz
# 解压
tar -xzf node_exporter-0.18.1.linux-amd64.tar.gz
```
2. 启用
`sudo ./node_exporter &`

## Grafana 安装配置
1. 安装 (ubuntu)
```sh
# 官网下载包
wget https://dl.grafana.com/oss/release/grafana_6.2.5_amd64.deb     #版本按需更改
# 
sudo apt-get install -y adduser libfontconfig1
# 安装
sudo dpkg -i grafana_6.2.5_amd64.deb 
```
2. 启用
- `sudo service grafana-server start`
- 开机启用
`sudo update-rc.d grafana-server defaults`
3. 使用
默认开启3000端口, 默认账户名密码为 admin/admin 

## Consul 安装配置
1. docker安装
```sh
# 拉取镜像
docker pull consul
# 运行 并绑定端口
docker run --name consul -d -p 8500:8500 consul
```

2. 压缩包安装
```sh
# 下载安装包
wget https://releases.hashicorp.com/consul/1.5.2/consul_1.5.2_linux_arm64.zip
# 解压
unzip consul_1.0.0_linux_amd64.zip
# 复制consul到bin
cp consul /usr/local/bin/
# 启动
consul agent -server -ui -bootstrap-expect 1 -data-dir /tmp/consul -bind=192.168.50.19 -client 0.0.0.0 2>&1 &   # -bind=>服务器ip -client=> 能够访问的ip
```

3. 服务注册
```sh
{
  "id": "prometheus-server",  #id 之后要删除服务时就用这个ID
  "name": "prometheus-node",    # service_name
  "address": "192.168.50.19",   #要注册服务的ip
  "port": 9100, 
  "tags": ["prometheus-target"],
  "checks": [
      {
          "http": "http://www.baidu.com",   # 健康检查的网址
          "interval": "15s"         # 健康检查间隔
      }
  ]
}
# 将上边的json内容保存成json文件, 向 http://localhost:8500/v1/agent/service/register 发送put请求
curl --request PUT --data @regitor.json http://localhost:8500/v1/agent/service/register
```

4. 解除服务
```sh
# 向http://localhost:8500/v1/agent/service/deregister发送PUT请求,后边跟服务名
curl --request PUT http://localhost:8500/v1/agent/service/deregister/SERVICE_ID   #SERVICE_ID为服务注册时的id

5. prometheus.yml 中配置
```sh
- job_name: 'consul-prometheus'
    consul_sd_configs:
    #consul 地址
      - server: 'xx.xx.xx.xx:8500'
        services: []
    relabel_configs:
      - source_labels: [__meta_consul_tags]
        regex: .*prometheus-target.*
        action: keep
      #用__meta_consul_service_id标签替换 instance中的值
      - source_labels: [__meta_consul_service_id]   
        target_label: instance
```

## Alertmanager 安装配置
1. 安装配置
```sh
# 下载安装包
wget https://github.com/prometheus/alertmanager/releases/download/v0.17.0/alertmanager-0.17.0.linux-amd64.tar.gz
# 解压
tar -xfz alertmanager-0.17.0.linux-amd64.tar.gz
# 启动
./alertmanager
```
配置文件 alertmanager.yml 如下
```sh
global:
  resolve_timeout: 5m

route:
  group_by: ['alertname']
  group_wait: 10s       #组报警等待时间
  group_interval: 10s   #组报警间隔时间
  repeat_interval: 1h   #发送的频率
  receiver: 'webhook'   #使用的通知渠道 webhook为 钉钉机器人
receivers:
- name: 'webhook'
  webhook_configs:
  - url: 'http://localhost:8060/dingtalk/ops_dingding/send'     # 这里使用的是向prometheus-webhook-dingtalk服务发消息,prometheus-webhook-dingtalk实现转发
    send_resolved: true         # 告警解除后是否发送通知
inhibit_rules:
  - source_match:
      severity: 'critical'
    target_match:
      severity: 'warning'
    equal: ['alertname', 'dev', 'instance']
```
2. prometheus.yml 中的告警规则配置
```sh
rule_files: [ 'rules.yml' ]
```
```sh
# rules.yml 示例
groups:
  - name: host_monitoring
    rules:
    - alert: 内存报警
      expr: ((node_memory_MemFree_bytes)  + (node_memory_Cached_bytes) + (node_memory_Buffers_bytes)) / 1024 / 1024 < 500
      for: 2m
      labels:
        team: node
      annotations:
       # Alert_type: 内存报警
       # Server: '{{$labels.instance}}'
        #summary: "{{$labels.instance}}: High Memory usage detected"
        explain: "可用内存 < 500MB，value：{{ $value }}MB"
        #description: "{{$labels.instance}}: Memory usage is above 80% (current value is: {{ $value }})"
    - alert: 磁盘报警
      expr: (max(node_filesystem_avail_bytes{device=~"/dev.*"}) by (instance)) / 1024 / 1024 < 1024
      for: 2m
      labels:
        team: node
      annotations:
        #Alert_type: 磁盘报警
        #Server: '{{$labels.instance}}'
        explain: "磁盘可用容量小于 1 GiB，value：{{ $value }}GiB"
    - alert: 服务告警
      expr: up == 0
      for: 2m
      labels:
        team: node
      annotations:
        #Alert_type: 服务报警
        #Server: '{{$labels.instance}}'
        explain: "node_exporter服务已断开"
```

## prometheus-webhook-dingtalk 安装配置
因为prometheus-webhook-dingtalk使用golang编写 所以我们要先安装golang
1. golang安装配置
```sh
# 下载源码
wget https://dl.google.com/go/go1.10.3.linux-amd64.tar.gz
# 解压
tar -C /usr/local -xzf go1.10.3.linux-amd64.tar.gz
# 添加二进制文件加入PATH
vim /etc/profile
export GOROOT=/usr/local/go
export PATH=$PATH:$GOROOT/bin
source /etc/profile
```

2. prometheus-webhook-dingtalk 安装配置
```sh
# golang的src目录下新建，并且cd /usr/local/go/src/github.com/timonwong
# clone 项目 并编译
git clone https://github.com/timonwong/prometheus-webhook-dingtalk.git
cd prometheus-webhook-dingtalk
make
```

3. 启动
```sh
nohup ./prometheus-webhook-dingtalk --ding.profile=“ops_dingding=dingding_webhook” 2>&1 1>dingding.log &    
# 启动8060端口, 启动后可 netstat -a | grep 8060 看下服务服务示范正常启动
# 如需要使用自定义模板 启动时加上 --template.file=""  ""内填写绝对路径
```

