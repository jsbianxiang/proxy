from pathlib import Path

ROOT = Path(__file__).resolve().parent
SUB_FILE = ROOT / "subscriptions.local.txt"
TEMPLATES = ["mihomo.yaml", "mihomo_smart.yaml"]
SLOTS = 4


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
        if "example.com" in line:
            raise SystemExit("检测到 example.com 示例链接，请先替换成真实订阅地址")
        links.append(line)
    if not links:
        raise SystemExit("subscriptions.local.txt 中没有有效订阅链接")
    if len(links) > SLOTS:
        raise SystemExit(f"最多支持 {SLOTS} 条订阅链接")
    if len(links) < SLOTS:
        print(f"警告: 只提供 {len(links)} 条订阅，缺少的槽位将复用最后一条；如需区分地区请手动调整分组")
        links.extend([links[-1]] * (SLOTS - len(links)))
    return links


def main():
    links = read_subscriptions()
    for name in TEMPLATES:
        text = (ROOT / name).read_text(encoding="utf-8")
        for index, link in enumerate(links, start=1):
            text = text.replace(f"订阅链接{index}", link)
        output = ROOT / name.replace(".yaml", ".local.yaml")
        output.write_text(text, encoding="utf-8")
        print(f"已生成 {output.name}")
    print("导入 mihomo.local.yaml 或 mihomo_smart.local.yaml 到客户端即可；请勿提交 *.local.yaml")


if __name__ == "__main__":
    main()
