"""
本代码对应PDF文件中的“XSS 自动化工具运用与开发：Burp 插件深度联动：Jython 脚本实现复杂逻辑检测”
本代码用于在Burp Suite中检测XSS漏洞，使用Jython脚本实现。
"""

from burp import IBurpExtender, IScannerCheck, IScanIssue
from java.util import ArrayList
import urllib

class BurpExtender(IBurpExtender, IScannerCheck):
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        callbacks.setExtensionName("XSS Scanner")
        callbacks.registerScannerCheck(self)
        print("XSS Scanner loaded")
    
    def doPassiveScan(self, baseRequestResponse):
        return None
    def doActiveScan(self, baseRequestResponse, insertionPoint):
        # 构建测试 Payload
        payloads = ["<script>alert(1)</script>", "< img src=x onerror=alert(1)>"]
        issues = []
        for payload in payloads:
            checkRequest = insertionPoint.buildRequest(payload)
            checkResponse = self._callbacks.makeHttpRequest(
                baseRequestResponse.getHttpService(), checkRequest)
            responseInfo = self._helpers.analyzeResponse(checkResponse)
            body = checkResponse.tostring()
            if payload in body:
                issues.append(self._createIssue(baseRequestResponse, payload))
        return issues if issues else None
    
    def _createIssue(self, baseRequestResponse, payload):
        return self._callbacks.applyMarkers(
            self._helpers.createScanIssue(
                baseRequestResponse.getHttpService(),
                self._helpers.analyzeRequest(baseRequestResponse).getUrl(),
                [baseRequestResponse],
                "XSS Vulnerability",
                "A cross-site scripting vulnerability was detected with payload: " + payload,
                "High",
                "Certain"
            )
        )
    
    def consolidateDuplicateIssues(self, existingIssue, newIssue):
        return -1