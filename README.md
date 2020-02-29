# Upload2MoneyForward
This program is to register expenses and incomes to MoneyForward by uploading csv files.  

## Description
This program is to regsiter expenses and incomes data to MoneyForward by uploading csv files.

## Features
- regsiter expenses and income data to MoneyForward by uploading csv files 
- You can use some parameter following:  
  日付,大分類,中分類,備考,金額

## Requirement
- Python 3.6.3 or later  
- selenium 3.141 or later  
- Chrome
- ChromeDriver


## Usage
1. Install dependencies:  

   ```shell
   $ pip install selenium
   $ # You can install proper version with following command.
   $ pip install chromedriver-binary~=`google-chrome --version \
    | perl -pe 's/([^0-9]+)([0-9]+\.[0-9]+).+/$2/g'`
   ```
2. Create .env file to set username and password.

   ```
   $ cat .env
   USERNAME="hoge@gmail.com"
   PASSWORD='password'
   ```
3. Input file format
This program only allow following CSV format:  
```日付,大分類,中分類,備考,金額```  
You can see sample data from "sample.csv"

## Running Tests
You can execute this program using:  
```python uploadCSVtoMF.py sample.csv```

## Author
- [yysosuke](https://twitter.com/yyosuke)
- [hssay](https://twitter.com/a_hssay)

## License
[GPL](https://github.com/yyosuke/Upload2MoneyForward/blob/master/LICENSE)
