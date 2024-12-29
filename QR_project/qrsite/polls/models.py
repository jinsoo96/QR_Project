from django.db import models


class QRCodeModel(models.Model):
    file_path = models.CharField(max_length=255)  # QR 코드 파일 경로
    user_input = models.TextField()               # 사용자 입력
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 날짜 및 시간

    def __str__(self):
        return f"QR Code for {self.user_input[:50]}"