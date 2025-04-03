# accounts/email_validate.py
from django.core.mail.backends.smtp import EmailBackend
import ssl
import smtplib


class CustomEmailBackend(EmailBackend):
    """
    SSL 인증서 검증을 우회하기 위한 커스텀 백엔드 (보안 환경에서만 임시로 사용 권장)
    """

    def open(self):
        """
        Django의 EmailBackend.open()을 오버라이드하여
        연결 시 SSL 인증서 검증을 우회하도록 SSLContext 설정
        """
        if self.connection:
            return False

        try:
            self.connection = smtplib.SMTP(
                self.host,
                self.port,
                local_hostname="email.ap-northeast-2.amazonaws.com",
                timeout=20000,
            )
            # Debug 설정
            if self.use_debug_level:
                self.connection.set_debuglevel(1)

            # TLS(STARTTLS) 사용 시, 인증 우회 SSLContext 적용
            if self.use_tls:
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                self.connection.ehlo()
                self.connection.starttls(context=context)
                self.connection.ehlo()

            if self.username and self.password:
                self.connection.login(self.username, self.password)

            return True
        except Exception:
            if self.fail_silently:
                return False
            else:
                raise

    def close(self):
        """기존과 동일"""
        super().close()

    def send_messages(self, email_messages):
        """
        부모 클래스의 send_messages를 그대로 사용(권장).
        open(), close() 내부에서 인증 우회 처리를 하므로,
        특별히 이 부분을 직접 재정의하지 않아도 됩니다.
        """
        return super().send_messages(email_messages)
