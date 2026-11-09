## Overview
本稿では本リポジトリのブランチ戦略について述べる。

## Branches

| ブランチ | 役割 | 作成元 | マージ先 | マージ後 |
|---|---|---|---|---|
| `main` | リリース可能な状態を保つ | - | - | - |
| `feature/<tool>` | 1つのツールの導入作業をまとめる | `main` | `main` | 残す |
| `dev/<tool>/<topic>` | ツール導入の中の個別作業 | `feature/<tool>` | `feature/<tool>` | 残す |
| `docs/<topic>` | プロジェクト共通の文書 | `main` | `main` | 削除する |
| `fix/<topic>` | `main`に入ったツールの小さな誤りの修正 | `main` | `main` | 削除する |

```text
main
 ├─ feature/<tool>
 │   └─ dev/<tool>/<topic>
 ├─ docs/<topic>
 └─ fix/<topic>
```

- `<tool>`にはツール名を、`<topic>`には作業内容をケバブケースの短い英単語で入れる(例：`feature/ruff`、`dev/ruff/ruff-config`)。
- `main`への反映はツール単位とし、導入途中のツールが他のツールの作業に影響しないようにする。
- `dev/<tool>/<topic>`では1つの作業だけを扱う。
- `fix/<topic>`では誤りの修正だけを扱う。設定や機能の追加は`feature/<tool>`と`dev/<tool>/<topic>`で扱う。
- `docs`/`fix`ブランチは数が多くなりやすいため、マージ後に削除する。コミットとPull Requestのページは残る。

文書の作業は、次の区別でブランチを選ぶ。

| 作業 | ブランチ |
|---|---|
| 導入中のツールの設定・説明 | `dev/<tool>/<topic>` |
| `main`に入ったツールの設定・説明の誤り | `fix/<topic>` |
| プロジェクト共通の文書、複数の文書の表記の統一 | `docs/<topic>` |

## Merge

- `main`と`feature/<tool>`には直接pushせず、Pull Requestでマージする。
- マージには「Create a merge commit」を使う。ブランチの分岐と合流を履歴に残すためである。
- `main`の変更を`feature/<tool>`に取り込む場合は、`main` → `feature/<tool>`のPull Requestでマージする。`dev/<tool>/<topic>`には、更新後の`feature/<tool>`を取り込む。

## Pull Request

Pull Requestは、対応するIssueを1つ参照する。ただし、次のPull Requestは、Issueを作らない。

- `docs/<topic>`・`fix/<topic>`のうち、既存のファイルの中身の修正だけを行うもの(ファイルの追加・削除・名前の変更・移動を含むものは、Issueを作る)
- `main`の変更を取り込むだけのもの

Issueを作らない場合は、変更の理由をPull Requestの本文に書く。

| マージ先 | Issueの参照 | Issueを閉じる方法 |
|---|---|---|
| `feature/<tool>` | `Refs #<番号>` | 完了条件を満たした時点で手動で閉じる |
| `main` | `Closes #<番号>` | マージ時に自動で閉じる(既定ブランチでのみ働く) |

## GitHub Settings

本稿のルールは、次のGitHubの設定を前提とする。テンプレートからは引き継がれないため、リポジトリ作成後に設定する。

### General

| 設定 | 値 |
|---|---|
| Allow merge commits | 有効 |
| Allow squash merging | 無効 |
| Allow rebase merging | 無効 |
| Automatically delete head branches | 無効(`dev`ブランチを残すため) |
| Default commit message | Pull request title |

### Rulesets

「Enforcement status」は`Active`とし、「Bypass list」には誰も追加しない。

| ルール | `main`用 | `feature`用 |
|---|---|---|
| Target branches | Default branch | `feature/**` |
| Restrict deletions | 有効 | 有効 |
| Block force pushes | 有効 | 有効 |
| Require a pull request before merging | 有効 | 有効 |
| Required approvals | 0(個人開発のため) | 0(個人開発のため) |
| Allowed merge methods | Merge | Merge |

CIの導入時に、両方のルールセットで「Require status checks to pass」を有効にする。

## Commit Message

Conventional Commits(`<type>(<scope>): <summary>`)に従う(例：`docs(tool.ruff): add tool-ruff.md`)。

マージコミットは対象外であり、`Default commit message: Pull request title`を変更しない。
つまり、`PR-title (#NN)`の形式となっているのが正しい。
例外として、#1 と #4 は、方針を決定する前のものなので、形式が異なっている。

| `<type>` | 用途 |
|---|---|
| `feat` | 機能の追加 |
| `fix` | 誤りの修正 |
| `docs` | 文書の追加・修正 |
| `refactor` | 動作を変えない整理 |
| `chore` | 設定・依存関係など、上記以外の変更 |
