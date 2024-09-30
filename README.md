# Calabiyau(卡拉彼丘) server node switcher
This is a simple server node switcher for Calabiyau(卡拉彼丘) game. It can help you change hosts file to switch server node easily.

## How to use
1. Download the latest release from [release page](https://github.com/Halozhan/calabiyau_dns_fixer/releases).
2. Run the executable file.
3. There are four regions and you have to choose the best server for each.
![image](https://github.com/user-attachments/assets/fedbc086-0630-4d9c-a3c3-f2da3c913f6d)


## What is the best server?
The best server is the server that has the lowest and most stable ping.
In my case, I live in Korea. So, the best server might be different from your country.
```
Tianjin(天津) is 116.130.xxx.xxx or 123.151.54.47 is recommended.
Nanjing(南京) is 182.50.15.118 or 121.229.92.16, 180.110.193.185 is recommended.
Guangzhou(广州) is 43.159.233.178 or 183.47.107.193 is recommended.
Chongqing(重庆) is 113.250.9.xxx or 58.144.164.xxx is recommended.

Avoid 43.159.233.xxx if possible, except for Guangzhou(广州). Those servers are Hong Kong relay servers and can have high latency.
```

## How to restore hosts file
There are 4 buttons each. "set to default" button can restore hosts file to default.


## Contribution
```sh
pip install -e .
```