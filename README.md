# scanner
扫描器基本组件。每个文件可以单独使用。

1-spider_domain.py用来爬取一个网站上所有链接的域名。-u指定url，-d指定爬取深度。
```bash
usage: 1-spider_domain.py [-h] [-u] [-d]

Spider_domain V1.0 to spider a website to get all domains

optional arguments:
  -h, --help    show this help message and exit
  -u , --url    url
  -d , --deep   deep to spider

```
2-domain_to_ip.py来获取域名对应的ip地址，并且把ip地址扩展一个子网。例如爬取到1.1.1.1和1.1.1.254,则1.1.1.0/24都有可能是这个企业的ip段。-s可以制定两个ip距离多少可以将这中间的ip全部看作ip段。为0-3，0为最小。
``` bash
usage: 2-domain_to_ip.py [-h] [-i] [-o] [-s]

Domain_to_ip v1.0 to query domain name to ip address and format ip address

optional arguments:
  -h, --help     show this help message and exit
  -i , --input   input file
  -o , --out     result out file
  -s , --scope   format scope,from 0 to 3,0 means a small scope

```
3-zmap_live.py用来使用zmap扫描存活的ip。
```bash
usage: 3-zmap_live.py [-h] [-i] [-o] [-t]

Zmap_live V1.0 to scan for live hosts

optional arguments:
  -h, --help     show this help message and exit
  -i , --input   input file
  -o , --out     result out file
  -t , --times   Retry times in case zmap scan failed!
```
3-zmap_port.py用来扫描开放的端口。-l范围为1-3，代表扫描开放端口的范围大小，1为最小。
```bash
usage: 3-zmap_port.py [-h] [-i] [-o] [-t] [-l]

Zmap_port V1.0 to scan for open port

optional arguments:
  -h, --help     show this help message and exit
  -i , --input   input file
  -o , --out     result out file
  -t , --times   Retry times in case zmap scan failed!
  -l , --level   level of ports to scan,1-3,1 means the least
```