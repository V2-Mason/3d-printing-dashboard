# 🔐 Streamlit Cloud Secrets 配置指南

## 配置步骤

1. **访问Streamlit Cloud**
   - 打开：https://share.streamlit.io/
   - 登录您的账号

2. **进入App设置**
   - 找到您的App：`3d-printing-dashboard`
   - 点击右侧的 **"⚙️ Settings"** 按钮

3. **打开Secrets配置**
   - 在左侧菜单中，点击 **"Secrets"**

4. **复制以下内容到Secrets编辑器**

```toml
[gcp_service_account]
type = "service_account"
project_id = "grounded-region-485009-u0"
private_key_id = "69396d0b03e06fc68d50800c07f48452c1f20cff"
private_key = """-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCfKvXIOMxz7DYp
tn0O5fpyN8FfMBaOA2Z312wALQeNkztCqO3HlOB13dcjk92Z3cmHON9adl3230+M
GgsE+qioKBs2/cyC0KFMl56GYR1l23cxiF4zyoGh/QdzYUf1Ab1sLUoqyfbOHmJE
ulKyCybf8INIg58uD+jzyJMEpLJSdpVIi6wBe9Qmu9+eM2aDY12qs2nSCESbMKdm
Zh2EapiQ9RsR9tBfXqDuILtyT2JGN30oixvVWKhoTAX1FlXeoo8/zj+UzuRrNhSl
wGyFMc+q4QjTne/DjVCvBxSoXMDTJNV/UEWBfzYTtju3BfIAF8rz4fJ/N4JjUF1y
ypN349NnAgMBAAECggEABHU0EAkDNOXzOGTbiMzJIGTOXiefIhgXSRj39eNM+Fqc
yMepbTMOvE5bxavRA4uyJr7hhouVIyJq/G4IS/nnOlpxNK+UCD/mnJoMfw/+PkmQ
w4rhtIqh6dMH3+PkG4kScJKuJpekeW5hazJauZDVZGU8kA3bqfMZH6bI81LXibas
MEdKT5P6FGHQHhUwRFlaZvvy4U2rouENDN5pUOhjll0zUecTFuBUqYD8/+HNfpaV
/tTwuXNQqKBq1XZ/iPpYX68Gy62RUDgkkFS25UvYnNBNHsYJo4hjTkifh5vT/VBx
xg8ndI/zQS0HwfS9YROiQvl3n1h4AIXW3JMjh+fcdQKBgQDXBRrhPS+dxDe2RPwv
f4zqR+ORn59pL2eHH2ZFoxeu4Beem8oF7ayZ3R3I/b53BpXmUrY/MZfRtOTj4qf5
la50+O8kKniQkS4226Y/YB0fw2uIxcyTqfLbtF138mhOXs0N5m56b025BommslBb
vkD8UTexfmCYWc57XRka6qRqIwKBgQC9gM+eyCmr1uuUaE4/qDAqZTQku0s6UxK1
CPCdd4GRF1YsUiLjsgDBAUzL+rIPhsAfLiA9B5wAwnSHIsXPNn2AtvNnMIubXE2h
492dNW9bOP37edEF923ZPDldFFPDHnAJFB18K3NqENSVt7itpO6KNaLZMVzl2qrD
sSJbvqK77QKBgHoKFriSrsz/ypM0UmJvJb7vcJV9oM/lrP//bV/G8rE51Y4bZC27
OYTXAInMo2cRINFqTrBNaJsI7gT951L8htkzVSAUzvtWu4E9Z/1+guk9VHJ7ueJx
yjqzA34J4vPgUMg76qapN9b1g/lOKdf4gw/y1QZz8UVna4+PRqmFVi47AoGBAIWo
pMfJRhr9q4sxRn9/kPlWCEEgGR86GKe3dn6aG7jKTO1VwWX31rBKym/UkmKBGGDl
l7dz9oRSov3teLd+J2bxoxvVEaKyp87XeSe42KHuwLTuZo9exQvDfnI4NBwbC8pb
dbButSjKViaDPq669cRlsEagmnVElc0Q0rsC6qTBAoGAYihfi1iJXGDMtNaQ0uev
rEOGNbH/O29CXVIzAKF+Ue1IeQZRbOI5ijs1D8LDG86KWlHY8WWNj4y7KOBWW2Q1
FppBQRd+eNGm++kRIT3JclhBXXelI1hTAE/CbYC13xNJKbFtR4KLYFHhiTovFf5V
RvA6HDgOIc0rD4CTrN1ucxw=
-----END PRIVATE KEY-----"""
client_email = "streamlit-dashboard@grounded-region-485009-u0.iam.gserviceaccount.com"
client_id = "116466063783757749964"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/streamlit-dashboard%40grounded-region-485009-u0.iam.gserviceaccount.com"
universe_domain = "googleapis.com"
```

5. **点击 "Save" 保存**

6. **重启App**
   - Streamlit会自动重启并应用新的配置

---

## ✅ 完成后

配置完成后，Dashboard将能够：
- 从Google Drive加载历史数据
- 上传新周次数据
- 自动管理多周数据

---

## 🔒 安全提示

- Secrets配置是加密存储的
- 只有您能看到和编辑
- 不会出现在代码仓库中
