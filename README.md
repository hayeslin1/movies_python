# movies_python
资源采集网爬虫


> python2.7

## 爬取网站上不定时更新的视频资源
+ MainTask : 电影爬虫
+ TV_Task : 电视剧爬虫
+ Media_Task : 综艺爬虫
+ Anime_Task : 动漫爬虫
+ searchTask : 搜索爬虫

## 视频站

+ 当前项目只是爬取数据并入库，并不具备展示和播放视频的功能。 

+ 有需要的小伙伴可以fork[这个项目]([http://](https://github.com/hayeslin1/hayes_tube))

+ 项目地址： https://github.com/hayeslin1/hayes_tube.git


## 启动脚本命令：
```shell 

git clone https://github.com/hayeslin1/movies_python.git

python MainTask.py
python TV_Task.py
python Media_Task.py
python Anime_Task.py
python searchTask.py

## 可自行设置crontab定时任务

```

## 提供联合脚本：
```shell 
#!/bin/bash

yum install -y wget 
yum install -y git


mkdir -p /home/videos
cd /home/videos

git clone https://github.com/hayeslin1/hayes_tube.git 
git clone https://github.com/hayeslin1/movies_python.git 

wget http://mirrors.tuna.tsinghua.edu.cn/apache/maven/maven-3/3.6.2/binaries/apache-maven-3.6.2-bin.tar.gz

tar -zxvf apache-maven-3.6.2-bin.tar.gz

echo 'export MVN_HOME=/home/videos/apache-maven-3.6.2' >> /etc/profile
echo 'export PATH=$PATH:$MVN_HOME/bin' >> /etc/profile

source /etc/profile

cp /home/videos/hayes_tube/aliyun/settings.xml /home/videos/apache-maven-3.6.2/conf/settings.xml

cd /home/videos/hayes_tube/

source /etc/profile
mvn clean install 

nohup java -jar target/hayes_tube-0.0.1-SNAPSHOT.jar --server.port=8080  >> /home/videos/hayes_tube/catalina.out 2>&1 &


yum install -y epel-release
yum install -y python-pip

pip install --upgrade pip
pip install requests 
pip install bs4
pip install pymysql
pip install lxml
pip install logging 

cd /home/videos/movies_python

touch crew.sh
chmod +x crew.sh

echo '#!/bin/bash' >> crew.sh
echo 'source /etc/profile' >> crew.sh
echo '' >> crew.sh
echo 'python MainTask.py' >> crew.sh
echo 'python TV_Task.py' >> crew.sh
echo 'python Media_Task.py' >> crew.sh
echo 'python Anime_Task.py' >> crew.sh

bash crew.sh 

crontab -l > conf && echo "00 00 * * *  /bin/bash /home/videos/movies_python/crew.sh" >> conf 
crontab conf && rm -f conf

```



## 感谢

> [OK资源网](http://www.jisudhw.com/) 
