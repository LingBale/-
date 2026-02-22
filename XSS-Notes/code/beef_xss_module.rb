"""
本代码对应PDF文件中的“XSS 自动化工具运用与开发：自定义脚本开发：BeEF实战:自定义模块开发”
本代码用于测试XSS漏洞，使用BeEF模块开发自定义模块。
"""

# modules/example/example.rb
class Example < BeEF::Core::Command
  def self.options
    @configuration = BeEF::Core::Configuration.instance
    return [
      {'name' => 'message', 'type' => 'textarea', 'value' => 'Hello', 'description' => 'Message to alert'}
    ]
  end

  def post_execute
    content = {}
    content['result'] = @datastore['result']
    save content
  end
end