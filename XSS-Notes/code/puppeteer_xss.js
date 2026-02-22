/* 
本代码对应PDF文件中的“XSS 自动化工具运用与开发：自定义脚本开发：JPython + Selenium/Puppeteer/Playwright构建动态扫描器”
本代码用于测试XSS漏洞，使用Playwright库进行自动化测试。
*/


const puppeteer = require('puppeteer');

(async () => {
    const browser = await puppeteer.launch({ headless: false });
    const page = await browser.newPage();
    
    page.on('dialog', async dialog => {
        console.log('Alert:', dialog.message());
        await dialog.dismiss();
    });
    
    await page.goto('http://target.com/search?q=<script>alert(1)</script>');
    await browser.close();
})();