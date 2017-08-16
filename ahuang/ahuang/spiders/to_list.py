import json
#python to_list.py -s baidu.json -t baidu.txt
def main(source, target):
    with open(source) as f:
        items = json.load(f)
    with open(target, "a") as f:
        for item in items:
            f.write("{}\n".format(item["url"]).encode("utf-8"))


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Export scrapy result json to plain text')
    parser.add_argument("-s", "--source", required=True, help="scrapy result file,json format")
    parser.add_argument("-t", "--target", required=True, help="plain text path")

    args = parser.parse_args()
    main(args.source, args.target)