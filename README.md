

### 发送短信
> POST http://127.0.0.1:8877/send_messages

```markdown
        {
            "phone_number":"185****0621",
            "sms_sign":"员工盒子",
            "template_id":"378130",
            "proxy":"腾讯云",
            "params":["老杨","短信模块","发送成功了"]
        }
```



### 发送邮件
> POST http://127.0.0.1:8877/send_email

```markdown
        {
            "content":"请查收报表,谢谢!",
            "title":"每日报表",
            "receivers":["1041132457@qq.com"],
            "to_name":"Dear",
            "send_name":"员工盒子",
            "file_name":"每日报表.xlsx",
            "file_path": "C:\\Users\\dell\\Desktop\\报表.xlsx",
            "file_type":"xlsx"
        }
```