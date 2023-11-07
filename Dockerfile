# 파이썬 베이스 이미지 사용
FROM python:3.11.3

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 패키지 및 도구 설치
RUN apt-get update && \
    apt-get install -y wget unzip && \
    apt-get install -y libx11-xcb1 libxcomposite1 libxi6 libxrandr2 libasound2 libpangocairo-1.0-0 libatk1.0-0 libatk-bridge2.0-0 libgtk-3-0 libnss3

# Chrome 및 ChromeDriver 설치
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt-get install -y ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb

RUN wget https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/119.0.6045.105/linux64/chromedriver-linux64.zip && \
    unzip chromedriver-linux64.zip && \
    mv chromedriver-linux64/chromedriver /usr/bin/chromedriver && \
    chmod +x /usr/bin/chromedriver && \
    rm chromedriver-linux64.zip

# 환경 변수 설정
ENV GOOGLE_CHROME_BIN /usr/bin/google-chrome
ENV CHROMEDRIVER_PATH /usr/bin/chromedriver

# 의존성 파일 복사 및 설치
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# 애플리케이션 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
