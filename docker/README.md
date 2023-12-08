cvfl/docker
=========

## What is this ?

Docker を用いた CVFL のコンテナビルド、および、起動手順です。 

## Installation & Lunch

```
cd ..
cp -p .env.example .env
sed 's/ENV='\''\/dev\/'\''/ENV='\''\/'\''/' .env
```

```
docker build -f docker/Dockerfile -t cvfl .
docker run -p 5000:5000 cvfl
```

## Usage

ブラウザから下記 URL に接続

http://[ip address]:5000