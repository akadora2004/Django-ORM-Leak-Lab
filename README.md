# Django ORM Leak Lab

このプロジェクトは、Django の ORM に潜む「ORM Leaking（ORM インジェクション）」脆弱性を検証・再現するためのデモアプリケーションです。

PortSwiggerの「[Top 10 web hacking techniques of 2025](https://portswigger.net/research/top-10-web-hacking-techniques-of-2025)」で第2位に選出された手法をベースにしています。</br>
SQLインジェクション対策がなされている現代的な Web アプリにおいても、ORM の不適切な利用が致命的な情報漏洩に繋がることを示します。

---

## 🔧 技術スタック

- Python 3.12-slim
- Django 5.x / 6.x
- SQLite3
- Docker / Docker Compose

## 🚀 セットアップ

Docker が使える環境で以下を実行します。

```bash
git clone <リポジトリURL>
cd Django-ORM-Leak-Lab
docker compose up -d --build
```

データベースを初期化し、サンプルデータを投入します。

```bash
docker compose exec django python manage.py migrate
docker compose exec django python manage.py shell < main/seed.py
```

---

## 🔍 脆弱性の解説

脆弱な実装は `main/views.py` にあります。

```python
def index(request):
    query_params = request.GET.dict()
    # 【脆弱性の原因】ユーザー入力を検証せずに ORM の引数として展開している
    results = Employee.objects.filter(**query_params)
    return render(request, 'main/index.html', {'results': results})
```

`request.GET` の内容をそのまま `filter(**query_params)` に渡すと、`__startswith` などの Django ルックアップを攻撃者に悪用され、意図しないカラムで検索される可能性があります。

---

## 🎯 攻撃シナリオ

攻撃者は `private_token` というカラムの存在を推測、特定したと仮定します。
1. 初期状態: 攻撃者は「田中 太郎」のトークンを一切知りません。

2. ブルートフォース攻撃: `__startswith` などのルックアップを利用したURLを生成します。

   `/?name=田中 太郎&private_token__startswith=a` -> 「0件」

   `/?name=田中 太郎&private_token__startswith=s` -> 「1件見つかりました」

3. 推論: サーバーの応答（真偽値）を観察することで、トークンを一文字ずつ特定（リーク）させます。

   ```text
   /?name=田中 太郎&private_token__startswith=a
   /?name=田中 太郎&private_token__startswith=s
   ```

- `a` の場合: `0件`
- `s` の場合: `1件`

上記を繰り返すことで、secret_id_1252 のような機密情報を完全に特定します。

---

## 🛡️ 対策

「`カラム名 = 値` で書く方法」

```python
name = request.GET.get('name')
department = request.GET.get('department')

results = Employee.objects.all()
if name:
    results = results.filter(name=name)
if department:
    results = results.filter(department=department)
```

`private_token` なんてコードに書いていない以上、外部から何を送り込まれても絶対に漏洩しません。
