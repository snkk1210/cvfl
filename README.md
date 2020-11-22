certificate_verify_flask_lambda
=========

## これは何？

SSL証明書の整合性をチェックするWEBツールです。  
AWSのlambdaにデプロイします。

## 使い方

### 0.必要なパッケージの導入

```
yum install python3 python3-devel
pip3 install flask
```

### 1.レポジトリのclone

```
git clone [URL]
cd certificate_verify_flask_lambda
```

### 2.lambdaにデプロイ

```
zappa init
zappa deploy
```

