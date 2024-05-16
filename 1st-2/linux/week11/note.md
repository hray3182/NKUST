# 12週考試筆記

更新 apt

```
sudo apt update
```

安裝 ssh 

```
sudo apt install openssh-server
```

重啟 ssh service 

```
sudo service ssh restart
```

安裝 net-tools

```
sudo apt install net-tools
```

安裝完 net-tools 可以用 `ifconfig` 查看 IP，並改用 ssh 操作

安裝 apache2

```
sudo apt install apache2
```

重啟 apache2 

```
sudo service apache2 restart
```

安裝 mysql server

```
sudo apt install mysql-server
```

打開 mysql

```
sudo mysql
```

啟用 root 密碼登入

```sql
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password';
```

輸入 `exit` 離開

安裝 PHP

```
sudo apt install php libapache2-mod-php php-mysql
```

檢查有無安裝成功

```
php -v
```

安裝 phpmyadmin

```
sudo apt install phpmyadmin
```

