from selenium import webdriver
from bs4 import BeautifulSoup
import boto3
from datetime import datetime, timedelta

def remove_noize(text):
    res = text.strip("\xa0")
    res = res.replace('\u200f', "")
    res = res.replace('\u200e', "")
    res = res.replace('&lrm;', "")
    res = res.replace('\n', "")
    res = res.replace(' ', "")
    return res

def get_all_prods():                     
    prod_list = []                        #　初期化
    prod_list = [
        ['https://aws.amazon.com/jp/about-aws/whats-new/analytics/?whats-new-content.sort-by=item.additionalFields.postDateTime&whats-new-content.sort-order=desc&awsf.whats-new-products=*all','分析'],
        ['https://aws.amazon.com/jp/about-aws/whats-new/application-integration/?whats-new-content.sort-by=item.additionalFields.postDateTime&whats-new-content.sort-order=desc&awsf.whats-new-products=*all','アプリケーション統合'],
        ['https://aws.amazon.com/jp/about-aws/whats-new/ar-vr/?whats-new-content.sort-by=item.additionalFields.postDateTime&whats-new-content.sort-order=desc&awsf.whats-new-products=*all',"AR & VR"],
        ['https://aws.amazon.com/jp/about-aws/whats-new/blockchain/?whats-new-content.sort-by=item.additionalFields.postDateTime&whats-new-content.sort-order=desc&awsf.whats-new-products=*all', "ブロックチェーン"],
        ["https://aws.amazon.com/jp/about-aws/whats-new/business-applications/?whats-new-content.sort-by=item.additionalFields.postDateTime&whats-new-content.sort-order=desc&awsf.whats-new-products=*all","ビジネスアプリケーション"],
        ["https://aws.amazon.com/jp/about-aws/whats-new/cloud-financial-management/?whats-new-content.sort-by=item.additionalFields.postDateTime&whats-new-content.sort-order=desc&awsf.whats-new-products=*all","コスト管理"],
        ["https://aws.amazon.com/jp/about-aws/whats-new/compute/?whats-new-content.sort-by=item.additionalFields.postDateTime&whats-new-content.sort-order=desc&awsf.whats-new-products=*all","コンピューティング"],
        ["https://aws.amazon.com/jp/new/?nc1=h_ls&whats-new-content-all.sort-by=item.additionalFields.postDateTime&whats-new-content-all.sort-order=desc&awsf.whats-new-analytics=*all&awsf.whats-new-app-integration=*all&awsf.whats-new-arvr=*all&awsf.whats-new-blockchain=*all&awsf.whats-new-business-applications=*all&awsf.whats-new-cloud-financial-management=*all&awsf.whats-new-compute=*all&awsf.whats-new-containers=general-products%23aws-copilot%7Cgeneral-products%23amazon-ecr%7Cgeneral-products%23amazon-ecs%7Cgeneral-products%23aws-fargate%7Cgeneral-products%23amazon-eks&awsf.whats-new-customer-enablement=*all&awsf.whats-new-customer%20engagement=*all&awsf.whats-new-database=*all&awsf.whats-new-developer-tools=*all&awsf.whats-new-end-user-computing=*all&awsf.whats-new-mobile=*all&awsf.whats-new-gametech=*all&awsf.whats-new-iot=*all&awsf.whats-new-machine-learning=*all&awsf.whats-new-management-governance=*all&awsf.whats-new-media-services=*all&awsf.whats-new-migration-transfer=*all&awsf.whats-new-networking-content-delivery=*all&awsf.whats-new-quantum-tech=*all&awsf.whats-new-robotics=*all&awsf.whats-new-satellite=*all&awsf.whats-new-security-id-compliance=*all&awsf.whats-new-serverless=*all&awsf.whats-new-storage=*all","コンテナ"],
        ["https://aws.amazon.com/jp/about-aws/whats-new/customer-engagement/?whats-new-content.sort-by=item.additionalFields.postDateTime&whats-new-content.sort-order=desc&awsf.whats-new-products=*all","カスタマーエンゲージメント"],
        ["https://aws.amazon.com/jp/about-aws/whats-new/database/?whats-new-content.sort-by=item.additionalFields.postDateTime&whats-new-content.sort-order=desc&awsf.whats-new-products=*all","データベース"],
        ["https://aws.amazon.com/jp/about-aws/whats-new/developer-tools/?whats-new-content.sort-by=item.additionalFields.postDateTime&whats-new-content.sort-order=desc&awsf.whats-new-products=*all","Dev ツール"],
        ["https://aws.amazon.com/jp/about-aws/whats-new/end-user-computing/?whats-new-content.sort-by=item.additionalFields.postDateTime&whats-new-content.sort-order=desc&awsf.whats-new-products=*all","エンドユーザコンピュート"],
        ["https://aws.amazon.com/jp/about-aws/whats-new/front-end-web-and-mobile/?whats-new-content.sort-by=item.additionalFields.postDateTime&whats-new-content.sort-order=desc&awsf.whats-new-products=*all","フロントエンドweb、モバイル"],
        ["https://aws.amazon.com/jp/about-aws/whats-new/internet-of-things/?whats-new-content.sort-by=item.additionalFields.postDateTime&whats-new-content.sort-order=desc&awsf.whats-new-products=*all","IoT"],
        ["https://aws.amazon.com/jp/about-aws/whats-new/machine-learning/?whats-new-content.sort-by=item.additionalFields.postDateTime&whats-new-content.sort-order=desc&awsf.whats-new-products=*all","Machine learning"],
        ["https://aws.amazon.com/jp/about-aws/whats-new/management-and-governance/?whats-new-content.sort-by=item.additionalFields.postDateTime&whats-new-content.sort-order=desc&awsf.whats-new-products=*all","マネジメント、ガバナンス"],
        ["https://aws.amazon.com/jp/about-aws/whats-new/media-services/?whats-new-content.sort-by=item.additionalFields.postDateTime&whats-new-content.sort-order=desc&awsf.whats-new-products=*all","メディアサービス"],
        ["https://aws.amazon.com/jp/about-aws/whats-new/migration-and-transfer/?whats-new-content.sort-by=item.additionalFields.postDateTime&whats-new-content.sort-order=desc&awsf.whats-new-products=*all","マイグレーション、転送"],
        ["https://aws.amazon.com/jp/about-aws/whats-new/networking_and_content_delivery/?whats-new-content.sort-by=item.additionalFields.postDateTime&whats-new-content.sort-order=desc&awsf.whats-new-products=*all","ネットワーク、コンテンツ配信"],
        ["https://aws.amazon.com/jp/about-aws/whats-new/security_identity_and_compliance/?whats-new-content.sort-by=item.additionalFields.postDateTime&whats-new-content.sort-order=desc&awsf.whats-new-products=*all","セキュリティ、コンプライアンス"],
        ["https://aws.amazon.com/jp/new/?nc1=h_ls&whats-new-content-all.sort-by=item.additionalFields.postDateTime&whats-new-content-all.sort-order=desc&awsf.whats-new-analytics=*all&awsf.whats-new-app-integration=general-products%23amazon-sqs&awsf.whats-new-arvr=*all&awsf.whats-new-blockchain=*all&awsf.whats-new-business-applications=*all&awsf.whats-new-cloud-financial-management=*all&awsf.whats-new-compute=*all&awsf.whats-new-containers=*all&awsf.whats-new-customer-enablement=*all&awsf.whats-new-customer%20engagement=*all&awsf.whats-new-database=*all&awsf.whats-new-developer-tools=*all&awsf.whats-new-end-user-computing=*all&awsf.whats-new-mobile=*all&awsf.whats-new-gametech=*all&awsf.whats-new-iot=*all&awsf.whats-new-machine-learning=*all&awsf.whats-new-management-governance=*all&awsf.whats-new-media-services=*all&awsf.whats-new-migration-transfer=*all&awsf.whats-new-networking-content-delivery=*all&awsf.whats-new-quantum-tech=*all&awsf.whats-new-robotics=*all&awsf.whats-new-satellite=*all&awsf.whats-new-security-id-compliance=*all&awsf.whats-new-serverless=general-products%23aws-lambda%7Cgeneral-products%23aws-step-functions%7Cgeneral-products%23amazon-sns%7Cgeneral-products%23amazon-sqs%7Cgeneral-products%23amazon-eventbridge%7Cgeneral-products%23amazon-api-gateway&awsf.whats-new-storage=*all","サーバレス"],
        ["https://aws.amazon.com/jp/about-aws/whats-new/storage/?whats-new-content.sort-by=item.additionalFields.postDateTime&whats-new-content.sort-order=desc&awsf.whats-new-products=*all","Storage"]
    ]
 
    return prod_list

def get_amazon_page_info(url):
    text = ""                               #　初期化
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--hide-scrollbars")
    options.add_argument("--single-process")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--window-size=880x996")
    options.add_argument("--no-sandbox")
    options.add_argument("--homedir=/tmp")
    options.binary_location = "/opt/headless/python/bin/headless-chromium"

    #ブラウザの定義
    browser = webdriver.Chrome(
        "/opt/headless/python/bin/chromedriver",
        options=options
    )
    
    browser.get(url)
    text = browser.page_source               #　ページ情報を取得
    browser.close()

    return text


def lambda_handler(event, context):
    prod_list = get_all_prods() 
    deleteTime = datetime.now()
    deleteTime = deleteTime + timedelta(days=31)
    deleteEpocTime = int(deleteTime.timestamp())
    
    try:
        dynamoDB = boto3.resource("dynamodb")
        table = dynamoDB.Table("sourceTable-es3xck76ybbjvizulygc5obree-dev") # DynamoDBのテーブル名
        # table = dynamoDB.Table("voteTable-susnhidebbfzpiaefclhfh77rq-dev") # DynamoDBのテーブル名
        
        
        for prod_link_url in prod_list:
            output_list_one =[]
            text = get_amazon_page_info(prod_link_url[0])    #　ページ情報(HTML)を取得する
            prod_bs = BeautifulSoup(text, "html.parser")    #　HTML情報を解析する
            articles = prod_bs.find_all(class_='m-card')
            for article in articles:
                art_title = article.find("a")
                print (art_title)
                url = "https://aws.amazon.com/jp/" + str(art_title.get("href"))
                name = art_title.get_text()
                art_date = article.find(class_="m-card-info")
                date = remove_noize(art_date.get_text())
                dateYM = date[0:7]
                createdAt = str(datetime.now().isoformat()) + "Z"
                updatedAt = str(datetime.now().isoformat()) + "Z"
                nowYM = datetime.now().strftime("%Y/%m")
                output_list_one = [prod_link_url[1],date,name,url,createdAt,updatedAt]
                print (output_list_one)
                print (dateYM)
                print (nowYM)
                 # DynamoDBへのPut処理実行
                if dateYM == nowYM  :
                # if dateYM == "2021/09" :
                    try:

                        response = table.put_item(
                            Item = {
                                "title": name, # Partition Keyのデータ
                                "category": prod_link_url[1],  # その他のデータ
                                "date": date,
                                "url": url,
                                "createdAt" : createdAt,
                                "updatedAt" : updatedAt,
                                "deleteEpocTime" : deleteEpocTime,
                                "voteCount": 0
                            },
                            ConditionExpression = 'attribute_not_exists(title)'
                        )
                    except Exception as err:
                        print (err)
                else:
                    pass
                    
    except Exception as e:
        print (e)