cvfl/docker
=========

## What is this ?

Docker を用いた cvfl のビルド、および、ローカルでの起動手順です。 

## Installation & Lunch

```
cd ..
cp -p .env.example .env
sed -i 's/ENV='\''\/dev\/'\''/ENV='\''\/'\''/' .env
```

```
docker build -f docker/Dockerfile -t cvfl .
docker run -p 5000:5000 cvfl
```

## Usage

ブラウザで以下 URL に接続して下さい。

http://localhost:5000