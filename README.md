# Captcha Collection and Simple Recognition Tool

A toolkit for automatically collecting and simple recognizing captchas from Melon Ticket - Global. The tool includes two main functional modules: captcha collection and recognition.

![Captcha Preview](image.png)

## Directory Structure
```
├── collect_captcha.py  # Captcha collection script
├── quick_ocr.py        # Captcha recognition script
├── requirements.txt    # Project dependencies
├── saved_captcha/      # Directory for saving captcha images
└── processed_captcha/  # Directory for processed captcha images
```

## Installation Steps

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. Install Tesseract-OCR
1. Visit [Tesseract-OCR Download Page](https://github.com/UB-Mannheim/tesseract/wiki)
2. Download and install Tesseract-OCR (Windows users should choose the Windows version)
3. Default installation path: `C:\Program Files\Tesseract-OCR\`
4. Remember the installation path as it will be needed later

## Usage Instructions

### 1. Launch Chrome Browser
Run the following command in terminal:
```bash
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:/Users/your_username/AppData/Local/Google/Chrome/User Data"
```
Note:
- Replace "your_username" with your actual Windows username
- If Chrome is installed in a different location, modify the path accordingly
  
Enter the Chrome browser, open the Melon Ticket - Global website, log in, and navigate to the ticket purchase popup page to ensure that the captcha image is displayed correctly.
   
![购票弹窗](popup.png)

### 2. Collect Captchas (collect_captcha.py)
1. Run the collection script:
```bash
python collect_captcha.py
```
2. The script will automatically:
   - Connect to the opened Chrome browser
   - Create saved_captcha folder (if it doesn't exist)
   - Wait for user to press Enter to start collection
   - Automatically collect 200 captcha images
   - Save images in the saved_captcha folder

### 3. Recognize Captchas (quick_ocr.py)
1. Run the recognition script:
```bash
python quick_ocr.py
```
2. The script will automatically:
   - Check necessary directories and Tesseract installation
   - Read images from saved_captcha
   - Preprocess and perform OCR on each image
   - Save original images to processed_captcha folder with recognition results as filenames

## File Description

### collect_captcha.py
- Function: Automatically collect captcha images
- Workflow:
  1. Connect to opened Chrome browser
  2. Wait for user confirmation to start collection
  3. Loop to collect captcha images
  4. Automatically click refresh button for new captchas
  5. Save images to saved_captcha folder

### quick_ocr.py
- Function: Recognize captcha image content
- Workflow:
  1. Read images from saved_captcha
  2. Preprocess images (add white background, invert colors, etc.)
  3. Use Tesseract-OCR for text recognition
  4. Save original images to processed_captcha folder with recognition results as names

## Important Notes

1. Environment Requirements:
   - Python 3.6 or higher
   - Chrome browser
   - Windows operating system (other systems need path modifications)

2. Common Issues:
   - If "Tesseract-OCR not found" appears, check installation path
   - If unable to connect to Chrome, verify browser is properly launched
   - If recognition rate is unsatisfactory, image preprocessing parameters may need adjustment

3. Folder Description:
   - saved_captcha: Stores original captcha images
   - processed_captcha: Stores processed images (named with recognized text)
   - temp: Temporary folder (automatically created and deleted during execution)


## Disclaimer
This tool is for educational and research purposes only. Users should comply with the website's terms of service and relevant laws and regulations. The authors are not responsible for any misuse or potential consequences of using this tool.

For issues or suggestions, please submit an Issue.
