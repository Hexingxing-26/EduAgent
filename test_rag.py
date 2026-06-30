import requests
import json

complex_question = """
请帮我分析以下Python代码的执行流程，并解释其中涉及的核心概念：

def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

def memoize(func):
    cache = {}
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper

@memoize
def optimized_fibonacci(n):
    if n <= 1:
        return n
    return optimized_fibonacci(n-1) + optimized_fibonacci(n-2)

# 调用测试
print(fibonacci(10))
print(optimized_fibonacci(10))

问题：
1. 普通递归和带装饰器的优化递归有什么区别？
2. 装饰器memoize是如何实现缓存的？
3. 这两种方式的时间复杂度分别是多少？
4. 如果我想限制缓存大小，应该如何修改memoize装饰器？
5. 请结合Python的闭包和函数式编程特性进行详细解释。
"""

payload = {'user_id': '1', 'message': complex_question}
r = requests.post('http://localhost:8000/chat', json=payload, timeout=120)
result = r.json()

print('=== 响应状态 ===')
print(f'Status: {r.status_code}')
print(f'Is Approved: {result.get("is_approved")}')
print()
print('=== 用户画像 ===')
print(json.dumps(result.get('profile'), ensure_ascii=False, indent=2))
print()
print('=== RAG检索结果 ===')
retrieved_docs = result.get('retrieved_docs', [])
print(f'检索到 {len(retrieved_docs)} 条相关文档')
for i, doc in enumerate(retrieved_docs[:3], 1):
    print(f'\n文档 {i}:')
    print(f'来源: {doc.get("source", "未知")}')
    content = doc.get('content', '')
    print(f'内容预览: {content[:300]}...')
print()
print('=== 生成的资源 ===')
resources = result.get('resources', [])
for i, resource in enumerate(resources, 1):
    print(f'\n资源 {i} ({resource.get("type", "未知")}):')
    content = resource.get('content', '')
    print(content[:800] + '...' if len(content) > 800 else content)
print()
print('=== 学习路径建议 ===')
learning_path = result.get('learning_path', '')
if learning_path:
    print(learning_path[:1000] + '...' if len(learning_path) > 1000 else learning_path)