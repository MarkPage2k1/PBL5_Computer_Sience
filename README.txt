*Nếu tạo mới cơ sở dữ liệu trên FireBase thì các việc cần thay đổi trên code ESP32_cam:
	+ Nhập tên và mật khẩu wifi tương ứng đang muốn ESP32_cam kết nối tới
	+ Nhập API Key của csdl đó
	+ Nhập URL của Real Time db mới
	+ Nhập Nhập Email và mật khẩu tương ứng khi đăng kí cơ sở dữ liệu mới trên Firebase
	+ Sửa tên biến "Account" tương ứng với tên tài khoản có trong db FireBase mới

*Nếu tạo mới cơ sở dữ liệu trên FireBase thì các việc cần thay đổi trên code ESP8266:
	+ Nhập tên và mật khẩu wifi tương ứng đang muốn ESP8266 kết nối tới
	+ Nhập  Nhập Real Time Database URL
	+ Nhập Secret_key( vào project_settings trên firebase chọn Service acounts chọn Database secrets)

*Nguồn tham khảo cách cài đặt ESP32_cam
https://pigirl2020.blogspot.com/2021/07/send-datacaptured-image-from.html

*Nguồn tham khảo cách mã hóa file ảnh thành base64 và url
https://github.com/zenmanenergy/ESP8266-Arduino-Examples/find/master

*Nguồn tham khảo cách cấu hình chất lượng hình ảnh của ESP32-cam
https://ohtech.vn/all-courses/lap-trinh-esp32-cam-voi-arduino-ide/lessons/thay-doi-cai-dat-cho-esp32-cam-ov2640-camera-2/