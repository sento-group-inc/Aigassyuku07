#!/usr/bin/env python3
"""JEVのAPIキーを、画面に出さずに保存する。

キーはホーム配下の`~/.config/typesafe/api-key`（本人所有600・親700）へ保存する。
環境変数や引数からは受け取らない。`--replace`以外では既存のキーを上書きしない。
"""

import argparse
import getpass
import json
import os
import stat
import sys
import urllib.error
import urllib.request
from pathlib import Path

KEY_PATH = Path.home() / ".config" / "typesafe" / "api-key"
ENDPOINT = "https://api.typesafe.ai/v1/systemone"


def validate(value):
    value = value.strip()
    if not 1 <= len(value) <= 4096 or any(not 33 <= ord(c) <= 126 for c in value):
        raise ValueError("キーの形式を確認してください（空白や改行が混ざっていませんか）。")
    return value


def save(value, replace):
    path = KEY_PATH
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    info = path.parent.lstat()
    if not stat.S_ISDIR(info.st_mode) or stat.S_IMODE(info.st_mode) & 0o077:
        raise RuntimeError(f"{path.parent} は権限700にしてください。")
    if path.exists() and not replace:
        raise FileExistsError(f"{path} は既にあります。置き換えるなら --replace を付けてください。")
    flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC | os.O_NOFOLLOW
    descriptor = os.open(path, flags, 0o600)
    with os.fdopen(descriptor, "w") as output:
        output.write(value + "\n")
        output.flush()
        os.fsync(output.fileno())
    os.chmod(path, 0o600)
    return path


def load():
    for name in ("JEV_API_KEY", "TYPESAFE_API_KEY"):
        if os.environ.get(name, "").strip():
            return validate(os.environ[name])
    if KEY_PATH.exists():
        return validate(KEY_PATH.read_text("utf-8"))
    raise FileNotFoundError("キーがまだありません。先に保存してください。")


def verify(key):
    body = json.dumps(
        {
            "model": "jev-latest",
            "state": "AI合宿の疎通確認です。",
            "questions": {"reachable": {"type": "noul", "instructions": "This request was received."}},
        }
    ).encode()
    request = urllib.request.Request(
        ENDPOINT,
        data=body,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--replace", action="store_true", help="既存のキーを置き換える")
    parser.add_argument("--verify", action="store_true", help="保存後に1回だけAPIを呼んで確認する")
    args = parser.parse_args()

    try:
        if args.replace or not KEY_PATH.exists():
            print("JEVのAPIキーを貼り付けてください（入力は画面に表示されません）。")
            value = validate(getpass.getpass("API key: "))
            path = save(value, replace=args.replace)
            print(f"保存しました: {path}（権限600）")
        else:
            print(f"既に登録済みです: {KEY_PATH}（変更するなら --replace）")
    except (ValueError, RuntimeError, FileExistsError) as error:
        sys.exit(str(error))

    if args.verify:
        try:
            result = verify(load())
        except urllib.error.HTTPError as error:
            sys.exit(f"APIがエラーを返しました: HTTP {error.code}。キーと契約状態を確認してください。")
        except Exception as error:  # ネットワーク断はここへ来る
            sys.exit(f"APIへ接続できませんでした: {type(error).__name__}")
        print("接続に成功しました。")
        print(json.dumps({"model": result.get("model"), "answers": result.get("answers")}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
