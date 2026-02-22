/* 
本代码对应PDF文件中的“XSS 自动化工具运用与开发：自定义脚本开发：Tampermonkey 用户脚本辅助手工测试”
本代码用于测试XSS漏洞，使用Tampermonkey用户脚本辅助手工测试。
*/
// ==UserScript==
// @name         XSS Helper
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  Add XSS test parameters to all links
// @author       You
// @match        *://*/*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';
    document.querySelectorAll('a').forEach(link => {
        let url = new URL(link.href);
        if (!url.searchParams.has('xss_test')) {
            url.searchParams.set('xss_test', '<script>alert(1)</script>');
            link.href = url.toString();
        }
    });
})();