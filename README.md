# ElasticSearch Test
## Installation
### Elasticsearch
Download the latest package here https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-1.4.2.deb and install it.

```
# dpkg -i elasticsearch-1.4.2.deb
```

For more detail instructions, please visit http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/_installation.html

### head plugin
head is a plugin that allows you to take a look at your indexes and documents and also all the settings in your elasticsearch. It is a very convenient tool.

```
# cd /usr/share/elasticsearch/bin
# ./plugin -install mobz/elasticsearch-head
```

After you install the plugin, you can take a look at your elasticsearch through http://localhost:9200/_plugin/head

For more information, please visit http://mobz.github.io/elasticsearch-head/

### mmseg plugin
The mmseg plugin is an analysis tool for Chinese (simplified specifically). It is also part of the elasticsearch-rtf project.
Take a look at their github page for more detail: https://github.com/medcl/elasticsearch-analysis-mmseg

Download the jar first https://github.com/medcl/elasticsearch-rtf/blob/master/plugins/analysis-mmseg/elasticsearch-analysis-mmseg-1.2.2.jar
Remember to get the link from the "Raw" button.

```
# cd /usr/share/elasticsearch/plugins
# mkdir analysis-mmseg
# cd analysis-mmseg
# wget https://github.com/medcl/elasticsearch-rtf/raw/master/plugins/analysis-mmseg/elasticsearch-analysis-mmseg-1.2.2.jar
```

Download the data files

```
# cd /etc/elasticsearch
# mkdir mmseg
# wget https://github.com/medcl/elasticsearch-rtf/raw/master/config/mmseg/chars.dic
# wget https://github.com/medcl/elasticsearch-rtf/raw/master/config/mmseg/units.dic
# wget https://github.com/medcl/elasticsearch-rtf/raw/master/config/mmseg/words.dic
# wget https://github.com/medcl/elasticsearch-rtf/raw/master/config/mmseg/words-my.dic
```

## Start the server
```
# service elasticsearch start
```

## Dependencies
```
$ sudo apt-get install libxml2-dev libxslt1-dev python-dev zlib1g-dev
```
After these packages are installed, use pip to install the requirements
```
(estest)$ pip install -r requirements.txt
```

## Final steps
### Create index
```
(estest)$ python create_index.py
```

### Start crawling
```
(estest)$ python scrape.py
```

### Start the server
```
(estest)$ python server.py
```
The server runs at port 9528. Open your browser and browse http://localhost:9528/
