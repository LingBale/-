//本代码对应XSS 防御与浏览器对抗：浏览器原生防御：Trusted Types：创建 Trusted Types
//本示例展示了如何使用 Trusted Types 策略来创建安全的 HTML 内容。
//对于动态生成的 HTML 内容，使用 Trusted Types 策略可以防止 XSS 攻击。

// 创建一个策略
const policy = trustedTypes.createPolicy('myPolicy', {
  createHTML: (input) => {
    // 消毒或转义用户输入
    return DOMPurify.sanitize(input);
  },
  createScript: (input) => {
    // 通常应避免创建脚本
    throw new Error('不允许动态脚本');
  }
});

// 使用策略
element.innerHTML = policy.createHTML(userInput);  // ✅ 安全
// element.innerHTML = userInput;  // ❌ 被 CSP 阻止