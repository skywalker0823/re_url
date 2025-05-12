#!/bin/bash

# 提示輸入域名
read -p "請輸入您的域名 (例如: example.com): " domain

if [ -z "$domain" ]; then
    echo "域名不能為空！"
    exit 1
fi

# 生成 .env 檔案
echo "正在生成 .env 檔案..."
cat > .env << EOF
DOMAIN_NAME=$domain
EOF

# 生成 nginx.conf
echo "正在生成 nginx.conf..."
cat > ./nginx/nginx.conf << EOF
events {
    worker_connections 1024;
}

http {
    upstream flask_app {
        server web:5000;
    }

    server {
        listen 80;
        listen [::]:80;
        server_name $domain;

        location / {
            proxy_pass http://flask_app;
            proxy_set_header Host \$host;
            proxy_set_header X-Real-IP \$remote_addr;
            proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto \$scheme;
        }
    }
}
EOF

echo "### Starting services ..."
docker-compose up --force-recreate -d
