# Calabiyau(卡拉彼丘) server node switcher

This is a simple server node switcher for Calabiyau(卡拉彼丘) game. It can help you change hosts file to switch server node easily.
**Due to recent changes in game server logic, the following method no longer works.**

## How to use

1. Use xunyou VPN or
2. Use Mudfish VPN but use mudfish profiles from the release channel

~~1. Download the latest `net8.0-windows.zip` release from [release page](https://github.com/Halozhan/calabiyau-server-node-switcher/releases/latest).~~
~~2. `Extract` the zip file.~~
~~3. Run the `exe`cutable file.~~
~~4. There are four regions and you have to choose the lowest score servers.~~
~~5. You can simple click by `Auto-Find Best Server` and it will find the best server for you.~~
~~6. Done! You can now play the game with the selected server.~~

![image](https://github.com/user-attachments/assets/462cb765-34a7-4189-83fe-4b4f376466f8)
![image](https://github.com/user-attachments/assets/539a7fb5-a174-419f-93c8-3152faafede4)

## How to change server node manually

1. `Open` the `hosts` file with administrator in the `C:\Windows\System32\drivers\etc` directory.
2. `Add` each game server ip and domains to the hosts file.
3. example like this

```
157.148.58.53 ds-gz-1.klbq.qq.com
175.27.48.249 ds-cq-1.klbq.qq.com
182.50.15.118 ds-nj-1.klbq.qq.com
109.244.173.251 ds-tj-1.klbq.qq.com
```

## How to restore hosts file

`Reset Configurations` button can restore hosts file to default.

or you can manually delete the added lines in the hosts file.

## Contribution

Feel free to open an issue or pull request.
