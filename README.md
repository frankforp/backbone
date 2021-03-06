# backbone
使用Tornado（Python）框架搭建网站的示例。


## include
* 7x24hs 是主站，单页网站，个人信息展示，[Demo](http://www.7x24hs.com)
* qrcode 输入URL，获取二维码，[Demo](http://qrcode.7x24hs.com)
* kit (keep in touch)，各站点下面联系我的发送消息，通过发送email提醒站长, [Demo](http://kit.7x24hs.com)
* api，account服务: 登录／注册／忘记密码／修改个人昵称、头像；session服务, [Demo](http://7x24hs.com/login)
* ui: 移动端UI, [Demo](http://ui.7x24hs.com)
* blog: 个人博客, [Demo](http://blog.7x24hs.com)

## 部署系统环境：
Linux CentOS 7.0 x86-64

Python 2.7.3

    # yum install libtool -y
    # yum install zlib zlib-devel -y
    # yum install openssl -y
    # yum install pcre -y
    # yum install nginx -y
    # yum install openssl-devel -y
    # yum install python-devel -y

    # pip install --upgrade tornado
    # pip install --upgrade pymongo
    # pip install --upgrade xlwt
    # pip install --upgrade xhtml2pdf
    # pip install --upgrade wechat-sdk
    # pip install --upgrade qrcode
    # yum install libjpeg-turbo-devel -y
    # pip install --upgrade Image
    # pip install --upgrade html2text
    # pip install --upgrade markdown

Nginx配置
>    # vi /etc/nginx/conf.d/7x24hs.com.conf 

    server {
        listen   80;
        root /root/nmapp2_venv;
        index main.py index.html;

        server_name 7x24hs.com;

        location / {
            proxy_pass_header Server;
            proxy_set_header Host $http_host;
            proxy_redirect off;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Scheme $scheme;
            proxy_pass http://127.0.0.1:8001;
        }
    }
    
    server {
        listen   443 ssl;
        root /root/nmapp2_venv;
        index main.py index.html;

        server_name 7x24hs.com;

        ssl          on;
        ssl_certificate       /etc/nginx/sslkey/7x24hs.com_bundle.crt;
        ssl_certificate_key   /etc/nginx/sslkey/7x24hs.com.key;
        ssl_session_timeout   5m;
        ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
        ssl_ciphers AESGCM:ALL:!DH:!EXPORT:!RC4:+HIGH:!MEDIUM:!LOW:!aNULL:!eNULL;
        ssl_prefer_server_ciphers  on;

        location / {
            proxy_pass_header Server;
            proxy_set_header Host $http_host;
            proxy_redirect off;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Scheme $scheme;
            proxy_pass http://127.0.0.1:8001;
        }
    }

>    # vi /etc/nginx/conf.d/kit.7x24hs.com.conf

    server {
        listen   80;
        root /root/nmapp2_venv;
        index main.py index.html;

        server_name kit.7x24hs.com;

        location / {
            proxy_pass_header Server;
            proxy_set_header Host $http_host;
            proxy_redirect off;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Scheme $scheme;
            proxy_pass http://127.0.0.1:8005;
        }
    }

>    # vi /etc/nginx/conf.d/qrcode.7x24hs.com.conf 

    server {
        listen   80;
        root /root/nmapp2_venv;
        index main.py index.html;

        server_name qrcode.7x24hs.com;

        location / {
            proxy_pass_header Server;
            proxy_set_header Host $http_host;
            proxy_redirect off;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Scheme $scheme;
            proxy_pass http://127.0.0.1:8003;
        }
    }

>    # vi /etc/nginx/conf.d/ssl.conf

    # HTTPS server
    server {
        listen       443 ssl;
        server_name  localhost;

        ssl          on;
        ssl_certificate       /etc/nginx/sslkey/7x24hs.com_bundle.crt;
        ssl_certificate_key   /etc/nginx/sslkey/7x24hs.com.key;
        ssl_session_timeout   5m;
        ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
        ssl_ciphers AESGCM:ALL:!DH:!EXPORT:!RC4:+HIGH:!MEDIUM:!LOW:!aNULL:!eNULL;
        ssl_prefer_server_ciphers  on;

        location / {
            root   html;
            index  index.html index.htm;
        }
    }

使用外部的smtp服务器发送mail
>    # vi /etc/mail.rc  

    set from=no_reply@7x24hs.com
    set smtp=smtp.mxhichina.com
    set smtp-auth-user=no_reply@7x24hs.com
    set smtp-auth-password=your_password
    set smtp-auth=login

然后通过命令来发送测试邮件
> echo "hello word" | mail -s "title” thomas.zh@qq.com  
