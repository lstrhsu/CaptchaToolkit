# Captcha Collection and Simple Recognition Tool

A toolkit for automatically collecting and simply recognizing captchas from Melon Ticket - Global. The tool includes two main functional modules: captcha collection and recognition.  
This project is more suitable for quickly preparing datasets. For deep learning solutions for corresponding captchas, please refer to [CapthcaDL](https://github.com/lstrhsu/CaptchaDL).

![Captcha Preview](https://github.com/lstrhsu/MyHost/blob/main/pics/captcha_130.png)

## Directory Structure
```
├── collect_captcha.py  # Captcha collection script
├── quick_ocr.py        # Captcha recognition script
├── requirements.txt    # Project dependencies
├── saved_captcha/      # Directory for saving captcha images
└── processed_captcha/  # Directory for processed captcha images
```

## Installation Steps

#### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

#### 2. Install Tesseract-OCR

Remember the installation path as it will be needed in `quick_ocr.py`.

Windows:
- Download and install [Tesseract-OCR](https://github.com/UB-Mannheim/tesseract/wiki)
- Default installation path: `C:\Program Files\Tesseract-OCR\`

macOS:
- Install using Homebrew:
  ```bash
  brew install tesseract
  ```
- Default installation path: `/usr/local/bin/tesseract`

## Usage Instructions

#### 1. Launch Chrome Browser
Run the following command in terminal:

Windows:
```bash
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:/Users/your_username/AppData/Local/Google/Chrome/User Data"
```

macOS:
```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --remote-debugging-port=9222 --user-data-dir="/Users/your_username/Library/Application Support/Google/Chrome"
```

Note:
- Replace "your_username" with your actual username
- If Chrome is installed in a different location, modify the path accordingly

Enter the Chrome browser, open the Melon Ticket - Global website, log in, and navigate to the ticket purchase popup page to ensure that the captcha image is displayed correctly.
   
![购票弹窗](https://github.com/lstrhsu/MyHost/blob/main/pics/melon_popup.png)

#### 2. Collect Captchas (collect_captcha.py)
Run the collection script:
```bash
python collect_captcha.py
```
The script will automatically:
- Connect to the opened Chrome browser
- Create saved_captcha folder (if it doesn't exist)
- Wait for user to press Enter to start collection
- Automatically collect 200 captcha images
- Save images in the saved_captcha folder

#### 3. Recognize Captchas (quick_ocr.py)
Run the recognition script:
```bash
python quick_ocr.py
```
The script will automatically:
- Check necessary directories and Tesseract installation
- Read images from saved_captcha
- Preprocess and perform OCR on each image
- Save original images to processed_captcha folder with recognition results as names

## File Description

#### collect_captcha.py
- Function: Automatically collect captcha images
- Workflow:
  1. Connect to opened Chrome browser
  2. Wait for user confirmation to start collection
  3. Loop to collect captcha images
  4. Automatically click refresh button for new captchas
  5. Save images to saved_captcha folder

#### quick_ocr.py
- Function: Recognize captcha image content
- Workflow:
  1. Read images from saved_captcha
  2. Preprocess images (add white background, invert colors, etc.)
  3. Use Tesseract-OCR for text recognition
  4. Save original images to processed_captcha folder with recognition results as names

## Important Notes

#### Environment Requirements:
- Python 3.6 or higher
- Chrome browser
- Windows operating system (other systems need path modifications)

#### Common Issues:
- If "Tesseract-OCR not found" appears, check installation path
- If unable to connect to Chrome, verify browser is properly launched
- If recognition rate is unsatisfactory, image preprocessing parameters may need adjustment

#### Folder Description:
- saved_captcha: Stores original captcha images
- processed_captcha: Stores processed images (named with recognized text)
- temp: Temporary folder (automatically created and deleted during execution)


## Disclaimer
This tool is for educational and research purposes only. Users should comply with the website's terms of service and relevant laws and regulations. The authors are not responsible for any misuse or potential consequences of using this tool.

For issues or suggestions, please submit an Issue.
