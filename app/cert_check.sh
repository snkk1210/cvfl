#!/bin/bash

##############################################################################
#これは何？
# 証明書、秘密鍵、中間証明書の整合性が保たれているか確認するスクリプトです
#
#使い方
# 下記の通りに引数を指定して実行してください
#
# =====================
# 第一引数に証明書
# 第二引数に秘密鍵
# 第三引数に中間証明書
# =====================
#
# 実行結果がOKであれば整合性が保たれています
# 証明書の期限も出力されます
#
#使用例
#
# ./cert_check.sh server.crt server.key server.ca.crt
##############################################################################

FILE1=/tmp/temp1.txt
FILE2=/tmp/temp2.txt

# エラー出力関数
function stdout_error(){
        echo "実行結果が不正です"
        exit 1
}

# opensslコマンドの実行結果確認関数
function error_check(){
        if [ $? != 0 ]; then
                stdout_error
        fi
}

# 引数のチェック
if [ $# != 3 ]; then
        echo "正しく引数を指定してください"
        exit 1
fi

# ファイルの初期化
cat /dev/null > $FILE1
cat /dev/null > $FILE2

# 証明書のハッシュ値を出力
openssl x509 -noout -modulus -in $1 > /dev/null 2>&1
error_check
openssl x509 -noout -modulus -in $1 | md5sum 1> $FILE1 2> /dev/null

# 秘密鍵のハッシュ値を出力
openssl rsa -noout -modulus -in $2 > /dev/null 2>&1
error_check
openssl rsa -noout -modulus -in $2 | md5sum 1> $FILE2 2> /dev/null

# 証明書のハッシュ値を出力
openssl x509 -issuer_hash -noout -in $1 > /dev/null 2>&1
error_check
openssl x509 -issuer_hash -noout -in $1 1>> $FILE1 2> /dev/null

# 中間証明書のハッシュ値を出力
openssl x509 -subject_hash -noout -in $3 > /dev/null 2>&1
error_check
openssl x509 -subject_hash -noout -in $3 1>> $FILE2 2> /dev/null

# ファイルに出力があるか確認
if [ ! -s $FILE1 ]; then
        stdout_error
fi

# 正しく出力されているか確認
FILE1_line=`cat $FILE1 | wc -l`
FILE2_line=`cat $FILE2 | wc -l`

if [ $FILE1_line != 2 ]; then
        stdout_error
fi

if [ $FILE2_line != 2 ]; then
        stdout_error
fi

# 整合性確認
if diff -q $FILE1 $FILE2 > /dev/null ; then
        echo "OK"
        openssl x509 -noout -dates -in $1
else
        echo "ERROR"
fi
