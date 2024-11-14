
# Web Scraping & AI Interaction with Flask API

This project is a web scraping and AI interaction system that integrates with a Microsoft Copilot-like platform using Selenium, Flask, and various utilities. It fetches messages from an AI platform, processes the data, and serves it via a Flask API.

---

## Özellikler

- **Web Scraping**: Selenium ile, bir web sitesinden AI mesajlarını çekme ve bunları işleme.
- **Mesaj İşleme**: AI tarafından gönderilen mesajlarda ön ek (prefix) temizleme ve özel kelime değişiklikleri yapma.
- **Resim Tespiti**: AI mesajlarındaki resim bağlantılarını kontrol etme.
- **Kod Blokları**: AI mesajlarından kod bloklarını çıkarma.
- **Flask API**: Web üzerinden yapılan istekleri işleyerek yanıtlar sağlama.
- **Cookies ve LocalStorage Kaydetme**: Tarayıcıda oturum bilgilerini kaydetme ve tekrar yükleme.
- **API Anahtarı Doğrulaması**: Güvenlik amacıyla API anahtarları ile doğrulama.

---

## Kurulum

### Gereksinimler

- Python 3.x
- Selenium
- Flask
- ChromeDriver
- Google Chrome
- API Anahtarları ve **settings.json** dosyası

### Adımlar

1. **Python Bağımlılıklarını Yükleyin**:
   ```bash
   pip install -r requirements.txt
   ```

2. **ChromeDriver ve Google Chrome**: 
   Tarayıcı sürümünüze uygun ChromeDriver'ı [buradan](https://sites.google.com/a/chromium.org/chromedriver/) indirip projenizin kök dizinine yerleştirin.

3. **settings.json**:
   `settings.json` dosyasını aşağıdaki örneğe göre yapılandırın:

   ```json
   {
     "driver": {
       "chrome_driver_path": "path/to/chromedriver",
       "user_agent": "your_user_agent"
     },
     "api": {
       "keys_file": "keys.txt",
       "response_messages": {
         "ai_message": "ai_message",
         "code_blocks": "code_blocks",
         "img_link": "img_link"
       }
     },
     "cookies_path": "cookies.pkl",
     "localstorage_path": "localstorage.pkl",
     "log_messages": {
       "login_prompt": "Please log in.",
       "error_occurred": "An error occurred",
       "server_started": "Server started successfully"
     },
     "xpath_code_blocks": "//pre[@class='code-block']",
     "xpath_user_input": "//textarea[@id='input']",
     "xpath_ai_message": "//div[@class='ai-message']",
     "xpath_img_container": "//div[@class='img-container']",
     "img_link_check_timeout": 10
   }
   ```

4. **API Anahtarları**:
   `keys.txt` dosyasına, API anahtarlarınızı her satıra bir anahtar olacak şekilde ekleyin.

5. **Flask Sunucusunu Başlatın**:
   Projeyi başlatmak için:
   ```bash
   python app.py
   ```

---

## API Kullanımı

### Endpoint

`GET /api`

### Parametreler

- **yazi**: AI'ya gönderilecek yazı.
- **key**: API anahtarınız.

### Örnek İstek

```bash
curl "http://localhost:5000/api?yazi=Merhaba&key=your_api_key"
```

### Yanıt Örneği

```json
{
  "ai_message": "Hello, how can I help you?",
  "code_blocks": "def example(): pass",
  "img_link": "https://example.com/image.jpg"
}
```

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Features

- **Web Scraping**: Fetch and process AI messages from a website using Selenium.
- **Message Processing**: Clean up prefixes and replace specific words in AI-generated messages.
- **Image Detection**: Check for image links in AI messages.
- **Code Block Extraction**: Extract code blocks from AI responses.
- **Flask API**: Serve requests over a Flask API.
- **Cookies and LocalStorage**: Save and load session information in the browser.
- **API Key Authentication**: Secure the API using API keys.

---

## Installation

### Requirements

- Python 3.x
- Selenium
- Flask
- ChromeDriver
- Google Chrome
- API Keys and **settings.json** file

### Steps

1. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **ChromeDriver and Google Chrome**: 
   Download the correct version of ChromeDriver from [here](https://sites.google.com/a/chromium.org/chromedriver/) and place it in the root directory of your project.

3. **settings.json**:
   Configure your `settings.json` file as shown below:

   ```json
   {
     "driver": {
       "chrome_driver_path": "path/to/chromedriver",
       "user_agent": "your_user_agent"
     },
     "api": {
       "keys_file": "keys.txt",
       "response_messages": {
         "ai_message": "ai_message",
         "code_blocks": "code_blocks",
         "img_link": "img_link"
       }
     },
     "cookies_path": "cookies.pkl",
     "localstorage_path": "localstorage.pkl",
     "log_messages": {
       "login_prompt": "Please log in.",
       "error_occurred": "An error occurred",
       "server_started": "Server started successfully"
     },
     "xpath_code_blocks": "//pre[@class='code-block']",
     "xpath_user_input": "//textarea[@id='input']",
     "xpath_ai_message": "//div[@class='ai-message']",
     "xpath_img_container": "//div[@class='img-container']",
     "img_link_check_timeout": 10
   }
   ```

4. **API Keys**:
   Add your API keys to `keys.txt`, one key per line.

5. **Start the Flask Server**:
   To run the project:
   ```bash
   python app.py
   ```

---

## API Usage

You can use the API like this:

### Endpoint

`GET /api`

### Parameters

- **yazi**: The text to send to the AI.
- **key**: Your API key.

### Example Request

```bash
curl "http://localhost:5000/api?yazi=Hello&key=your_api_key"
```

### Example Response

```json
{
  "ai_message": "Hello, how can I help you?",
  "code_blocks": "def example(): pass",
  "img_link": "https://example.com/image.jpg"
}
```

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
