ruce自动化测试工具简介：

1，如测是一个规范化的http接口测试工具，目前支持对http请求的get和post协议测试。

2，如测完成的工作就是对一个或者多个http请求接口的数据校验工作。

3，如测是基于unittest的一个http测试框架，编写测试用例风格与unitest相似。


ruce依赖：

1，引入新的requests包来分析http请求.

2，引入新的模板包jinjia2来处理模板文件。

3，引入yaml包来使用配置文件管理的功能。

4，依赖包均在depends目录中,直接安装上去即可

5，Python版本仅在Python2.7.6版本以上测试,理论2.7版本的均可以使用本包。


ruce新增功能：

1，开发了pyshell来处理Python执行shell的逻辑，执行本地shell的逻辑与返回结果形式参考fabric。

2，颜色输出（只针对Linux操作系统）。


ruce安装方法：

1，先安装依赖参考require.txt

2，执行命令python setup.py install 进行安装。


ruce使用教程：

1，编写启动ruce脚本run.py：

   from ruce import main
  
   if __name__=='__main__':
      
       main.run()

2，执行命令：python run.py --help 查看命令行帮助信息。

3，执行命令：python run.py --gen_conf='env_name=host:port',生成配置文件。
   其中host和port需要替换为要测试的接口。
 
   生成文件ruce.conf.yml

4，执行命令：python run.py --gen_tpl=case_name， 生成测试case_name的测试文件模板，其中case_name替换为要测试的case接口名称。
 
   生成文件test_case_name.py
5，编辑test_case_name.py完成测试用例的填写。

6，执行python test_case_name.py 来检验测试用例。

7，执行python run.py 来执行所有的测试用例。


