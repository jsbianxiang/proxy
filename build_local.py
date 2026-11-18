from pathlib import Path

ROOT = Path(__file__).resolve().parent
SUB_FILE = ROOT / "subscriptions.local.txt"
TEMPLATES = ["mihomo.yaml", "mihomo_smart.yaml"]


def read_subscriptions():
    if not SUB_FILE.exists():
        raise SystemExit("找不到 subscriptions.local.txt")
    links = []
    for raw in SUB_FILE.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if not line.startswith(("http://", "https://")):
            raise SystemExit(f"订阅链接必须以 http(s) 开头: {line}")
        links.append(line)
    if len(links) > 4:
        raise SystemExit("最多支持 4 条订阅链接")
    return links


def main():
    links = read_subscriptions()
    for name in TEMPLATES:
        text = (ROOT / name).read_text(encoding="utf-8")
        for index in range(1, 5):
            token = f"订阅链接{index}"
            if index <= len(links):
                text = text.replace(token, links[index - 1])
            else:
                print(f"警告: {name} 的 {token} 未填写，保留占位符")
        output = ROOT / name.replace(".yaml", ".local.yaml")
        output.write_text(text, encoding="utf-8")
        print(f"已生成 {output.name}")
    print("导入 mihomo.local.yaml 或 mihomo_smart.local.yaml 到客户端即可；请勿提交 *.local.yaml")


if __name__ == "__main__":
    main()
