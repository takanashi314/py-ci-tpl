## Overview

本稿では`pyproject.toml`の`[tool.ruff.format]`について述べる。

`uv run ruff format`で整形する。`uv run ruff format --check`は、ファイルを書き換えずに整形が必要かを確認する。

行の長さとインデント幅は`[tool.ruff]`で指定する。本構成では`line-length = 88`と`indent-width = 4`を明示している。


## Style

### `indent-style`

インデントに使う文字。`"space"`は、インデント1段に`[tool.ruff]`の`indent-width`で指定した数のスペースを使う。`"tab"`は、1段にタブ1文字を使い、行の長さの計算には`indent-width`をタブの幅として使う。

本構成では未指定とする。既定の`"space"`と`indent-width = 4`の組み合わせで、1段が4スペースになる。

- 型: `str`（`"space"`・`"tab"`）
- 既定値：`"space"`
- 設定値：未指定

> [!CAUTION]
> `"tab"`を指定した状態で`W191`（タブによるインデント）を有効にすると、`ruff format`は設定の衝突を警告する。

### `quote-style`

文字列リテラルを囲む引用符の指定。`"double"`は二重引用符、`"single"`は一重引用符を優先する。`"preserve"`は元の引用符を維持する。

本構成では未指定とする。既定の`"double"`を使う。

- 型: `str`（`"double"`・`"single"`・`"preserve"`）
- 既定値：`"double"`
- 設定値：未指定

> [!TIP]
> エスケープを減らせる場合、優先設定と異なる引用符が使われることがある。例えば、`"double"`を指定しても`'say "hi"'`は一重引用符のまま残る。三重引用符の文字列やdocstringでは、`"single"`を指定しても`"""`を優先する。

> [!CAUTION]
> `Q000`または`Q003`が有効で、`lint.flake8-quotes.inline-quotes`と`quote-style`の一方が`"single"`、もう一方が`"double"`の場合、`ruff format`は警告する。`Q001`と`Q002`は、それぞれ`multiline-quotes`と`docstring-quotes`で引用符を指定する。

### `nested-string-quote-style`

f文字列などの補間式（`{...}`）に含まれる文字列の引用符を指定する。`"alternating"`は外側と内側で異なる引用符を使い、`"preferred"`は内側にも`quote-style`を適用する。

本構成では未指定とする。既定の`"alternating"`を使う。

- 型: `str`（`"alternating"`・`"preferred"`）
- 既定値：`"alternating"`
- 設定値：未指定

`quote-style = "double"`の場合の整形例。

```python
f"{data['name']}"  # alternating
f"{data["name"]}"  # preferred
```

> [!TIP]
> この項目は整形対象のPythonバージョンが3.12以上の場合に効く。上の例で外側と内側に同じ引用符を使えるのはPython 3.12以降である。本構成では、通常の設定探索で`requires-python = "==3.15.*"`から`py315`が推測される。

### `line-ending`

整形時に使う改行コード。

- `"auto"`はファイルごとに最初に検出した改行コードにそろえる。改行がなければLFを使う。
- `"lf"`はLF（`\n`）にそろえる。
- `"cr-lf"`はCRLF（`\r\n`）にそろえる。
- `"native"`はWindowsでCRLF、それ以外ではLFを使う。

本構成では"auto"を明示的に記載する。

Windowsなどで本構成を利用して、何か不具合があったときに、この項目について確認しやすいようにするため。

- 型: `str`（`"auto"`・`"lf"`・`"cr-lf"`・`"native"`）
- 既定値：`"auto"`
- 設定値：`"auto"`

> [!CAUTION]
> `"lf"`を指定した状態で、整形対象のファイルがGitによってCRLFでチェックアウトされると、`ruff format --check`で未整形と判定され得る。Git側でチェックアウト時の改行コードを指定する場合は`.gitattributes`の`eol`を使う。

### `skip-magic-trailing-comma`

既存の末尾カンマを複数行に展開する合図として扱うかどうか。`false`では、1行に収まる引数リストなども末尾カンマを手掛かりに複数行に整形する。`true`ではその合図を無視するため、レイアウトが1行にまとまることがある。

本構成では未指定とする。既定の`false`により、末尾カンマで複数行のレイアウトを選べる。

- 型: `bool`
- 既定値：`false`
- 設定値：未指定

> [!CAUTION]
> この項目を`true`にした場合、`I001`（import文の並べ替え）が有効で、`[tool.ruff.lint.isort]`の`force-single-line = false`と`split-on-trailing-comma = true`がそろうと、`ruff format`は設定の衝突を警告する。

## File Selection

### `exclude`

整形対象から追加で外すファイルのglobパターン。`[tool.ruff]`の`exclude`や`extend-exclude`による共通の除外に加えて、`ruff format`に適用される。ディレクトリを探索する場合、パターンは見つかったファイルのパス全体とファイル名に照合される。

本構成では未指定とする。ディレクトリを探索する際は、`[tool.ruff]`の`include`にある`src/**/*.py`、`tests/**/*.py`、`scripts/**/*.py`が整形の候補になる。`pyproject.toml`は設定として読み込まれ、整形の対象から外れる。

- 型: `list[str]`
- 既定値：`[]`
- 設定値：未指定

例えば、生成コードをlintの対象に含めつつ、`src/generated/`配下を再帰的に整形の対象から外す場合は、配下のファイルのパスに一致するパターンを書く。

```toml
[tool.ruff.format]
exclude = ["src/generated/**"]
```

> [!CAUTION]
> ファイルをコマンドに直接渡したときも除外を適用するには、`[tool.ruff]`で`force-exclude = true`を指定するか、`ruff format --force-exclude`を使う。

## Docstrings

### `docstring-code-format`

docstring内のPythonコード例を整形するかどうか。doctest形式、Markdownのフェンス付きコードブロック、reStructuredTextのリテラルブロックやコードブロックなどが対象になる。入力や整形結果が無効なPythonコードになる場合は、その例をそのまま残す。

本構成では未指定とする。既定の`false`では、docstring内のコード例はこの機能による整形の対象から外れる。

- 型: `bool`
- 既定値：`false`
- 設定値：未指定

> [!CAUTION]
> この項目を`true`にすると、言語指定のないMarkdownのフェンス付きコードブロックやreStructuredTextのリテラルブロックも、Pythonとして解析できれば整形の対象になる。例えば、JSONのつもりで書いた`{"a":1}`が`{"a": 1}`に整形される。

### `docstring-code-line-length`

docstring内のコード例を折り返す際の行の長さの目安。`"dynamic"`では、`[tool.ruff]`の`line-length`からdocstring内外のインデント幅を差し引いて、コード例に使える行幅を決める。整数を指定した場合は、その値をコード例の行幅の目安とする。

本構成では未指定とする。この項目が効くのは`docstring-code-format = true`の場合である。

- 型: `int`（または`"dynamic"`）
- 既定値：`"dynamic"`
- 設定値：未指定

> [!TIP]
> 整数を指定した場合、インデントを含む整形後の行が`line-length`を超えることがある。

## Others

### `preview`

Ruffにおける開発中のスタイルを整形に適用するかどうか。未指定の場合は`[tool.ruff]`の`preview`を引き継ぐ。

本構成では未指定とする。上位の`preview`も未指定なので、整形にpreviewスタイルは適用されない。

- 型: `bool`
- 既定値：`false`（上位の`preview`も未指定の場合）
- 設定値：未指定

> [!TIP]
> `[tool.ruff]`で`preview = true`を指定した状態で、`[tool.ruff.format]`に`preview = false`を書くと、整形だけをpreviewモードから外せる。

## References

- [Ruffの設定一覧（`format`）](https://docs.astral.sh/ruff/settings/#format)
- [Ruff 0.17.2の`FormatOptions`定義](https://github.com/astral-sh/ruff/blob/0.17.2/crates/ruff_workspace/src/options.rs#L3999-L4312)
- [Ruff 0.17.2のフォーマッタ公式ガイド](https://github.com/astral-sh/ruff/blob/0.17.2/docs/formatter.md)
- [フォーマッタの設定衝突を検出する条件](https://github.com/astral-sh/ruff/blob/0.17.2/crates/ruff/src/commands/format.rs#L1083-L1266)
- [Gitの`eol`属性](https://git-scm.com/docs/gitattributes#_eol)
