# 数据库配置模块

## 配置说明

### 数据库连接配置
```plaintext
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost:3306/shixun'
```

### 使用说明
连接字符串格式：
```plaintext
mysql+pymysql://<用户名>:<密码>@<主机>:<端口>/<数据库名>
```
修改成本地数据库即可访问自己的数据库
