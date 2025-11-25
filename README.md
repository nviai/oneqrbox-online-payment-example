# Webhook Server cho OneQR Box

## Giới thiệu

Đây là một webhook server đơn giản được xây dựng bằng FastAPI để nhận thông báo từ ứng dụng OneQR Box khi có giao dịch chuyển khoản thành công.

## Yêu cầu

- Python 3.7+
- FastAPI
- Uvicorn
- python-dotenv

## Cài đặt

### 1. Cài đặt các thư viện cần thiết
```bash
pip install fastapi uvicorn python-dotenv
```

### 2. Tạo Webhook Secret

Sử dụng OpenSSL để tạo một secret key ngẫu nhiên:
```bash
openssl rand -hex 32
```

Lệnh này sẽ tạo ra một chuỗi 64 ký tự hex (ví dụ: `17bc05010e5f423d6a26093ca76b7af13c7d882ab4cee7d3dee97f21d194ef49`)

### 3. Tạo file .env

Tạo file `.env` trong thư mục gốc của project và thêm secret key vừa tạo:
```env
WEBHOOK_SECRET=your_generated_secret_key_here
```

Ví dụ:
```env
WEBHOOK_SECRET=17bc05010e5f423d6a26093ca76b7af13c7d882ab4cee7d3dee97f21d194ef49
```

## Chạy ứng dụng

### Cách 1: Chạy trực tiếp
```bash
python main.py
```

### Cách 2: Sử dụng uvicorn
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Server sẽ chạy tại địa chỉ: `http://localhost:8000`
Mở ngrok tunnel để OneQR Box có thể gọi được API, tham khảo: ngrok.com

```bash
ngrok http 8000
```
Endpoint webhook: `https://<id>.ngrok-free.app/checkout/webhook`


## Cấu hình trong OneQR Box

1. Đăng nhập vào ứng dụng OneQR Box
2. Vào phần cấu hình webhook
3. Nhập URL webhook của bạn: `https://your-domain.com/checkout/webhook`
4. Nhập Webhook Secret giống với giá trị trong file `.env`

## Cách hoạt động

1. Khi có giao dịch chuyển khoản thành công qua OneQR Box, hệ thống sẽ gửi một POST request đến endpoint webhook của bạn
2. Request sẽ kèm theo header `x-signature` chứa chữ ký HMAC-SHA256
3. Server sẽ xác thực chữ ký bằng cách:
   - Tính toán HMAC-SHA256 của request body với secret key
   - So sánh với chữ ký nhận được từ header
4. Nếu xác thực thành công, server sẽ xử lý dữ liệu webhook
5. Trả về response "ok" để xác nhận đã nhận webhook
