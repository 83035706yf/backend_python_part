# Sciencetopia 后端 Python 部分

## 概述
Sciencetopia的后端Python部分专注于提供AI相关的功能，如生成学习计划。它使用Flask框架构建，并与OpenAI GPT-3.5模型集成。这个部分生成独立的API端口，和.NET编写的后端部分完全独立。

## 主要特性
- **生成学习计划**：基于用户提供的主题和描述，使用OpenAI GPT-3.5模型生成个性化学习计划。
- **测试接口**：提供一个测试接口，用于验证API的运行状态。

## 技术栈
- **Flask**：轻量级的Web应用框架。
- **OpenAI GPT-4o-mini**：用于生成学习计划的AI模型。
- **Swagger**：用于API文档的自动生成。

## 如何开始
1. **克隆仓库**：`git clone https://github.com/Sciencetopia-org/backend_python_part.git`
2. **安装依赖**：运行`pip install -r requirements.txt`安装所需依赖。
3. **设置环境变量**：确保设置了`OPENAI_API_KEY`环境变量。
4. **运行应用**：使用`python run.py`命令启动服务。

## API文档
- API文档通过Swagger自动生成，可在运行应用后访问`/swagger`查看。
